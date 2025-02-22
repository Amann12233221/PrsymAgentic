import asyncio
from src.core.enhanced_orchestrator import EnhancedOrchestrator

async def main():
    config = {
        'cache_url': 'redis://localhost:6379/0',
        'queue_url': 'redis://localhost:6379/1',
        'redis_url': 'redis://localhost:6379/2'
    }
    
    orchestrator = EnhancedOrchestrator(config)
    
    # Define a workflow with multiple agents
    workflow = {
        'id': 'workflow_1',
        'tasks': [
            {
                'id': 'task_1',
                'agent_id': 'openai_agent',
                'data': {'prompt': 'Analyze this text'},
                'dependencies': []
            },
            {
                'id': 'task_2',
                'agent_id': 'anthropic_agent',
                'data': {'input': 'Process results'},
                'dependencies': ['task_1']
            }
        ]
    }
    
    try:
        results = await orchestrator.execute_workflow(workflow)
        print("Workflow completed:", results)
    except Exception as e:
        print("Workflow failed:", str(e))

if __name__ == "__main__":
    asyncio.run(main()) 