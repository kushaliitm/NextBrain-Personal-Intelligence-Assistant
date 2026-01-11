import os
from datetime import datetime
from langsmith import traceable
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from notion_client import Client


class GetMyTodoListInput(BaseModel):
    date: str = Field(description="Date for which to retrieve tasks (YYYY-MM-DD)")

@tool("GetMyTodoList", args_schema=GetMyTodoListInput)
@traceable(run_type="tool", name="GetMyTodoList")
def get_my_todo_list(date: str):
    """Use this to get all tasks from my todo list"""
    try:
        # Validate date format
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."

        notion = Client(auth=os.getenv("NOTION_TOKEN"))

        # ✅ Correct filter: Due Date
        filter_params = {
            "filter": {
                "property": "Due Date",
                "date": {
                    "equals": date
                }
            }
        }

        results = notion.databases.query(
            database_id=os.getenv("NOTION_DATABASE_ID"),
            **filter_params
        )

        tasks = []

        for page in results["results"]:
            props = page["properties"]

            task = {
                "id": page["id"],
                "title": (
                    props["Name"]["title"][0]["plain_text"]
                    if props["Name"]["title"]
                    else None
                ),
                "status": (
                    props["Completion Status"]["status"]["name"]
                    if props["Completion Status"]["status"]
                    else None
                ),
                "priority": (
                    props["Priority Level"]["select"]["name"]
                    if props["Priority Level"]["select"]
                    else None
                ),
                "assigned_to": [
                    person["name"]
                    for person in props["Assigned To"]["people"]
                ],
                "due_date": (
                    props["Due Date"]["date"]["start"]
                    if props["Due Date"]["date"]
                    else None
                ),
                "url": page["url"]
            }

            tasks.append(task)

        if not tasks:
            return f"No tasks found for {date}."

        return {
            "date": date,
            "total_tasks": len(tasks),
            "tasks": tasks
        }

    except Exception as e:
        return f"An error occurred: {str(e)}"