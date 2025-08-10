# Project Structure

```
enterprise-agentic-ai/
├── README.md                           # Project overview and architecture
├── DEPLOYMENT.md                       # Deployment instructions
├── PROJECT_STRUCTURE.md               # This file
├── requirements.txt                    # Python dependencies
├── deploy.sh                          # Automated deployment script
├── test_deployment.py                 # Deployment validation
├── enable_bedrock_models.py           # Bedrock model setup
│
├── src/                               # Source code
│   ├── agents/                        # Core agent implementations
│   │   ├── supervisor_agent.py        # Orchestration and task delegation
│   │   ├── document_perception_agent.py # Document extraction and understanding
│   │   ├── analysis_agent.py          # Deep reasoning and compliance
│   │   └── action_agent.py            # Process execution and integration
│   │
│   └── memory/                        # Memory management system
│       └── agent_memory.py            # Multi-tier memory architecture
│
├── infrastructure/                    # Infrastructure as Code
│   ├── app.py                         # CDK application entry point
│   ├── cdk.json                       # CDK configuration
│   └── requirements.txt               # CDK dependencies
│
├── tests/                             # Test files (optional)
│   ├── unit/                          # Unit tests
│   └── integration/                   # Integration tests
│
└── docs/                              # Additional documentation
    ├── architecture_diagrams/         # System architecture visuals
    ├── api_documentation/             # API specifications
    └── business_use_cases/            # Use case examples
```

## Key Files Description

### Core Application
- **`src/agents/`**: Contains the four main agents implementing enterprise agentic AI patterns
- **`src/memory/`**: Hierarchical memory system for context retention and learning
- **`infrastructure/app.py`**: Complete AWS infrastructure definition using CDK

### Deployment & Operations
- **`deploy.sh`**: One-command deployment script
- **`test_deployment.py`**: Validates successful deployment
- **`DEPLOYMENT.md`**: Comprehensive deployment guide

### Configuration
- **`requirements.txt`**: Python package dependencies
- **`infrastructure/cdk.json`**: CDK framework configuration
- **`enable_bedrock_models.py`**: Bedrock model access setup

## Architecture Patterns Implemented

### Agent Patterns
- **Supervisor Pattern**: Central orchestration and task delegation
- **Agent Broker Pattern**: Dynamic agent selection and load balancing
- **Multi-Agent Collaboration**: Coordinated reasoning across specialized agents

### Memory Architecture
- **Working Memory**: Current session context (DynamoDB with TTL)
- **Episodic Memory**: Historical interactions for learning
- **Semantic Memory**: Domain knowledge and patterns
- **Procedural Memory**: Optimized workflows (Step Functions)

### Enterprise Features
- **Security**: IAM roles, encryption, audit trails
- **Scalability**: Auto-scaling, serverless architecture
- **Monitoring**: CloudWatch, X-Ray tracing
- **Compliance**: Audit logging, data governance

## Technology Stack

### AWS Services
- **Amazon Bedrock**: Foundation models (Claude, Titan)
- **AWS Lambda**: Serverless agent execution
- **Amazon DynamoDB**: Agent state and memory management
- **Amazon S3**: Document storage and archival
- **AWS Step Functions**: Workflow orchestration
- **Amazon EventBridge**: Agent communication
- **Amazon Textract**: Document processing
- **Amazon Comprehend**: Entity recognition
- **Amazon OpenSearch**: Vector search and RAG

### Development Tools
- **AWS CDK**: Infrastructure as Code
- **Python 3.11**: Primary development language
- **Boto3**: AWS SDK for Python
