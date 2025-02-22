from typing import Dict, Any
import json
from datetime import datetime
import pytz
from pydantic import BaseModel, validator
from redis import asyncio as aioredis

class DataTransformer:
    def __init__(self):
        self.schema_registry = {}
        self.transformation_rules = {}
        
    async def transform_data(
        self, 
        data: Dict[str, Any],
        source_agent: str,
        target_agent: str
    ) -> Dict[str, Any]:
        """Transform data between agents"""
        source_schema = self.schema_registry[source_agent]
        target_schema = self.schema_registry[target_agent]
        
        # Apply transformation rules
        transformed = await self._apply_rules(
            data,
            source_schema,
            target_schema
        )
        
        return transformed
        
    async def _apply_rules(
        self,
        data: Dict[str, Any],
        source_schema: Dict,
        target_schema: Dict
    ) -> Dict[str, Any]:
        """Apply transformation rules"""
        transformed = {}
        for field, value in data.items():
            if field in self.transformation_rules:
                transformed[field] = await self.transformation_rules[field](value)
            else:
                transformed[field] = value
        return transformed

class DataConsistencyManager:
    def __init__(self, redis_url: str):
        self.redis = aioredis.from_url(redis_url)
        self.lock_timeout = 30  # seconds
        
    async def acquire_lock(self, resource_id: str) -> bool:
        """Acquire distributed lock for resource"""
        return await self.redis.set(
            f"lock:{resource_id}",
            "1",
            ex=self.lock_timeout,
            nx=True
        )
        
    async def release_lock(self, resource_id: str):
        """Release distributed lock"""
        await self.redis.delete(f"lock:{resource_id}") 