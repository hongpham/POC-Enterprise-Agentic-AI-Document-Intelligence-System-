#!/bin/bash

# Deploy Enterprise Agentic AI Architecture

echo "🚀 Deploying Enterprise Agentic AI Architecture..."

# Check AWS CLI configuration
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ AWS CLI not configured. Run 'aws configure' first."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Bootstrap CDK (if not already done)
echo "🔧 Bootstrapping CDK..."
cd infrastructure
cdk bootstrap

# Deploy the stack
echo "🏗️ Deploying infrastructure..."
cdk deploy --require-approval never

# Enable Bedrock model access
echo "🤖 Enabling Bedrock model access..."
aws bedrock put-model-invocation-logging-configuration \
    --logging-config '{"cloudWatchConfig":{"logGroupName":"/aws/bedrock/modelinvocations","roleArn":"arn:aws:iam::'$(aws sts get-caller-identity --query Account --output text)':role/service-role/AmazonBedrockExecutionRoleForCloudWatchLogs"}}'

echo "✅ Deployment complete!"
echo "📋 Next steps:"
echo "   1. Enable Bedrock models in AWS Console"
echo "   2. Upload test documents to S3 bucket"
echo "   3. Test the system with sample requests"
