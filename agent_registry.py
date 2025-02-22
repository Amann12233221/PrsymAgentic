from typing import Dict, Any, Type, Optional
from .interfaces import AgentInterface
import importlib
import json

class AgentRegistry:
    def __init__(self):
        self.agent_types = {}
        self.agent_configs = {}
        
    def register_agent_type(self, name: str, agent_class: Type[AgentInterface], config: Dict[str, Any]):
        """Register a new type of agent with its configuration"""
        self.agent_types[name] = agent_class
        self.agent_configs[name] = config
        
    def load_agent_from_config(self, config_path: str) -> Optional[AgentInterface]:
        """Load an agent from a configuration file"""
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        agent_type = config.get('type')
        if agent_type not in self.agent_types:
            raise ValueError(f"Unknown agent type: {agent_type}")
            
        agent_class = self.agent_types[agent_type]
        return agent_class(**config.get('parameters', {})) 