# Deployment Guide

## Prerequisites

### 1. AWS Account Setup
- AWS CLI installed and configured with appropriate permissions
- AWS account with access to: Lambda, DynamoDB, S3, Bedrock, EventBridge, Step Functions
- Recommended regions: `us-east-1` or `us-west-2` (full Bedrock model availability)

### 2. Local Environment
```bash
# Install Node.js (required for CDK)
# macOS: brew install node
# Ubuntu: sudo apt install nodejs npm
# Windows: Download from nodejs.org

# Install AWS CDK
npm install -g aws-cdk

# Verify installations
node --version
cdk --version
aws --version
```

### 3. Configure AWS Credentials
```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and preferred region
```

## Deployment Steps

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd enterprise-agentic-ai
pip install -r requirements.txt
```

### 2. Deploy Infrastructure
```bash
# Make deployment script executable
chmod +x deploy.sh

# Deploy the complete architecture
./deploy.sh
```

### 3. Enable Bedrock Models
**Manual step required in AWS Console:**

1. Navigate to AWS Console > Amazon Bedrock > Model access
2. Request access for these models:
   - `anthropic.claude-3-sonnet-20240229-v1:0`
   - `amazon.titan-embed-text-v1`
3. Wait for approval (usually instant for most accounts)

Alternatively, check model availability:
```bash
python3 enable_bedrock_models.py
```

### 4. Verify Deployment
```bash
python3 test_deployment.py
```

## Architecture Components

### AWS Services Deployed
- **4 Lambda Functions**: Supervisor, Perception, Analysis, Action agents
- **3 DynamoDB Tables**: Working, episodic, and semantic memory
- **1 S3 Bucket**: Document storage
- **1 Step Functions State Machine**: Workflow orchestration
- **1 EventBridge Event Bus**: Agent communication
- **IAM Roles**: Secure service permissions

### Resource Naming Convention
- Lambda Functions: `SupervisorAgent`, `PerceptionAgent`, `AnalysisAgent`, `ActionAgent`
- DynamoDB Tables: `working-memory`, `episodic-memory`, `semantic-memory`
- S3 Bucket: `agenticsystem-documentbucket-<random>`
- Step Functions: `DocumentProcessingWorkflow`

## Cost Considerations

### Pay-per-Use Services
- **Lambda**: $0.20 per 1M requests + compute time
- **DynamoDB**: $0.25 per million read/write requests
- **Bedrock**: ~$0.003 per 1K input tokens, ~$0.015 per 1K output tokens
- **S3**: $0.023 per GB storage
- **Step Functions**: $0.025 per 1K state transitions

### Estimated Monthly Cost
- Light usage (100 documents): ~$10-20
- Medium usage (1000 documents): ~$50-100
- Heavy usage (10000 documents): ~$200-500

## Security Features

### Built-in Security
- IAM roles with least-privilege access
- S3 bucket encryption enabled
- DynamoDB encryption at rest
- VPC isolation ready (optional)
- CloudTrail audit logging

### Compliance Ready
- All actions logged for audit trails
- Data retention policies configurable
- GDPR/CCPA deletion capabilities
- SOC 2 Type II compliant services

## Troubleshooting

### Common Issues

**1. CDK Bootstrap Error**
```bash
cdk bootstrap aws://ACCOUNT-NUMBER/REGION
```

**2. Bedrock Access Denied**
- Ensure models are enabled in AWS Console
- Check region availability for Bedrock
- Verify IAM permissions include `bedrock:InvokeModel`

**3. Lambda Timeout**
- Default timeout is 5 minutes
- Increase if processing large documents
- Monitor CloudWatch logs for performance

**4. DynamoDB Throttling**
- Tables use on-demand billing
- Auto-scales based on traffic
- Monitor CloudWatch metrics

### Monitoring and Logs
- **CloudWatch Logs**: `/aws/lambda/[FunctionName]`
- **X-Ray Tracing**: Enabled for performance monitoring
- **CloudWatch Metrics**: Custom metrics for agent performance
- **EventBridge**: Message flow monitoring

## Cleanup

### Remove All Resources
```bash
cd infrastructure
cdk destroy
```

### Manual Cleanup (if needed)
- Empty S3 buckets before deletion
- Check for any remaining CloudWatch log groups
- Verify all DynamoDB tables are deleted

## Support

### Documentation
- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)

### Monitoring
- CloudWatch Dashboard: Monitor all services
- X-Ray Service Map: Visualize request flow
- Cost Explorer: Track spending

## Next Steps

After successful deployment:

1. **Upload Test Documents**: Add PDFs/images to S3 bucket
2. **Test Workflows**: Use Step Functions console to trigger processing
3. **Monitor Performance**: Check CloudWatch metrics and logs
4. **Scale Configuration**: Adjust Lambda memory/timeout as needed
5. **Add Custom Logic**: Extend agents for specific business requirements
