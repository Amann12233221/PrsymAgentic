from abc import ABC, abstractmethod
from typing import Dict, Any
from ..core.interfaces import AgentInterface, TaskData, WorkflowData

class AgentAdapter(ABC):
    """Base adapter class for third-party agents"""
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the third-party agent"""
        pass
        
    @abstractmethod
    async def execute(self, task_data: TaskData) -> Dict[str, Any]:
        """Execute task using the third-party agent"""
        pass
        
    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass 