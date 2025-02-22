import asyncio
from datetime import datetime
from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.syntax import Syntax
from rich.markdown import Markdown

console = Console()

# Simulated agent responses
MOCK_RESPONSES = {
    'text_analysis': {
        'fragments': {
            'system_requirements': """
                - High availability (99.99% uptime)
                - Scalable to 1M concurrent users
                - Low latency (<100ms response time)
            """,
            'technical_constraints': """
                - AWS Cloud Infrastructure
                - Kubernetes orchestration
                - Microservices architecture
            """,
            'performance_metrics': """
                - CPU utilization < 70%
                - Memory usage < 80%
                - Network bandwidth: 10Gbps
            """
        },
        'metadata': {
            'confidence': 0.95,
            'processing_time': '1.2s',
            'model': 'gpt-4-turbo'
        }
    },
    'requirements_processing': {
        'fragments': {
            'functional_requirements': """
                1. User Authentication System
                2. Real-time Data Processing
                3. API Gateway Integration
                4. Load Balancing System
            """,
            'non_functional_requirements': """
                1. Security Compliance (SOC2, GDPR)
                2. Disaster Recovery Plan
                3. Performance Optimization
                4. Monitoring & Alerting
            """
        },
        'metadata': {
            'confidence': 0.88,
            'processing_time': '1.5s',
            'model': 'claude-2'
        }
    },
    'architecture_design': {
        'fragments': {
            'component_diagram': """
                [Frontend] ←→ [API Gateway]
                    ↓           ↓
                [Auth] ←→ [Microservices]
                    ↓           ↓
                [Cache] ←→ [Database]
            """,
            'deployment_model': """
                - Multi-region deployment
                - Auto-scaling groups
                - Container orchestration
                - Service mesh topology
            """
        },
        'metadata': {
            'confidence': 0.92,
            'processing_time': '1.8s',
            'model': 'gpt-4-turbo'
        }
    }
}

async def simulate_task_execution(task_id: str, delay: float = 1.0) -> dict:
    """Simulate task execution with mock responses"""
    await asyncio.sleep(delay)
    return {
        'task_id': task_id,
        'status': 'completed',
        'response': MOCK_RESPONSES[task_id],
        'execution_time': delay,
        'timestamp': datetime.now().isoformat()
    }

