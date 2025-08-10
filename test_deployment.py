#!/usr/bin/env python3
import boto3
import json
import time

def test_deployment():
    """Test the deployed agentic AI architecture"""
    
    # Initialize AWS clients
    lambda_client = boto3.client('lambda')
    s3_client = boto3.client('s3')
    stepfunctions = boto3.client('stepfunctions')
    
    print("🧪 Testing Enterprise Agentic AI Deployment...")
    
    # Test 1: Check if Lambda functions exist
    functions = ['SupervisorAgent', 'PerceptionAgent', 'AnalysisAgent', 'ActionAgent']
    for func in functions:
        try:
            response = lambda_client.get_function(FunctionName=func)
            print(f"✅ {func} deployed successfully")
        except Exception as e:
            print(f"❌ {func} not found: {e}")
    
    # Test 2: Check DynamoDB tables
    dynamodb = boto3.resource('dynamodb')
    tables = ['working-memory', 'episodic-memory', 'semantic-memory']
    for table_name in tables:
        try:
            table = dynamodb.Table(table_name)
            table.load()
            print(f"✅ {table_name} table exists")
        except Exception as e:
            print(f"❌ {table_name} table not found: {e}")
    
    # Test 3: Check S3 bucket
    try:
        buckets = s3_client.list_buckets()
        doc_bucket = [b for b in buckets['Buckets'] if 'document' in b['Name'].lower()]
        if doc_bucket:
            print(f"✅ Document bucket exists: {doc_bucket[0]['Name']}")
        else:
            print("❌ Document bucket not found")
    except Exception as e:
        print(f"❌ S3 access error: {e}")
    
    # Test 4: Test Bedrock access
    try:
        bedrock = boto3.client('bedrock')
        models = bedrock.list_foundation_models()
        print("✅ Bedrock access confirmed")
    except Exception as e:
        print(f"❌ Bedrock access error: {e}")
    
    print("\n📋 Deployment test complete!")

if __name__ == "__main__":
    test_deployment()
