import boto3
import json
from typing import Dict, Any, List

class ActionAgent:
    def __init__(self):
        self.lambda_client = boto3.client('lambda')
        self.stepfunctions = boto3.client('stepfunctions')
        self.dynamodb = boto3.resource('dynamodb')
        self.audit_table = self.dynamodb.Table('audit-log')
    
    async def execute_actions(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute business processes based on analysis"""
        # 1. Determine required actions
        actions = await self._determine_actions(analysis_results)
        
        # 2. Execute actions with error handling
        execution_results = []
        for action in actions:
            result = await self._execute_single_action(action)
            execution_results.append(result)
            
            # Log action for audit
            await self._log_action(action, result)
        
        # 3. Validate execution success
        validation = await self._validate_execution(execution_results)
        
        return {
            'actions_executed': execution_results,
            'validation_status': validation,
            'audit_trail': await self._get_audit_trail()
        }
    
    async def _determine_actions(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Determine what actions to take based on analysis"""
        action_prompt = f"""
        Based on this analysis, determine required actions:
        
        Analysis: {analysis['analysis']}
        Compliance: {analysis['compliance_status']}
        Insights: {analysis['insights']}
        
        Return specific actions to execute:
        - approve/reject decisions
        - notifications to send
        - data updates required
        - workflow triggers
        
        Format as structured action list.
        """
        
        response = boto3.client('bedrock-runtime').invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'messages': [{'role': 'user', 'content': action_prompt}],
                'max_tokens': 1000
            })
        )
        
        return self._parse_actions(response)
    
    async def _execute_single_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute individual action with retry logic"""
        action_type = action['type']
        
        try:
            if action_type == 'workflow_trigger':
                return await self._trigger_workflow(action)
            elif action_type == 'notification':
                return await self._send_notification(action)
            elif action_type == 'data_update':
                return await self._update_data(action)
            elif action_type == 'approval_decision':
                return await self._process_approval(action)
            else:
                return {'status': 'unknown_action', 'action': action}
                
        except Exception as e:
            return {
                'status': 'failed',
                'action': action,
                'error': str(e),
                'retry_count': action.get('retry_count', 0) + 1
            }
    
    async def _trigger_workflow(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger Step Functions workflow"""
        response = self.stepfunctions.start_execution(
            stateMachineArn=action['workflow_arn'],
            input=json.dumps(action['payload'])
        )
        
        return {
            'status': 'triggered',
            'execution_arn': response['executionArn'],
            'action_type': 'workflow_trigger'
        }
    
    async def _log_action(self, action: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Log action execution for audit trail"""
        self.audit_table.put_item(
            Item={
                'timestamp': boto3.dynamodb.conditions.Key('timestamp').eq(int(time.time())),
                'action_type': action['type'],
                'action_details': action,
                'execution_result': result,
                'agent_id': 'action-agent'
            }
        )
