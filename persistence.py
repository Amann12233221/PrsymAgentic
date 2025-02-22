from typing import Dict, Any, List
import json
import sqlite3
from datetime import datetime
from ..core.interfaces import WorkflowData, TaskData

class WorkflowStorage:
    def __init__(self, db_path: str = "workflows.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS workflows (
                    workflow_id TEXT PRIMARY KEY,
                    agent_id TEXT,
                    created_at TIMESTAMP,
                    data JSON
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    workflow_id TEXT,
                    status TEXT,
                    created_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    data JSON,
                    FOREIGN KEY (workflow_id) REFERENCES workflows (workflow_id)
                )
            """)

    def save_workflow(self, workflow: WorkflowData, agent_id: str):
        with sqlite3.connect(self.db_path) as conn:
            # Check if workflow exists
            cursor = conn.execute(
                "SELECT workflow_id FROM workflows WHERE workflow_id = ?",
                (workflow.workflow_id,)
            )
            
            if cursor.fetchone():
                # Update existing workflow
                conn.execute(
                    """
                    UPDATE workflows 
                    SET data = ?, agent_id = ?, created_at = ?
                    WHERE workflow_id = ?
                    """,
                    (
                        json.dumps(workflow.__dict__),
                        agent_id,
                        datetime.now(),
                        workflow.workflow_id
                    )
                )
            else:
                # Insert new workflow
                conn.execute(
                    """
                    INSERT INTO workflows (workflow_id, agent_id, created_at, data)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        workflow.workflow_id,
                        agent_id,
                        datetime.now(),
                        json.dumps(workflow.__dict__)
                    )
                )

    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT data FROM workflows WHERE workflow_id = ?",
                (workflow_id,)
            )
            result = cursor.fetchone()
            return json.loads(result[0]) if result else None 