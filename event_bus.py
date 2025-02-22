from typing import Dict, List, Callable
from collections import defaultdict

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        
    def subscribe(self, topic: str, callback: Callable) -> None:
        self._subscribers[topic].append(callback)
        
    def publish(self, topic: str, data: dict) -> None:
        for callback in self._subscribers[topic]:
            callback(data) 