from anthropic import Anthropic
from typing import Dict, Any
from .base_adapter import AgentAdapter
from ..core.interfaces import TaskData, WorkflowData

class AnthropicAdapter(AgentAdapter):
    def __init__(self, api_key: str, model: str = "claude-2"):
        self.api_key = api_key
        self.model = model
        self.client = None
        
    async def initialize(self) -> None:
        self.client = Anthropic(api_key=self.api_key)
        
    async def execute(self, task_data: TaskData) -> Dict[str, Any]:
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": str(task_data.parameters.get('prompt', ''))
                }]
            )
            return {
                'task_id': task_data.task_id,
                'status': 'completed',
                'response': response.content,
                'model': self.model
            }
        except Exception as e:
            return {
                'task_id': task_data.task_id,
                'status': 'failed',
                'error': str(e)
            } 