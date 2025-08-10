import boto3
import json
import time
from typing import Dict, Any, List, Optional

class AgentMemory:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.s3 = boto3.client('s3')
        self.opensearch = boto3.client('opensearch')
        
        # Memory tables
        self.working_memory = self.dynamodb.Table('working-memory')
        self.episodic_memory = self.dynamodb.Table('episodic-memory')
        self.semantic_memory = self.dynamodb.Table('semantic-memory')
    
    async def store_working_memory(self, session_id: str, context: Dict[str, Any]) -> None:
        """Store current session context"""
        self.working_memory.put_item(
            Item={
                'session_id': session_id,
                'timestamp': int(time.time()),
                'context': context,
                'ttl': int(time.time()) + 3600  # 1 hour TTL
            }
        )
    
    async def get_working_memory(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve current session context"""
        response = self.working_memory.get_item(
            Key={'session_id': session_id}
        )
        return response.get('Item', {}).get('context')
    
    async def store_episodic_memory(self, interaction: Dict[str, Any]) -> None:
        """Store historical interaction"""
        # Store in DynamoDB for structured access
        self.episodic_memory.put_item(
            Item={
                'interaction_id': interaction['id'],
                'timestamp': int(time.time()),
                'user_request': interaction['request'],
                'agent_response': interaction['response'],
                'outcome': interaction['outcome'],
                'performance_metrics': interaction.get('metrics', {})
            }
        )
        
        # Store in S3 for long-term retention
        await self._archive_to_s3(interaction)
    
    async def retrieve_similar_episodes(self, current_context: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve similar past interactions using semantic search"""
        # Create embedding for current context
        embedding = await self._create_embedding(str(current_context))
        
        # Search OpenSearch for similar episodes
        search_query = {
            'query': {
                'knn': {
                    'context_embedding': {
                        'vector': embedding,
                        'k': limit
                    }
                }
            }
        }
        
        return await self._search_episodes(search_query)
    
    async def update_semantic_memory(self, concept: str, knowledge: Dict[str, Any]) -> None:
        """Update domain knowledge and learned patterns"""
        self.semantic_memory.put_item(
            Item={
                'concept': concept,
                'knowledge': knowledge,
                'confidence': knowledge.get('confidence', 0.8),
                'last_updated': int(time.time()),
                'usage_count': knowledge.get('usage_count', 0) + 1
            }
        )
    
    async def get_semantic_knowledge(self, concept: str) -> Optional[Dict[str, Any]]:
        """Retrieve domain knowledge"""
        response = self.semantic_memory.get_item(
            Key={'concept': concept}
        )
        return response.get('Item', {}).get('knowledge')
    
    async def consolidate_memory(self) -> None:
        """Periodic memory consolidation and optimization"""
        # Move old working memory to episodic
        await self._consolidate_working_memory()
        
        # Update semantic patterns from episodic memory
        await self._extract_semantic_patterns()
        
        # Archive old episodic memory to S3
        await self._archive_old_episodes()
    
    async def _create_embedding(self, text: str) -> List[float]:
        """Create vector embedding using Bedrock Titan"""
        bedrock = boto3.client('bedrock-runtime')
        
        response = bedrock.invoke_model(
            modelId='amazon.titan-embed-text-v1',
            body=json.dumps({'inputText': text})
        )
        
        return json.loads(response['body'].read())['embedding']
