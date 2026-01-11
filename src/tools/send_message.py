from typing import Optional, Type, Dict
from langchain_core.callbacks import CallbackManagerForToolRun
from langsmith import traceable
from pydantic import BaseModel
from langchain.tools import BaseTool
from src.agents.base import Agent


class SendMessage(BaseTool):
    name: str = "SendMessage"
    description: str = "Use this to send a message to one of your sub-agents"
    args_schema: Type[BaseModel]
    agent_mapping: Dict[str, "Agent"] = None 

    def send_message(self, recipient: str, message: str) -> str:
        agent = self.agent_mapping.get(recipient)
        if agent:
            try:
                # Use a unique thread_id for each sub-agent call to avoid checkpoint conflicts
                import time
                unique_thread_id = f"sub_{recipient}_{int(time.time() * 1000)}"
                sub_agent_config = {"configurable": {"thread_id": unique_thread_id}}
                
                response = agent.invoke({"messages": [("human", message)]}, config=sub_agent_config)
                
                # Extract the content properly
                if isinstance(response, dict) and "messages" in response:
                    last_message = response["messages"][-1]
                    if hasattr(last_message, "content"):
                        content = str(last_message.content)
                    elif isinstance(last_message, dict):
                        content = str(last_message.get("content", "No response"))
                    else:
                        content = str(last_message)
                elif hasattr(response, "content"):
                    content = str(response.content)
                else:
                    content = str(response)
                
                # Return formatted response
                return f"Response from {recipient}: {content}"
            except Exception as e:
                import traceback
                error_msg = f"Error communicating with {recipient}: {str(e)}"
                print(f"SendMessage error: {error_msg}")
                traceback.print_exc()
                return error_msg
        else:
            available = ', '.join(self.agent_mapping.keys()) if self.agent_mapping else "none"
            return f"Invalid recipient: {recipient}. Available recipients: {available}"

    @traceable(run_type="tool", name="SendMessage")
    def _run(
        self,
        recipient: str,
        message: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return self.send_message(recipient, message)