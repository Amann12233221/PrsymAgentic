from typing import Dict, List, Any
import time
from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class PerformanceMetrics:
    task_completion_time: float
    success_rate: float
    error_rate: float
    resource_usage: Dict[str, float]

class AdvancedMetricsCollector:
    def __init__(self):
        self.metrics_store = []
        self.start_times: Dict[str, float] = {}
        self.performance_history: Dict[str, List[PerformanceMetrics]] = {}

    def start_task_monitoring(self, task_id: str, agent_id: str):
        self.start_times[task_id] = time.time()

    def end_task_monitoring(self, task_id: str, agent_id: str, result: Dict[str, Any]):
        duration = time.time() - self.start_times[task_id]
        
        metrics = {
            'task_id': task_id,
            'agent_id': agent_id,
            'duration': duration,
            'timestamp': datetime.now(),
            'success': result.get('status') == 'completed',
            'error': result.get('error', None),
        }
        
        self.metrics_store.append(metrics)

    def get_agent_performance(self, agent_id: str) -> PerformanceMetrics:
        agent_metrics = [m for m in self.metrics_store if m['agent_id'] == agent_id]
        
        if not agent_metrics:
            return PerformanceMetrics(0.0, 0.0, 0.0, {'cpu': 0.0, 'memory': 0.0})
        
        total_tasks = len(agent_metrics)
        successful_tasks = sum(1 for m in agent_metrics if m['success'])
        error_tasks = sum(1 for m in agent_metrics if m['error'] is not None)
        avg_duration = sum(m['duration'] for m in agent_metrics) / total_tasks
        
        return PerformanceMetrics(
            task_completion_time=avg_duration,
            success_rate=successful_tasks / total_tasks,
            error_rate=error_tasks / total_tasks,
            resource_usage={'cpu': 0.5, 'memory': 0.3}  # Example values
        )

    def generate_performance_report(self) -> Dict[str, Any]:
        if not self.metrics_store:
            return {
                'overall_success_rate': 0.0,
                'average_task_duration': 0.0,
                'total_tasks_processed': 0,
                'agent_performances': {}
            }

        total_tasks = len(self.metrics_store)
        successful_tasks = sum(1 for m in self.metrics_store if m['success'])
        
        # Group by agent
        agent_metrics = defaultdict(list)
        for metric in self.metrics_store:
            agent_metrics[metric['agent_id']].append(metric)
            
        agent_performances = {}
        for agent_id, metrics in agent_metrics.items():
            agent_performances[agent_id] = {
                'duration': sum(m['duration'] for m in metrics) / len(metrics),
                'success': sum(1 for m in metrics if m['success']) / len(metrics)
            }

        return {
            'overall_success_rate': successful_tasks / total_tasks,
            'average_task_duration': sum(m['duration'] for m in self.metrics_store) / total_tasks,
            'total_tasks_processed': total_tasks,
            'agent_performances': agent_performances
        } 