import asyncio
from src.core.enhanced_orchestrator import EnhancedOrchestrator

async def main():
    config = {
        'cache_url': 'redis://localhost:6379/0',
        'queue_url': 'redis://localhost:6379/1',
        'redis_url': 'redis://localhost:6379/2'
    }
    
    orchestrator = EnhancedOrchestrator(config)
    
    # Complex workflow with multiple agents
    complex_workflow = {
        'id': 'complex_workflow_1',
        'tasks': [
            {
                'id': 'analysis_task',
                'agent_id': 'openai_agent',
                'data': {
                    'prompt': 'Analyze the sentiment of: "This product is amazing!"'
                },
                'dependencies': []
            },
            {
                'id': 'processing_task',
                'agent_id': 'anthropic_agent',
                'data': {
                    'input': 'Take the sentiment analysis and explain why'
                },
                'dependencies': ['analysis_task']
            }
        ]
    }
    
    try:
        print("\nStarting complex workflow execution...")
        print("---------------------------------------")
        
        results = await orchestrator.execute_workflow(complex_workflow)
        
        print("\nWorkflow Results:")
        print("----------------")
        
        for result in results:
            print(f"\nTask ID: {result.get('task_id')}")
            print(f"Agent: {result.get('agent_id')}")
            print(f"Status: {result.get('status')}")
            print(f"Response: {result.get('response')}")
            print(f"Execution Time: {result.get('execution_time')}s")
            print("-" * 50)
            
        print("\nPerformance Metrics:")
        print("-------------------")
        print(f"Total Execution Time: {sum(r.get('execution_time', 0) for r in results)}s")
        print(f"Cache Hit Rate: {result.get('cache_hit_rate', 0)}%")
        print(f"Resource Usage: {result.get('resource_usage', {})}")
        
    except Exception as e:
        print(f"Error executing workflow: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 