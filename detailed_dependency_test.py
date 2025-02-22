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
    
    # Enhanced workflow with data sharing and fragmentation details
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
                },
                'shared_with': ['requirements_processing']
            },
            {
                'id': 'requirements_processing',
                'agent_id': 'anthropic_agent',
                'data': {
                    'input': 'Convert technical analysis into system requirements'
                },
                'dependencies': [{
                    'task_id': 'text_analysis',
                    'required_fragments': ['system_requirements', 'technical_constraints'],
                    'data_transform': 'technical_to_requirements'
                }],
                'output_schema': {
                    'type': 'system_requirements',
                    'fragments': ['functional_requirements', 'non_functional_requirements']
                },
                'shared_with': ['architecture_design']
            },
            {
                'id': 'architecture_design',
                'agent_id': 'openai_agent',
                'data': {
                    'prompt': 'Design system architecture based on requirements'
                },
                'dependencies': [{
                    'task_id': 'requirements_processing',
                    'required_fragments': ['functional_requirements'],
                    'data_transform': 'requirements_to_architecture'
                }],
                'output_schema': {
                    'type': 'architecture_design',
                    'fragments': ['component_diagram', 'deployment_model']
                },
                'shared_with': []
            }
        ]
    }
    
    try:
        console.print("\n[bold blue]Starting Workflow Execution with Enhanced Dependencies[/bold blue]")
        console.print("="* 70)

        # Display dependency and data sharing graph
        table = Table(title="Task Dependencies and Data Sharing")
        table.add_column("Task ID", style="cyan")
        table.add_column("Agent", style="green")
        table.add_column("Input Dependencies", style="yellow")
        table.add_column("Output Fragments", style="magenta")
        table.add_column("Shared With", style="blue")

        for task in workflow['tasks']:
            deps = [f"{d['task_id']} ({', '.join(d['required_fragments'])})" 
                   for d in task['dependencies']] if isinstance(task['dependencies'], list) else []
            
            table.add_row(
                task['id'],
                task['agent_id'],
                "\n".join(deps) if deps else "None",
                "\n".join(task['output_schema']['fragments']),
                "\n".join(task['shared_with'])
            )

        console.print(table)
        console.print("\n[bold]Executing Workflow with Data Sharing...[/bold]\n")

        results = await orchestrator.execute_workflow(workflow)
        
        # Display detailed results with data sharing context
        for result in results:
            task_id = result.get('task_id')
            task_info = next(t for t in workflow['tasks'] if t['id'] == task_id)
            
            # Create dependency tree
            tree = Tree(f"[bold cyan]{task_id}[/bold cyan]")
            
            # Add input dependencies
            if isinstance(task_info['dependencies'], list) and task_info['dependencies']:
                deps_branch = tree.add("[bold yellow]Input Dependencies[/bold yellow]")
                for dep in task_info['dependencies']:
                    dep_details = deps_branch.add(f"[yellow]{dep['task_id']}[/yellow]")
                    dep_details.add(f"Required Fragments: {', '.join(dep['required_fragments'])}")
                    dep_details.add(f"Transform: {dep['data_transform']}")
            
            # Add output fragments
            fragments_branch = tree.add("[bold magenta]Output Fragments[/bold magenta]")
            for fragment in task_info['output_schema']['fragments']:
                fragments_branch.add(f"[magenta]{fragment}[/magenta]")
            
            # Add data sharing info
            if task_info['shared_with']:
                sharing_branch = tree.add("[bold blue]Shared With[/bold blue]")
                for target in task_info['shared_with']:
                    sharing_branch.add(f"[blue]{target}[/blue]")
            
            panel_content = f"""
[bold cyan]Task ID:[/bold cyan] {task_id}
[bold green]Agent:[/bold green] {task_info['agent_id']}
[bold white]Status:[/bold white] {result.get('status')}
[bold white]Execution Time:[/bold white] {result.get('execution_time', 0)}s

[bold]Dependency Tree:[/bold]
{tree}

[bold]Response:[/bold]
{result.get('response')}

[bold]Data Transformation Metrics:[/bold]
- Fragments Processed: {len(task_info['output_schema']['fragments'])}
- Data Transform Type: {task_info['dependencies'][0]['data_transform'] if isinstance(task_info['dependencies'], list) and task_info['dependencies'] else 'None'}
- Sharing Status: {'Shared with ' + ', '.join(task_info['shared_with']) if task_info['shared_with'] else 'Not shared'}
            """
            
            console.print(Panel(
                panel_content,
                title=f"Task Execution Result: {task_id}",
                border_style="blue"
            ))
            
        # Display enhanced performance metrics
        metrics_panel = f"""
[bold cyan]Task Metrics:[/bold cyan]
- Total Tasks: {len(results)}
- Successful Tasks: {sum(1 for r in results if r.get('status') == 'completed')}
- Total Execution Time: {sum(r.get('execution_time', 0) for r in results)}s

[bold yellow]Data Fragmentation Metrics:[/bold yellow]
- Total Data Fragments: {sum(len(t['output_schema']['fragments']) for t in workflow['tasks'])}
- Data Transformations: {sum(1 for t in workflow['tasks'] if isinstance(t['dependencies'], list) and t['dependencies'])}
- Fragment Sharing Events: {sum(len(t['shared_with']) for t in workflow['tasks'])}

[bold green]Efficiency Metrics:[/bold green]
- Average Task Time: {sum(r.get('execution_time', 0) for r in results)/len(results):.2f}s
- Fragment Reuse Rate: {sum(len(t['shared_with']) for t in workflow['tasks'])/len(workflow['tasks']):.2f}
        """
        
        console.print(Panel(
            metrics_panel,
            title="Enhanced Performance Metrics",
            border_style="green"
        ))
            
    except Exception as e:
        console.print(f"[bold red]Error executing workflow:[/bold red] {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 