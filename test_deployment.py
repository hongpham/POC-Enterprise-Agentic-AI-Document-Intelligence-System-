#!/usr/bin/env python3
import boto3
import json
import time

def find_resources_by_prefix(prefix):
    """Find resources by name prefix"""
    lambda_client = boto3.client('lambda')
    dynamodb = boto3.client('dynamodb')
    s3_client = boto3.client('s3')
    stepfunctions = boto3.client('stepfunctions')
    
    resources = {}
    
    # Find Lambda functions
    functions = lambda_client.list_functions()['Functions']
    for func in functions:
        name = func['FunctionName']
        if name.startswith(prefix):
            if 'SupervisorAgent' in name:
                resources['SupervisorAgent'] = name
            elif 'PerceptionAgent' in name:
                resources['PerceptionAgent'] = name
            elif 'AnalysisAgent' in name:
                resources['AnalysisAgent'] = name
            elif 'ActionAgent' in name:
                resources['ActionAgent'] = name
    
    # Find DynamoDB tables
    tables = dynamodb.list_tables()['TableNames']
    for table in tables:
        if table.startswith(prefix):
            if 'WorkingMemory' in table:
                resources['working-memory'] = table
            elif 'EpisodicMemory' in table:
                resources['episodic-memory'] = table
            elif 'SemanticMemory' in table:
                resources['semantic-memory'] = table
    
    # Find S3 bucket
    buckets = s3_client.list_buckets()['Buckets']
    for bucket in buckets:
        name = bucket['Name']
        if prefix.lower() in name.lower() and 'document' in name.lower():
            resources['document-bucket'] = name
            break
    
    # Find Step Functions
    workflows = stepfunctions.list_state_machines()['stateMachines']
    for workflow in workflows:
        name = workflow['name']
        if 'DocumentProcessing' in name:
            resources['workflow-arn'] = workflow['stateMachineArn']
            break
    
    return resources

def test_deployment():
    """Test the deployed agentic AI architecture"""
    
    # Initialize AWS clients
    lambda_client = boto3.client('lambda')
    s3_client = boto3.client('s3')
    stepfunctions = boto3.client('stepfunctions')
    
    print("🧪 Testing Enterprise Agentic AI Deployment...")
    
    # Find resources dynamically
    resources = find_resources_by_prefix('AgenticAIStack')
    
    # Test 1: Check Lambda functions
    agent_functions = ['SupervisorAgent', 'PerceptionAgent', 'AnalysisAgent', 'ActionAgent']
    for agent in agent_functions:
        if agent in resources:
            try:
                lambda_client.get_function(FunctionName=resources[agent])
                print(f"✅ {agent} deployed successfully")
            except Exception as e:
                print(f"❌ {agent} error: {e}")
        else:
            print(f"❌ {agent} not found")
    
    # Test 2: Check DynamoDB tables
    memory_tables = ['working-memory', 'episodic-memory', 'semantic-memory']
    dynamodb = boto3.resource('dynamodb')
    for table_type in memory_tables:
        if table_type in resources:
            try:
                table = dynamodb.Table(resources[table_type])
                table.load()
                print(f"✅ {table_type} table exists")
            except Exception as e:
                print(f"❌ {table_type} table error: {e}")
        else:
            print(f"❌ {table_type} table not found")
    
    # Test 3: Check S3 bucket
    if 'document-bucket' in resources:
        try:
            s3_client.head_bucket(Bucket=resources['document-bucket'])
            print(f"✅ Document bucket exists: {resources['document-bucket']}")
        except Exception as e:
            print(f"❌ Document bucket error: {e}")
    else:
        print("❌ Document bucket not found")
    
    # Test 4: Check Step Functions workflow
    if 'workflow-arn' in resources:
        try:
            stepfunctions.describe_state_machine(stateMachineArn=resources['workflow-arn'])
            print("✅ Document processing workflow exists")
        except Exception as e:
            print(f"❌ Step Functions workflow error: {e}")
    else:
        print("❌ Step Functions workflow not found")
    
    # Test 5: Test Bedrock access
    try:
        bedrock = boto3.client('bedrock')
        models = bedrock.list_foundation_models()
        print("✅ Bedrock access confirmed")
    except Exception as e:
        print(f"❌ Bedrock access error: {e}")
    
    print("\n📋 Deployment test complete!")

if __name__ == "__main__":
    test_deployment()

if __name__ == "__main__":
    test_deployment()
