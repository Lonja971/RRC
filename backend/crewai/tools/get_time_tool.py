from typing import Optional
import pytz
from dotenv import load_dotenv

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool

from datetime import datetime

load_dotenv()
user_answer = None

# ---TOOL---


class GetTimeTool(BaseTool):
    """Tool that will help determine the current time."""
    
    name: str = "get_time_tool"
    description: str = (
        "With the help of this tool, you can determine the current time."
    )

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the get_time_tool tool."""
        
        netherlands_timezone = pytz.timezone("Europe/Amsterdam")
        current_time = datetime.now(netherlands_timezone).strftime("%Y-%m-%dT%H:%M:%S.%f%z")

        return current_time