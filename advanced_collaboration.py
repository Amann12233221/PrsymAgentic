from typing import List, Dict, Any
import numpy as np
from dataclasses import dataclass
from ..core.interfaces import TaskData

@dataclass
class AgentCapability:
    agent_id: str
    specialties: List[str]
    performance_score: float
    max_concurrent_tasks: int

class AdvancedCollaborationManager:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.agent_capabilities: Dict[str, AgentCapability] = {}
        self.task_history: Dict[str, List[Dict]] = {}
        
    def register_agent_capability(self, capability: AgentCapability):
        self.agent_capabilities[capability.agent_id] = capability

    def assign_tasks_optimized(self, tasks: List[TaskData]) -> Dict[str, List[TaskData]]:
        assignments: Dict[str, List[TaskData]] = {}
        
        # Sort tasks by priority
        sorted_tasks = sorted(tasks, key=lambda x: x.priority, reverse=True)
        
        # Calculate agent scores for each task
        for task in sorted_tasks:
            best_agent = self._find_best_agent_for_task(task)
            if best_agent not in assignments:
                assignments[best_agent] = []
            assignments[best_agent].append(task)
            
        return assignments

    def _find_best_agent_for_task(self, task: TaskData) -> str:
        scores = {}
        for agent_id, capability in self.agent_capabilities.items():
            # Calculate score based on multiple factors
            score = self._calculate_agent_score(capability, task)
            scores[agent_id] = score
            
        return max(scores.items(), key=lambda x: x[1])[0]

    def _calculate_agent_score(self, capability: AgentCapability, task: TaskData) -> float:
        # Implement sophisticated scoring algorithm
        specialty_match = task.task_type in capability.specialties
        workload_factor = len(self.orchestrator.agents[capability.agent_id]['workflows'])
        
        score = (
            capability.performance_score * 0.4 +
            (1.0 if specialty_match else 0.0) * 0.4 +
            (1.0 - (workload_factor / capability.max_concurrent_tasks)) * 0.2
        )
        return score 