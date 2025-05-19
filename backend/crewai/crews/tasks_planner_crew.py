import os, requests, json
from typing import Union, List, Tuple, Dict
from dotenv import load_dotenv
from constants import MESSAGE_TYPES

# CREWAI
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.telemetry import Telemetry
from crewai.agents.parser import AgentAction, AgentFinish

#TOOLS
from tools.human_input_tool import HumanInput
from tools.get_time_tool import GetTimeTool

#LLM
from config.llm import llm


#---BASE---

load_dotenv()

#---LLM---

@CrewBase
class TasksPlannerCrew():

	def step_callback(self, agent_output: Union[str, List[Tuple[Dict, str]], AgentFinish], agent_name, *args):
		step_callback_info = ""
		step_callback_extra_info = ""
		agent = ""
	
		if isinstance(agent_output, str):
			try:
				agent_output = json.loads(agent_output)
			except json.JSONDecodeError:
				pass
	
		if isinstance(agent_output, AgentAction):
			agent_output = [(agent_output, "Unknown description")]
			for action, description in agent_output:
				step_callback_info += f"**Agent Name**: {agent_name}\n\n"
				agent = agent_name
				step_callback_info += f"**Thought**: {getattr(action, 'thought', 'Unknown')}\n\n"
				step_callback_extra_info += f"**Tool used**: {getattr(action, 'tool', 'Unknown')}\n\n"
				step_callback_extra_info += f"**Tool input**: {getattr(action, 'tool_input', 'Unknown')}\n\n"
				step_callback_extra_info += "\n**Log**:\n\n"
				step_callback_extra_info += f"{getattr(action, 'text', 'Unknown')}\n\n"
	
		elif isinstance(agent_output, list) and all(isinstance(item, tuple) for item in agent_output):
			for action, description in agent_output:
				step_callback_info += f"**Agent Name**: {agent_name}\n\n"
				agent = agent_name
				step_callback_info += f"**Thought**: {getattr(action, 'thought', 'Unknown')}\n\n"
				step_callback_extra_info += f"**Tool used**: {getattr(action, 'tool', 'Unknown')}\n\n"
				step_callback_extra_info += f"**Tool input**: {getattr(action, 'tool_input', 'Unknown')}\n\n"
				step_callback_extra_info += "\n**Log**:\n\n"
				step_callback_extra_info += f"{getattr(action, 'text', 'Unknown')}\n\n"
	
		else:
			step_callback_info += f"unexpected_type: {agent_output}"
			step_callback_info += f"unexpected_output: {agent_output}\n\n"
	
		final_info = step_callback_info.strip()
		final_extra_info = step_callback_extra_info.strip()
		message = {
						"type": MESSAGE_TYPES["step_callback"],
            "from": f"{agent} (Step Callback)",
            "data": {
							"info": final_info,
							"extra_info": final_extra_info
						}
        }
		requests.get(f'{os.getenv("FLASK_BASE")}{os.getenv("FLASK_RETURN_ANSWER_API")}', json=message)



	"""TestRagCrew crew"""
	agents_config = '../config/agents.yaml'
	tasks_config = '../config/tasks.yaml'

	def __init__(self) -> None:
		self.llm = llm

	@agent
	def search_agent(self) -> Agent:
		return Agent(
			config = self.agents_config['developer'],
			llm = self.llm,
            step_callback=lambda step: self.step_callback(step, "Developer"),
		)

	@task
	def create_tasks(self) -> Task:
		return Task(
			config = self.tasks_config['developer_task'],
			agent = self.search_agent(),
			#tools=[
			#	HumanInput(),
		  	#	GetTimeTool()
			#],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the FinancialAnalystCrew crew"""
		return Crew(
			agents =  self.agents,
			tasks = self.tasks,
			process = Process.sequential,
			verbose = True
		)