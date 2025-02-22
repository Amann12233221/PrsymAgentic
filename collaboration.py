from typing import List, Dict, Any
import uuid
from ..core.orchestrator import AgentOrchestrator
from ..core.interfaces import TaskData
import logging

class CollaborationManager:
    def __init__(self, orchestrator: AgentOrchestrator):
        self.orchestrator = orchestrator
        self.task_groups: Dict[str, List[TaskData]] = {}
        self.logger = logging.getLogger(__name__)
        
    def create_task_group(self, tasks: List[TaskData]) -> str:
        """Create a new task group"""
        group_id = str(uuid.uuid4())
        self.task_groups[group_id] = tasks
        self.logger.info(f"Created task group {group_id} with {len(tasks)} tasks")
        return group_id
        
    def get_available_agents(self) -> List[str]:
        """Get list of available agents"""
        return [
            agent_id for agent_id, agent_data in self.orchestrator.agents.items()
            if agent_data['status'] == 'idle'
        ]
        
    def assign_tasks(self, group_id: str) -> Dict[str, List[str]]:
        """Assign tasks to available agents"""
        if group_id not in self.task_groups:
            raise ValueError(f"Task group {group_id} not found")
            
        available_agents = self.get_available_agents()
        if not available_agents:
            raise ValueError("No agents available")
            
        assignments: Dict[str, List[str]] = {}
        tasks = self.task_groups[group_id]
        
        # Simple round-robin assignment
        for i, task in enumerate(tasks):
            agent_id = available_agents[i % len(available_agents)]
            if agent_id not in assignments:
                assignments[agent_id] = []
            assignments[agent_id].append(task.task_id)
            
        return assignments 