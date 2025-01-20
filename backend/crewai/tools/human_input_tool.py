from typing import Callable, Optional
import os, json, requests, time
from dotenv import load_dotenv

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import Field
from langchain_core.tools import BaseTool
import global_vars

from flask import jsonify, request

load_dotenv()
user_answer = None

def submit_answer(answer):
    global user_answer
    user_answer = answer
    return jsonify({'status': 'success'}), 200

# ---TOOL---


class HumanInput(BaseTool):
    """Tool that asks user for input."""
    
    name: str = "human"
    description: str = (
        "Je kunt een mens om leiding vragen als je denkt dat je dat bent"
        "vastgelopen of u weet niet zeker wat u nu moet doen."
        "De input moet een vraag voor de mens zijn."
        "Stel de gebruiker een vraag in het Nederlands."
    )

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human input tool."""
        
        global user_answer

        message = {
            "type": "message",
            "from": "assistant",
            "data": query
        }
        response = requests.get(f'{os.getenv("FLASK_BASE")}{os.getenv("FLASK_RETURN_ANSWER_API")}', json=message)

        if response.status_code == 200:
            global_vars.CHAT_STATUS = 'user_answer'
            print(f'\n--Human input tool question: {query}\n')
        else:
            print(f"Human_tool Error: Received status code {response.status_code}")
            print(f"Human_tool Response content: {response.content}")

        while user_answer is None:
            time.sleep(0.1)

        result = user_answer
        user_answer = None
        return result