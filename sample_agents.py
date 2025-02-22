from typing import Dict, Any
from src.core.interfaces import AgentInterface, TaskData, WorkflowData

class SimpleAgent(AgentInterface):
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.current_workflow = []
        
    def execute_task(self, task_data: TaskData) -> Dict[str, Any]:
        """Simple task execution"""
        result = {
            'agent': self.agent_name,
            'task_id': task_data.task_id,
            'status': 'completed',
            'result': f"Processed task {task_data.task_id}"
        }
        self.current_workflow.append(result)
        return result
        
    def share_workflow(self) -> WorkflowData:
        """Share current workflow"""
        return WorkflowData(
            workflow_id=f"{self.agent_name}_workflow",
            steps=self.current_workflow,
            metadata={'agent_name': self.agent_name}
        )
        
    def receive_workflow(self, workflow_data: WorkflowData) -> None:
        """Process received workflow"""
        print(f"Received workflow from {workflow_data.metadata['agent_name']}") 