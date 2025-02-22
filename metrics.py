from typing import Dict, List
from collections import defaultdict
from datetime import datetime
import json

class MetricsCollector:
    def __init__(self):
        self.metrics: Dict[str, List[Dict]] = defaultdict(list)
        
    def record_execution(self, agent_id: str, task_id: str) -> None:
        """Record task execution metrics"""
        self.metrics[agent_id].append({
            'task_id': task_id,
            'timestamp': datetime.now().isoformat(),
            'status': 'completed'
        })
        
    def get_agent_metrics(self, agent_id: str) -> List[Dict]:
        """Get metrics for specific agent"""
        return self.metrics.get(agent_id, [])
        
    def export_metrics(self, file_path: str) -> None:
        """Export metrics to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(self.metrics, f, indent=2) 