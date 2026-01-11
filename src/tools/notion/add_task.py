import os
from enum import Enum
from langsmith import traceable
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from notion_client import Client

class TaskStatus(Enum):
    NOT_STARTED = "Not started"
    IN_PROGRESS = "In progress"
    COMPLETED = "Done"

class AddTaskInTodoListInput(BaseModel):
    task: str = Field(description="Task to be added")
    date: str = Field(description="Date and time for the task (YYYY-MM-DD) (HH:MM)")

@tool("AddTaskInTodoList", args_schema=AddTaskInTodoListInput)
@traceable(run_type="tool", name="AddTaskInTodoList")
def add_task_in_todo_list(task: str, date: str):
    """Use this to add a new task to my todo list"""
    try:
        notion = Client(auth=os.getenv("NOTION_TOKEN"))

        properties = {
            # ✅ Title property
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": task
                        }
                    }
                ]
            },

            # ✅ Status property
            "Completion Status": {
                "status": {
                    "name": TaskStatus.NOT_STARTED.value
                }
            }
        }

        # ✅ Optional due date
        if date:
            properties["Due Date"] = {
                "date": {
                    "start": date
                }
            }

        notion.pages.create(
            parent={"database_id": os.getenv("NOTION_DATABASE_ID")},
            properties=properties
        )

        return {
            "message": "Task added successfully",
            "task": task,
            "due_date": date,
            "status": TaskStatus.NOT_STARTED.value
        }

    except Exception as e:
        return f"An error occurred: {str(e)}"