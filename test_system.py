import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

import asyncio
from src.core.interfaces import TaskData
from main import OrchestrationSystem

async def run_test():
    system = OrchestrationSystem()
    
    # Create multiple tasks with different parameters
    tasks = [
        TaskData(
            task_id=f"test_task_{i}",
            task_type="text" if i % 2 == 0 else "data",
            parameters={"input": f"Test input {i}"},
            priority=i % 3 + 1
        ) for i in range(5)
    ]
    
    # Run the system
    await system.run_system()
    
    # Get detailed performance report
    report = system.metrics_collector.generate_performance_report()
    
    print("\nDetailed Performance Report:")
    print("-" * 50)
    print(f"Total Tasks Processed: {report['total_tasks_processed']}")
    print(f"Overall Success Rate: {report['overall_success_rate']*100}%")
    print(f"Average Task Duration: {report['average_task_duration']*1000:.2f}ms")
    print("\nAgent Performances:")
    for agent_id, perf in report['agent_performances'].items():
        print(f"\n{agent_id}:")
        print(f"  Average Duration: {perf['duration']*1000:.2f}ms")
        print(f"  Success Rate: {perf['success']*100}%")
    
    print("-" * 50)

if __name__ == "__main__":
    asyncio.run(run_test()) 