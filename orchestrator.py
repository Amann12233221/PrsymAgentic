from typing import Dict, Any
import uuid
from .interfaces import AgentInterface, TaskData, WorkflowData
from .event_bus import EventBus
from ..utils.exceptions import AgentError
from ..monitoring.metrics import MetricsCollector
import logging
from .communication import CommunicationBus, Message
from .agent_registry import AgentRegistry

class AgentOrchestrator:
    def __init__(self):
        self.agents = {}
        self.workflows = {}
        self.registry = AgentRegistry()
        self.communication_bus = CommunicationBus()
        self.logger = logging.getLogger(__name__)
        
    async def register_agent(self, agent_id: str, agent_config: str) -> None:
        """Register a new agent using its configuration"""
        agent = self.registry.load_agent_from_config(agent_config)
        self.agents[agent_id] = {
            'interface': agent,
            'status': 'idle',
            'workflows': []
        }
        
        # Set up message handling for the agent
        self.communication_bus.subscribe(
            agent_id,
            self._handle_agent_message
        )
        
        self.logger.info(f"Agent {agent_id} registered successfully")
        
    async def _handle_agent_message(self, message: Message):
        """Handle inter-agent messages"""
        self.logger.info(f"Message from {message.sender_id} to {message.receiver_id}: {message.message_type}")
        
        if message.message_type == 'task_request':
            # Handle task requests between agents
            await self._handle_task_request(message)
        elif message.message_type == 'workflow_share':
            # Handle workflow sharing
            await self._handle_workflow_share(message)
            
    async def _handle_task_request(self, message: Message):
        """Handle task requests between agents"""
        sender = self.agents[message.sender_id]['interface']
        receiver = self.agents[message.receiver_id]['interface']
        
        task_data = TaskData(**message.content)
        result = await receiver.execute_task(task_data)
        
        # Send response back
        response = Message(
            sender_id=message.receiver_id,
            receiver_id=message.sender_id,
            message_type='task_response',
            content=result
        )
        await self.communication_bus.send_message(response)
        
    async def execute_task(self, agent_id: str, task: TaskData) -> Dict[str, Any]:
        """Execute a task using specified agent - now async"""
        if agent_id not in self.agents:
            raise AgentError(f"Agent {agent_id} not found")
            
        try:
            self.agents[agent_id]['status'] = 'busy'
            # If the agent's execute_task is async, await it
            if hasattr(self.agents[agent_id]['interface'], 'execute_task'):
                result = await self.agents[agent_id]['interface'].execute_task(task)
            else:
                result = self.agents[agent_id]['interface'].execute_task(task)
            
            self.metrics.record_execution(agent_id, task.task_id)
            return result
        except Exception as e:
            self.logger.error(f"Task execution failed for agent {agent_id}: {str(e)}")
            raise AgentError(f"Task execution failed: {str(e)}")
        finally:
            self.agents[agent_id]['status'] = 'idle' 