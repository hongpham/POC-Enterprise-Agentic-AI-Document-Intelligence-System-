#!/usr/bin/env python3
import boto3
import json

def enable_bedrock_models():
    """Enable required Bedrock models"""
    
    print("🤖 Enabling Bedrock models...")
    
    # Required models for the architecture
    required_models = [
        'anthropic.claude-3-sonnet-20240229-v1:0',
        'amazon.titan-embed-text-v1'
    ]
    
    bedrock = boto3.client('bedrock')
    
    try:
        # List available models
        available_models = bedrock.list_foundation_models()
        
        print("Available Bedrock models:")
        for model in available_models['modelSummaries']:
            model_id = model['modelId']
            if any(req in model_id for req in required_models):
                print(f"✅ {model_id} - Available")
        
        print("\n📋 Manual step required:")
        print("1. Go to AWS Console > Bedrock > Model access")
        print("2. Enable access for:")
        for model in required_models:
            print(f"   - {model}")
        print("3. Wait for approval (usually instant)")
        
    except Exception as e:
        print(f"❌ Error accessing Bedrock: {e}")
        print("Make sure Bedrock is available in your region")

if __name__ == "__main__":
    enable_bedrock_models()
