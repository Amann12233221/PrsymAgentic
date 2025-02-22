from typing import Dict, Any, List
import asyncio
from .agent_registry import AgentRegistry
from ..integration.agent_connector import AgentConnector
from ..data.transformation_engine import DataTransformer, DataConsistencyManager
from ..performance.optimization import PerformanceOptimizer, QueueManager

class EnhancedOrchestrator:
    def __init__(self, config: Dict[str, Any]):
        self.registry = AgentRegistry()
        self.connector = AgentConnector(
            config['cache_url'],
            config['queue_url']
        )
        self.transformer = DataTransformer()
        self.consistency_manager = DataConsistencyManager(config['redis_url'])
        self.optimizer = PerformanceOptimizer()
        self.queue_manager = QueueManager(config['redis_url'])
        
    async def execute_workflow(self, workflow: Dict[str, Any]):
        """Execute a multi-agent workflow"""
        try:
            # Optimize task execution
            tasks = workflow['tasks']
            execution_groups = await self.optimizer.optimize_execution(tasks)
            
            results = []
            for group in execution_groups:
                # Execute tasks in parallel within each group
                group_tasks = []
                for task in group:
                    # Ensure data consistency
                    async with self._resource_lock(task):
                        # Transform data if needed
                        transformed_data = await self.transformer.transform_data(
                            task['data'],
                            task['source_agent'],
                            task['target_agent']
                        )
                        
                        # Execute task with retries and rate limiting
                        group_tasks.append(
                            self.connector.execute_with_retry(
                                task['agent_id'],
                                transformed_data
                            )
                        )
                
                # Wait for all tasks in group to complete
                group_results = await asyncio.gather(
                    *group_tasks,
                    return_exceptions=True
                )
                results.extend(group_results)
                
            return results
            
        except Exception as e:
            # Handle failure cascade
            await self._handle_failure_cascade(workflow['id'], str(e))
            raise
            
    async def _resource_lock(self, task: Dict[str, Any]):
        """Context manager for resource locking"""
        resource_id = task.get('resource_id')
        if resource_id:
            try:
                await self.consistency_manager.acquire_lock(resource_id)
                yield
            finally:
                await self.consistency_manager.release_lock(resource_id)
        else:
            yield 