async def main():
    console.print("\n[bold blue]Advanced Multi-Agent System Demo[/bold blue]")
    console.print("[bold blue]================================[/bold blue]\n")

    # Define workflow with detailed dependencies
    workflow = {
        'id': 'complex_system_design',
        'tasks': [
            {
                'id': 'text_analysis',
                'agent_id': 'openai_agent',
                'agent_type': 'LLM',
                'capability': ['technical_analysis', 'requirement_extraction'],
                'dependencies': [],
                'output_schema': {
                    'type': 'technical_analysis',
                    'fragments': ['system_requirements', 'technical_constraints', 'performance_metrics']
                },
                'shared_with': ['requirements_processing'],
                'priority': 1
            },
            {
                'id': 'requirements_processing',
                'agent_id': 'anthropic_agent',
                'agent_type': 'LLM',
                'capability': ['requirement_analysis', 'system_design'],
                'dependencies': [{
                    'task_id': 'text_analysis',
                    'required_fragments': ['system_requirements', 'technical_constraints'],
                    'data_transform': 'technical_to_requirements',
                    'transform_rules': ['normalize', 'categorize', 'prioritize']
                }],
                'output_schema': {
                    'type': 'system_requirements',
                    'fragments': ['functional_requirements', 'non_functional_requirements']
                },
                'shared_with': ['architecture_design'],
                'priority': 2
            },
            {
                'id': 'architecture_design',
                'agent_id': 'openai_agent',
                'agent_type': 'LLM',
                'capability': ['system_architecture', 'deployment_planning'],
                'dependencies': [{
                    'task_id': 'requirements_processing',
                    'required_fragments': ['functional_requirements', 'non_functional_requirements'],
                    'data_transform': 'requirements_to_architecture',
                    'transform_rules': ['component_mapping', 'dependency_analysis']
                }],
                'output_schema': {
                    'type': 'architecture_design',
                    'fragments': ['component_diagram', 'deployment_model']
                },
                'shared_with': [],
                'priority': 3
            }
        ]
    }

    # Display initial workflow analysis
    console.print("[bold green]Workflow Analysis[/bold green]")
    console.print("─" * 50)

    # Agent Capabilities Table
    capability_table = Table(title="Agent Capabilities")
    capability_table.add_column("Agent ID", style="cyan")
    capability_table.add_column("Type", style="yellow")
    capability_table.add_column("Capabilities", style="green")
    capability_table.add_column("Priority", style="magenta")

    for task in workflow['tasks']:
        capability_table.add_row(
            task['agent_id'],
            task['agent_type'],
            ", ".join(task['capability']),
            str(task['priority'])
        )

    console.print(capability_table)
    console.print("\n")

    # Data Flow Diagram
    flow_table = Table(title="Data Flow and Dependencies")
    flow_table.add_column("Stage", style="cyan")
    flow_table.add_column("Input", style="yellow")
    flow_table.add_column("Transformation", style="green")
    flow_table.add_column("Output", style="magenta")
    flow_table.add_column("Consumers", style="blue")

    for task in workflow['tasks']:
        input_data = "Initial Input" if not task['dependencies'] else \
                    "\n".join(f"- {d['task_id']}: {', '.join(d['required_fragments'])}" 
                             for d in task['dependencies'])
        
        transform = "None" if not task['dependencies'] else \
                   "\n".join(f"- {d['data_transform']}\n  Rules: {', '.join(d['transform_rules'])}" 
                            for d in task['dependencies'])
        
        flow_table.add_row(
            task['id'],
            input_data,
            transform,
            "\n".join(task['output_schema']['fragments']),
            "\n".join(task['shared_with']) if task['shared_with'] else "None"
        )

    console.print(flow_table)
    console.print("\n")

    # Execute workflow with progress tracking
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        progress.add_task("[cyan]Executing workflow...", total=None)
        
        results = []
        for task in workflow['tasks']:
            result = await simulate_task_execution(
                task['id'], 
                delay=float(task['priority'])
            )
            results.append(result)
            
            # Display detailed task result
            task_panel = Panel(
                f"""[bold cyan]Task ID:[/bold cyan] {task['id']}
[bold yellow]Agent:[/bold yellow] {task['agent_id']} ({task['agent_type']})
[bold green]Status:[/bold green] {result['status']}
[bold magenta]Execution Time:[/bold magenta] {result['execution_time']}s

[bold]Data Fragments:[/bold]
{Syntax(str(result['response']['fragments']), 'yaml', theme='monokai')}

[bold]Metadata:[/bold]
{Syntax(str(result['response']['metadata']), 'yaml', theme='monokai')}

[bold]Dependencies:[/bold]
{Syntax(str(task.get('dependencies', [])), 'yaml', theme='monokai')}
""",
                title=f"Task Execution Result: {task['id']}",
                border_style="blue"
            )
            console.print(task_panel)
            console.print("\n")

    # Display final metrics
    metrics_panel = Panel(
        f"""[bold cyan]Workflow Metrics:[/bold cyan]
- Total Tasks: {len(results)}
- Total Execution Time: {sum(r['execution_time'] for r in results):.2f}s
- Average Task Time: {sum(r['execution_time'] for r in results)/len(results):.2f}s

[bold yellow]Data Metrics:[/bold yellow]
- Total Data Fragments: {sum(len(task['output_schema']['fragments']) for task in workflow['tasks'])}
- Data Transformations: {sum(len(task['dependencies']) for task in workflow['tasks'])}
- Fragment Sharing Events: {sum(len(task['shared_with']) for task in workflow['tasks'])}

[bold green]Agent Performance:[/bold green]
- OpenAI Agent Tasks: {sum(1 for task in workflow['tasks'] if task['agent_id'] == 'openai_agent')}
- Anthropic Agent Tasks: {sum(1 for task in workflow['tasks'] if task['agent_id'] == 'anthropic_agent')}
- Average Confidence: {sum(r['response']['metadata']['confidence'] for r in results)/len(results):.2%}
""",
        title="Final Workflow Metrics",
        border_style="green"
    )
    console.print(metrics_panel)

if __name__ == "__main__":
    asyncio.run(main()) 