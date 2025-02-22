from abc import ABC, abstractmethod
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class TaskData:
    task_id: str
    task_type: str
    parameters: Dict[str, Any]
    priority: int = 1

@dataclass
class WorkflowData:
    workflow_id: str
    steps: list[Dict[str, Any]]
    metadata: Dict[str, Any]

class AgentInterface(ABC):
    """Standard interface that all agents must implement"""
    
    @abstractmethod
    async def execute_task(self, task_data: TaskData) -> Dict[str, Any]:
        """Execute a given task and return results"""
        pass
        
    @abstractmethod
    def share_workflow(self) -> WorkflowData:
        """Share current workflow data"""
        pass
        
    @abstractmethod
    def receive_workflow(self, workflow_data: WorkflowData) -> None:
        """Process received workflow data"""
        pass 