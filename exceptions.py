class AgentError(Exception):
    """Base exception for agent-related errors"""
    pass

class WorkflowError(Exception):
    """Base exception for workflow-related errors"""
    pass

class TaskError(Exception):
    """Base exception for task-related errors"""
    pass 