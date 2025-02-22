import asyncio
from src.core.enhanced_orchestrator import EnhancedOrchestrator
from rich import print
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

console = Console()

async def main():
    config = {
        'cache_url': 'redis://localhost:6379/0',
        'queue_url': 'redis://localhost:6379/1',
        'redis_url': 'redis://localhost:6379/2'
    }
    
    orchestrator = EnhancedOrchestrator(config)
    
    # Workflow with clear dependencies
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
                'output_schema': {'type': 'technical_analysis'}
            },
            {
                'id': 'requirements_processing',
                'agent_id': 'anthropic_agent',
                'data': {
                    'input': 'Convert technical analysis into system requirements'
                },
                'dependencies': ['text_analysis'],
                'output_schema': {'type': 'system_requirements'}
            },
            {
                'id': 'architecture_design',
                'agent_id': 'openai_agent',
                'data': {
                    'prompt': 'Design system architecture based on requirements'
                },
                'dependencies': ['requirements_processing'],
                'output_schema': {'type': 'architecture_design'}
            }
        ]
    }
    
    try:
        console.print("\n[bold blue]Starting Workflow Execution with Dependencies[/bold blue]")
        console.print("="* 50)

        # Display dependency graph
        table = Table(title="Task Dependencies")
        table.add_column("Task ID", style="cyan")
        table.add_column("Agent", style="green")
        table.add_column("Depends On", style="yellow")
        table.add_column("Output Type", style="magenta")

        for task in workflow['tasks']:
            table.add_row(
                task['id'],
                task['agent_id'],
                ", ".join(task['dependencies']) if task['dependencies'] else "None",
                task['output_schema']['type']
            )

        console.print(table)
        console.print("\n[bold]Executing Workflow...[/bold]\n")

        results = await orchestrator.execute_workflow(workflow)
        
        # Display results with dependency context
        for result in results:
            task_id = result.get('task_id')
            task_info = next(t for t in workflow['tasks'] if t['id'] == task_id)
            
            panel_content = f"""
[bold cyan]Task ID:[/bold cyan] {task_id}
[bold green]Agent:[/bold green] {task_info['agent_id']}
[bold yellow]Dependencies:[/bold yellow] {', '.join(task_info['dependencies']) if task_info['dependencies'] else 'None'}
[bold magenta]Output Type:[/bold magenta] {task_info['output_schema']['type']}
[bold white]Status:[/bold white] {result.get('status')}

[bold]Response:[/bold]
{result.get('response')}
            """
            
            console.print(Panel(
                panel_content,
                title=f"Task Execution Result: {task_id}",
                border_style="blue"
            ))
            
        # Display performance metrics
        metrics_panel = f"""
[bold cyan]Total Tasks:[/bold cyan] {len(results)}
[bold green]Successful Tasks:[/bold green] {sum(1 for r in results if r.get('status') == 'completed')}
[bold yellow]Total Execution Time:[/bold yellow] {sum(r.get('execution_time', 0) for r in results)}s
[bold magenta]Data Transformations:[/bold magenta] {len(workflow['tasks']) - 1}
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