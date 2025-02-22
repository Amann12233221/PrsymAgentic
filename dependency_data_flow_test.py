import asyncio
from src.core.enhanced_orchestrator import EnhancedOrchestrator
from rich import print
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree
from datetime import datetime

console = Console()

async def main():
    config = {
        'cache_url': 'redis://localhost:6379/0',
        'queue_url': 'redis://localhost:6379/1',
        'redis_url': 'redis://localhost:6379/2'
    }
    
    orchestrator = EnhancedOrchestrator(config)
    
    # Workflow with data sharing and fragmentation details
    workflow = {
        'id': 'dependency_workflow',
        'tasks': [
            {
                'id': 'text_analysis',
                'agent_id': 'openai_agent',
                'data': {
                    'prompt': 'Analyze the technical requirements for a cloud system'
                },
                'dependencies': [],
                'output_schema': {
                    'type': 'technical_analysis',
                    'fragments': ['system_requirements', 'technical_constraints', 'performance_metrics']
                }
            },
            {
                'id': 'requirements_processing',
                'agent_id': 'anthropic_agent',
                'data': {
                    'input': 'Convert technical analysis into system requirements'
                },
                'dependencies': ['text_analysis'],
                'required_fragments': ['system_requirements', 'technical_constraints'],
                'output_schema': {
                    'type': 'system_requirements',
                    'fragments': ['functional_requirements', 'non_functional_requirements']
                }
            },
            {
                'id': 'architecture_design',
                'agent_id': 'openai_agent',
                'data': {
                    'prompt': 'Design system architecture based on requirements'
                },
                'dependencies': ['requirements_processing'],
                'required_fragments': ['functional_requirements', 'performance_metrics'],
                'output_schema': {
                    'type': 'architecture_design',
                    'fragments': ['system_components', 'interaction_patterns']
                }
            }
        ]
    }
    
    try:
        console.print("\n[bold blue]Starting Workflow Execution with Data Flow Analysis[/bold blue]")
        console.print("="* 60)

        # Display task dependencies
        deps_table = Table(title="Task Dependencies and Data Requirements")
        deps_table.add_column("Task ID", style="cyan")
        deps_table.add_column("Agent", style="green")
        deps_table.add_column("Depends On", style="yellow")
        deps_table.add_column("Required Data Fragments", style="magenta")
        deps_table.add_column("Produces Fragments", style="blue")

        for task in workflow['tasks']:
            deps_table.add_row(
                task['id'],
                task['agent_id'],
                ", ".join(task['dependencies']) if task['dependencies'] else "None",
                ", ".join(task.get('required_fragments', [])) or "None",
                ", ".join(task['output_schema']['fragments'])
            )

        console.print(deps_table)
        console.print("\n[bold]Executing Workflow with Data Flow Tracking...[/bold]\n")

        # Track data sharing
        data_flow = {}
        
        results = await orchestrator.execute_workflow(workflow)
        
        # Display results with data flow context
        for result in results:
            task_id = result.get('task_id')
            task_info = next(t for t in workflow['tasks'] if t['id'] == task_id)
            
            # Track data fragments
            data_flow[task_id] = {
                'produced': task_info['output_schema']['fragments'],
                'consumed': task_info.get('required_fragments', []),
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            
            panel_content = f"""
[bold cyan]Task ID:[/bold cyan] {task_id}
[bold green]Agent:[/bold green] {task_info['agent_id']}
[bold yellow]Dependencies:[/bold yellow] {', '.join(task_info['dependencies']) if task_info['dependencies'] else 'None'}

[bold magenta]Data Flow:[/bold magenta]
├── Required Fragments: {', '.join(task_info.get('required_fragments', ['None']))}
├── Produced Fragments: {', '.join(task_info['output_schema']['fragments'])}
└── Processing Time: {data_flow[task_id]['timestamp']}

[bold white]Status:[/bold white] {result.get('status')}

[bold]Response:[/bold]
{result.get('response')}
            """
            
            console.print(Panel(
                panel_content,
                title=f"Task Execution Result: {task_id}",
                border_style="blue"
            ))
            
        # Display data sharing metrics
        data_sharing_tree = Tree("[bold]Data Fragment Flow Analysis[/bold]")
        for task_id, flow_data in data_flow.items():
            task_node = data_sharing_tree.add(f"[cyan]{task_id}[/cyan]")
            task_node.add(f"[green]Produced:[/green] {', '.join(flow_data['produced'])}")
            if flow_data['consumed']:
                task_node.add(f"[yellow]Consumed:[/yellow] {', '.join(flow_data['consumed'])}")
            task_node.add(f"[blue]Timestamp:[/blue] {flow_data['timestamp']}")

        console.print("\n[bold]Data Sharing Analysis[/bold]")
        console.print(data_sharing_tree)
            
        # Display enhanced performance metrics
        metrics_panel = f"""
[bold cyan]Total Tasks:[/bold cyan] {len(results)}
[bold green]Successful Tasks:[/bold green] {sum(1 for r in results if r.get('status') == 'completed')}
[bold yellow]Total Execution Time:[/bold yellow] {sum(r.get('execution_time', 0) for r in results)}s
[bold magenta]Data Fragments Shared:[/bold magenta] {sum(len(f['produced']) for f in data_flow.values())}
[bold blue]Data Fragment Dependencies:[/bold blue] {sum(len(f['consumed']) for f in data_flow.values())}
        """
        
        console.print(Panel(
            metrics_panel,
            title="Performance Metrics",
            border_style="green"
        ))
            
    except Exception as e:
        console.print(f"[bold red]Error executing workflow:[/bold red] {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 