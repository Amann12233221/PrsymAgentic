from typing import Dict, Any, Callable
import asyncio
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    sender_id: str
    receiver_id: str
    message_type: str
    content: Dict[str, Any]
    timestamp: datetime = datetime.now()

class CommunicationBus:
    def __init__(self):
        self.channels: Dict[str, asyncio.Queue] = {}
        self.subscribers: Dict[str, Dict[str, Callable]] = {}
        
    async def send_message(self, message: Message):
        """Send a message to a specific agent"""
        if message.receiver_id not in self.channels:
            self.channels[message.receiver_id] = asyncio.Queue()
            
        await self.channels[message.receiver_id].put(message)
        
        # Notify subscribers
        if message.receiver_id in self.subscribers:
            for callback in self.subscribers[message.receiver_id].values():
                await callback(message)
    
    def subscribe(self, agent_id: str, callback: Callable):
        """Subscribe to messages for a specific agent"""
        if agent_id not in self.subscribers:
            self.subscribers[agent_id] = {}
        self.subscribers[agent_id][id(callback)] = callback
        
    async def get_messages(self, agent_id: str) -> Message:
        """Get messages for a specific agent"""
        if agent_id not in self.channels:
            self.channels[agent_id] = asyncio.Queue()
        return await self.channels[agent_id].get() 