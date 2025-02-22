import asyncio
from src.core.orchestrator import AgentOrchestrator
from src.core.interfaces import TaskData

async def main():
    orchestrator = AgentOrchestrator()
    
    # Register different third-party agents
    await orchestrator.register_agent(
        'openai_agent',
        'examples/agent_configs/openai_agent.json'
    )
    
    # Create a task
    task = TaskData(
        task_id="collaborative_task_1",
        task_type="text_processing",
        parameters={"input": "Process this text collaboratively"}
    )
    
    # Execute task with collaboration
    result = await orchestrator.execute_task('openai_agent', task)
    print(f"Task result: {result}")

if __name__ == "__main__":
    asyncio.run(main()) 