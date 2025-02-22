from src.core.orchestrator import AgentOrchestrator
from src.managers.collaboration import CollaborationManager
from src.core.interfaces import TaskData
from examples.sample_agents import SimpleAgent
from src.agents.specialized_agents import AIAgent, DataProcessingAgent
from src.managers.advanced_collaboration import AdvancedCollaborationManager
from src.monitoring.advanced_metrics import AdvancedMetricsCollector
from src.storage.persistence import WorkflowStorage
from src.managers.workflow_sharing import WorkflowSharingManager
import logging
import asyncio
from typing import List
from dataclasses import dataclass

@dataclass
class AgentCapability:
    agent_id: str
    specialties: List[str]
    performance_score: float
    max_concurrent_tasks: int

class OrchestrationSystem:
    def __init__(self):
        self.orchestrator = AgentOrchestrator()
        self.metrics_collector = AdvancedMetricsCollector()
        self.workflow_storage = WorkflowStorage()
        self.workflow_sharing = WorkflowSharingManager(self.orchestrator.observation_bus)

    async def execute_task_with_agent(self, agent_id: str, task: TaskData):
        self.metrics_collector.start_task_monitoring(task.task_id, agent_id)
        result = await self.orchestrator.execute_task(agent_id, task)
        self.metrics_collector.end_task_monitoring(task.task_id, agent_id, result)
        
        workflow = self.orchestrator.agents[agent_id]['interface'].share_workflow()
        self.workflow_storage.save_workflow(workflow, agent_id)
        await self.workflow_sharing.share_workflow(workflow, agent_id)
        return result

    async def run_system(self):
        # Register specialized agents
        ai_agent = AIAgent("gpt-4", "your-api-key")
        data_agent = DataProcessingAgent("data-processing")
        
        self.orchestrator.register_agent("ai_agent", ai_agent)
        self.orchestrator.register_agent("data_agent", data_agent)
        
        # Set up advanced collaboration
        collab_manager = AdvancedCollaborationManager(self.orchestrator)
        collab_manager.register_agent_capability(
            AgentCapability("ai_agent", ["text", "analysis"], 0.9, 5)
        )
        
        # Create and assign tasks
        tasks = [
            TaskData(f"task_{i}", "text", {"data": f"sample_{i}"}, i % 3 + 1)
            for i in range(5)
        ]
        
        assignments = collab_manager.assign_tasks_optimized(tasks)
        
        # Execute tasks and collect metrics
        for agent_id, agent_tasks in assignments.items():
            for task in agent_tasks:
                await self.execute_task_with_agent(agent_id, task)
        
        # Generate performance report
        performance_report = self.metrics_collector.generate_performance_report()
        print("Performance Report:", performance_report)

def main():
    # Configure basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator()
    collaboration_manager = CollaborationManager(orchestrator)
    
    # Register sample agents
    agents = [
        SimpleAgent("agent1"),
        SimpleAgent("agent2"),
        SimpleAgent("agent3")
    ]
    
    for i, agent in enumerate(agents):
        orchestrator.register_agent(f"agent{i+1}", agent)
    
    # Create sample tasks
    tasks = [
        TaskData(
            task_id=f"task_{i}",
            task_type="sample",
            parameters={"param": f"value_{i}"},
            priority=1
        ) for i in range(5)
    ]
    
    # Create task group and assign tasks
    group_id = collaboration_manager.create_task_group(tasks)
    assignments = collaboration_manager.assign_tasks(group_id)
    
    # Execute tasks
    results = []
    for agent_id, task_ids in assignments.items():
        for task_id in task_ids:
            task = next(t for t in tasks if t.task_id == task_id)
            result = orchestrator.execute_task(agent_id, task)
            results.append(result)
    
    # Share workflows
    for agent_id, agent_data in orchestrator.agents.items():
        workflow = agent_data['interface'].share_workflow()
        orchestrator.observation_bus.publish('workflow_update', workflow.dict())
    
    # Export metrics
    orchestrator.metrics.export_metrics("execution_metrics.json")
    
    system = OrchestrationSystem()
    asyncio.run(system.run_system())

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("Starting multi-agent orchestration system")
    main() 