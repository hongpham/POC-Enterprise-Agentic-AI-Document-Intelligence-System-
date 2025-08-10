# Testing the Enterprise Agentic AI System

## Prerequisites
- AWS CLI configured with appropriate permissions
- Python 3.8+ installed
- Deployed CloudFormation stack

## 1. Verify Deployment

Run the deployment verification test:
```bash
python3 test_deployment.py
```

Expected output: All components should show ✅ status

## 2. Test Document Processing

### Upload a test document:
```bash
# Get your bucket name from the deployment test output
aws s3 cp sample-invoice.pdf s3://YOUR-DOCUMENT-BUCKET/test-documents/
```

### Trigger the workflow via AWS Console:
1. Go to Step Functions in AWS Console
2. Find "DocumentProcessingWorkflow"
3. Start execution with input:
```json
{
  "document_key": "test-documents/sample-invoice.pdf",
  "task_type": "invoice_processing"
}
```

### Monitor execution:
- Watch the Step Functions execution graph
- Check CloudWatch logs for each agent
- Verify results in DynamoDB tables

## 3. Test Individual Agents

### Test Supervisor Agent:
```bash
aws lambda invoke \
  --function-name $(aws lambda list-functions --query 'Functions[?contains(FunctionName, `SupervisorAgent`)].FunctionName' --output text) \
  --payload '{"task": "analyze_document", "document_key": "test-documents/sample-invoice.pdf"}' \
  response.json
```

### Check agent memory:
```bash
aws dynamodb scan --table-name $(aws dynamodb list-tables --query 'TableNames[?contains(@, `WorkingMemory`)]' --output text)
```

## 4. Validate Business Use Cases

### Contract Intelligence:
- Upload contract PDF to S3
- Trigger workflow with `task_type: "contract_analysis"`
- Check analysis results in DynamoDB

### Invoice Processing:
- Upload invoice document
- Trigger workflow with `task_type: "invoice_processing"`
- Verify extraction and validation results

## 5. Monitor System Health

### Check CloudWatch metrics:
- Lambda function invocations and errors
- DynamoDB read/write capacity
- Step Functions execution success rate

### View logs:
```bash
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/AgenticAIStack"
```

## Expected Results
- ✅ All agents respond successfully
- ✅ Documents processed and stored in memory tables
- ✅ Workflow completes without errors
- ✅ Business insights generated and logged
