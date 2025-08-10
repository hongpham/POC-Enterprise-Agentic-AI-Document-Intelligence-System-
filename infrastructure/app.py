#!/usr/bin/env python3
import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_iam as iam,
    aws_events as events,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    Duration
)

class AgenticAIStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # S3 bucket for document storage
        self.document_bucket = s3.Bucket(
            self, "DocumentBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED
        )
        
        # DynamoDB tables for agent memory
        self.working_memory_table = dynamodb.Table(
            self, "WorkingMemoryTable",
            partition_key=dynamodb.Attribute(name="session_id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            time_to_live_attribute="ttl"
        )
        
        self.episodic_memory_table = dynamodb.Table(
            self, "EpisodicMemoryTable", 
            partition_key=dynamodb.Attribute(name="interaction_id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )
        
        self.semantic_memory_table = dynamodb.Table(
            self, "SemanticMemoryTable",
            partition_key=dynamodb.Attribute(name="concept", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )
        
        # IAM role for agents
        self.agent_role = iam.Role(
            self, "AgentExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ]
        )
        
        # Add Bedrock permissions
        self.agent_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelWithResponseStream"
                ],
                resources=["*"]
            )
        )
        
        # Lambda functions for each agent
        self.supervisor_agent = self._create_agent_lambda("SupervisorAgent", "supervisor_agent.py")
        self.perception_agent = self._create_agent_lambda("PerceptionAgent", "document_perception_agent.py")
        self.analysis_agent = self._create_agent_lambda("AnalysisAgent", "analysis_agent.py")
        self.action_agent = self._create_agent_lambda("ActionAgent", "action_agent.py")
        
        # EventBridge for agent communication
        self.agent_bus = events.EventBus(self, "AgentEventBus")
        
        # Step Functions for workflow orchestration
        self.create_workflow_state_machine()
    
    def _create_agent_lambda(self, name: str, handler_file: str) -> _lambda.Function:
        """Create Lambda function for agent"""
        return _lambda.Function(
            self, name,
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler=f"{handler_file.replace('.py', '')}.handler",
            code=_lambda.Code.from_asset("../src/agents"),
            role=self.agent_role,
            timeout=Duration.minutes(5),
            memory_size=1024,
            environment={
                "WORKING_MEMORY_TABLE": self.working_memory_table.table_name,
                "EPISODIC_MEMORY_TABLE": self.episodic_memory_table.table_name,
                "SEMANTIC_MEMORY_TABLE": self.semantic_memory_table.table_name,
                "DOCUMENT_BUCKET": self.document_bucket.bucket_name
            }
        )
    
    def create_workflow_state_machine(self):
        """Create Step Functions workflow for document processing"""
        # Define workflow steps
        perception_task = tasks.LambdaInvoke(
            self, "DocumentPerception",
            lambda_function=self.perception_agent,
            output_path="$.Payload"
        )
        
        analysis_task = tasks.LambdaInvoke(
            self, "DocumentAnalysis", 
            lambda_function=self.analysis_agent,
            output_path="$.Payload"
        )
        
        action_task = tasks.LambdaInvoke(
            self, "ActionExecution",
            lambda_function=self.action_agent,
            output_path="$.Payload"
        )
        
        # Chain the tasks
        definition = perception_task.next(analysis_task).next(action_task)
        
        self.workflow = sfn.StateMachine(
            self, "DocumentProcessingWorkflow",
            definition=definition,
            timeout=Duration.minutes(30)
        )

app = cdk.App()
AgenticAIStack(app, "AgenticAIStack")
app.synth()
