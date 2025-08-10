import boto3
import json
from typing import Dict, Any, List

class DocumentPerceptionAgent:
    def __init__(self):
        self.textract = boto3.client('textract')
        self.bedrock = boto3.client('bedrock-runtime')
        self.comprehend = boto3.client('comprehend')
        self.s3 = boto3.client('s3')
    
    async def process_document(self, document_path: str) -> Dict[str, Any]:
        """Extract and understand document content"""
        # 1. Extract text and structure
        extracted_data = await self._extract_document_data(document_path)
        
        # 2. Classify document type
        doc_type = await self._classify_document(extracted_data['text'])
        
        # 3. Extract entities and relationships
        entities = await self._extract_entities(extracted_data['text'])
        
        # 4. Structure the perception results
        return {
            'document_type': doc_type,
            'extracted_text': extracted_data['text'],
            'tables': extracted_data['tables'],
            'entities': entities,
            'confidence_scores': extracted_data['confidence']
        }
    
    async def _extract_document_data(self, document_path: str) -> Dict[str, Any]:
        """Use Textract for document extraction"""
        response = self.textract.analyze_document(
            Document={'S3Object': {'Bucket': 'doc-bucket', 'Name': document_path}},
            FeatureTypes=['TABLES', 'FORMS']
        )
        
        # Process Textract response
        text = self._extract_text_from_blocks(response['Blocks'])
        tables = self._extract_tables_from_blocks(response['Blocks'])
        
        return {
            'text': text,
            'tables': tables,
            'confidence': self._calculate_confidence(response['Blocks'])
        }
    
    async def _classify_document(self, text: str) -> str:
        """Use Bedrock to classify document type"""
        prompt = f"""
        Classify this document type based on content:
        {text[:1000]}...
        
        Return one of: contract, invoice, report, correspondence, legal_document
        """
        
        response = self.bedrock.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 100
            })
        )
        
        return self._parse_classification(response)
    
    async def _extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract named entities using Comprehend"""
        response = self.comprehend.detect_entities(
            Text=text[:5000],  # Comprehend limit
            LanguageCode='en'
        )
        
        return response['Entities']
