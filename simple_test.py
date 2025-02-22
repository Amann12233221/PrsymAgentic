import asyncio
from src.core.enhanced_orchestrator import EnhancedOrchestrator

async def main():
    # Configuration with local Redis (you can modify these URLs as needed)
    config = {
        'cache_url': 'redis://localhost:6379/0',
        'queue_url': 'redis://localhost:6379/1',
        'redis_url': 'redis://localhost:6379/2'
    }
    
    orchestrator = EnhancedOrchestrator(config)
    
    # Simple test workflow
    test_workflow = {
        'id': 'test_workflow_1',
        'tasks': [
            {
                'id': 'task_1',
                'agent_id': 'openai_agent',
                'data': {
                    'prompt': 'What is artificial intelligence?'
                },
                'dependencies': []
            }
        ]
    }
    
    try:
        print("Starting workflow execution...")
        results = await orchestrator.execute_workflow(test_workflow)
        print("\nWorkflow Results:")
        print("-" * 50)
        for result in results:
            print(f"Task ID: {result.get('task_id')}")
            print(f"Status: {result.get('status')}")
            print(f"Response: {result.get('response')}\n")
            
    except Exception as e:
        print(f"Error executing workflow: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 