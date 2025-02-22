from typing import Dict, List, Any
import asyncio
from ..core.interfaces import WorkflowData
from ..core.event_bus import EventBus

class WorkflowSharingManager:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.workflow_cache: Dict[str, WorkflowData] = {}
        self.subscriptions: Dict[str, List[str]] = {}

    async def share_workflow(self, workflow: WorkflowData, source_agent_id: str):
        # Store in cache
        self.workflow_cache[workflow.workflow_id] = workflow
        
        # Notify subscribers
        message = {
            'type': 'workflow_update',
            'source_agent': source_agent_id,
            'workflow_id': workflow.workflow_id,
            'workflow_data': workflow.__dict__
        }
        
        # Publish to relevant subscribers
        for agent_id in self.subscriptions.get(source_agent_id, []):
            await self._notify_agent(agent_id, message)

    async def _notify_agent(self, agent_id: str, message: Dict[str, Any]):
        # Implement actual notification logic
        self.event_bus.publish('workflow_update', {
            'target_agent': agent_id,
            'message': message
        })

    def subscribe_to_agent(self, subscriber_id: str, target_agent_id: str):
        if target_agent_id not in self.subscriptions:
            self.subscriptions[target_agent_id] = []
        self.subscriptions[target_agent_id].append(subscriber_id)

    def get_cached_workflow(self, workflow_id: str) -> WorkflowData:
        return self.workflow_cache.get(workflow_id) 