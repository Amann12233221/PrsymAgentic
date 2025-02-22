from openai import AsyncOpenAI
from typing import Dict, Any
from .base_adapter import AgentAdapter
from ..core.interfaces import TaskData, WorkflowData

class OpenAIAdapter(AgentAdapter):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.client = None
        
    async def initialize(self) -> None:
        self.client = AsyncOpenAI(api_key=self.api_key)
        
    async def execute(self, task_data: TaskData) -> Dict[str, Any]:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": str(task_data.parameters.get('prompt', ''))}
                ]
            )
            return {
                'task_id': task_data.task_id,
                'status': 'completed',
                'response': response.choices[0].message.content,
                'model': self.model
            }
        except Exception as e:
            return {
                'task_id': task_data.task_id,
                'status': 'failed',
                'error': str(e)
            }
            
    async def cleanup(self) -> None:
        """Cleanup any resources"""
        if self.client:
            await self.client.close() 