from typing import Dict, Any, List, Optional
import asyncio
from collections import defaultdict
import networkx as nx
import json
from redis import asyncio as aioredis

class PerformanceOptimizer:
    def __init__(self):
        self.dependency_graph = nx.DiGraph()
        self.performance_metrics = defaultdict(list)
        
    async def optimize_execution(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[List[Dict[str, Any]]]:
        """Optimize task execution order"""
        # Build dependency graph
        for task in tasks:
            self.dependency_graph.add_node(task['id'])
            for dep in task.get('dependencies', []):
                self.dependency_graph.add_edge(dep, task['id'])
                
        # Find parallel execution groups
        execution_groups = []
        remaining_nodes = set(self.dependency_graph.nodes())
        
        while remaining_nodes:
            # Find nodes with no dependencies
            available = {
                node for node in remaining_nodes
                if not any(pred in remaining_nodes 
                          for pred in self.dependency_graph.predecessors(node))
            }
            
            if not available:
                raise ValueError("Circular dependency detected")
                
            execution_groups.append(available)
            remaining_nodes -= available
            
        return execution_groups

class QueueManager:
    def __init__(self, redis_url: str):
        self.redis = aioredis.from_url(redis_url)
        self.queues = defaultdict(asyncio.Queue)
        
    async def enqueue_task(self, agent_id: str, task: Dict[str, Any]):
        """Enqueue task with priority"""
        priority = task.get('priority', 0)
        await self.redis.zadd(
            f"queue:{agent_id}",
            {json.dumps(task): priority}
        )
        
    async def dequeue_task(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Dequeue highest priority task"""
        task = await self.redis.zpopmax(f"queue:{agent_id}")
        if task:
            return json.loads(task[0][0])
        return None 