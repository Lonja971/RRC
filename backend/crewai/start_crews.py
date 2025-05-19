from flask import Blueprint, jsonify, request
from crews.story_builder_crew import StoryBuilderCrew
from crews.tasks_planner_crew import TasksPlannerCrew
import json, os, requests, time
from datetime import datetime, timezone
import global_vars
#from docx import Document
from constants import MESSAGE_TYPES

def extract_raw_values(data):
    """Extracting raw data from kickoff_for_each crew responses."""

    combined_tasks = []
    message = {
        "status": "success",
        "data": []
    }
    
    for item in data:
        if hasattr(item, 'raw'):
            raw_data = item.raw
            
            if isinstance(raw_data, str):
                raw_data = raw_data.replace("```json", "").replace("```", "")
                try:
                    raw_data = json.loads(raw_data)
                except json.JSONDecodeError:
                    message["status"] = "error"
                    message["data"] = {
                        "type": MESSAGE_TYPES["error_message"],
                        "from": "Error interpreter (Tasks Planner Crew)",
                        "data": f"**Error:** Expected a list but got: {type(data)}"
                    }
                    return message

            if isinstance(raw_data, list):
                combined_tasks.extend(raw_data)
            else:
                raise ValueError(f"Expected list in raw but got it: {type(raw_data)}")
            
    message["data"] = combined_tasks
    return message

def send_message(type, from_who, data):
    """Send message to UI"""

    message = {
        "type": type,
        "from": from_who,
        "data": data
    }
    requests.get(f'{os.getenv("FLASK_BASE")}{os.getenv("FLASK_RETURN_ANSWER_API")}', json=message)

def get_from_txt(file_name):
    """Get data from TXT document."""

    with open(f'../data/{file_name}.txt', 'r', encoding='utf-8') as file:
        data = file.read()
        return data

def save_in_txt(data, file_name):
    """Save the data in a TXT document."""

    with open(f'../data/{file_name}.txt', 'a') as file:
        file.write(str(data))
        file.write("\n")

def save_in_docx(data):
    """Save the data in a new Word document."""

    way = "../data/"

    if not os.path.exists(way):
        os.makedirs(way)

    document = Document()

    current_time = datetime.now().strftime("%Y%m%d%H%M%S%f")
    file_name = f"result_{current_time}.docx"

    try:
        if isinstance(data, (dict, list)):
            formatted_data = json.dumps(data, indent=4)
            data = formatted_data
        elif isinstance(data, str):
            try:
                data_json = json.loads(data)
                formatted_data = json.dumps(data_json, indent=4)
                data = formatted_data
            except json.JSONDecodeError:
                pass
        else:
            raise ValueError("The data type is not supported.")

        if isinstance(data, list):
            for line in data:
                document.add_paragraph(line)
        else:
            document.add_paragraph(str(data))
    
    except Exception as e:
        raise ValueError(f"Data processing error: {e}")
    
    document.save(f"{way}{file_name}")
    return file_name

def json_to_markdown(json_input):
    """Convert JSON object or string into Markdown."""

    if isinstance(json_input, str):
        try:
            json_obj = json.loads(json_input)
        except json.JSONDecodeError as e:
            return f"Error: Invalid JSON string provided. Details: {e}"
    else:
        json_obj = json_input

    def format_issue(issue, is_last=False):
        """Formats a single issue into Markdown."""
        description = issue.get("description", "").strip()
        formatted = (
            f"### {issue.get('summary', 'No Summary')}\n"
            f"- **Status:** {issue.get('status', 'Unknown')}\n"
            f"- **Issue Type:** {issue.get('issueType', 'Unknown')}\n"
            f"- **Created:** {issue.get('created', 'Unknown')}\n"
            f"- **Updated:** {issue.get('updated', 'Unknown')}\n"
            f"- **External ID:** `{issue.get('externalId', 'Unknown')}`\n\n"
            f"**Description:**\n\n"
            f"{description}\n"
        )
        if not is_last:
            formatted += "\n---\n"
        return formatted

    markdown = []
    projects = json_obj.get("projects", [])
    for project in projects:
        markdown.append(f"## {project.get('name', 'Unnamed Project')}\n")
        markdown.append(f"- **Key:** `{project.get('key', 'Unknown')}`\n")
        markdown.append(f"- **Type:** `{project.get('type', 'Unknown')}`\n")
        markdown.append(f"- **Description:** {project.get('description', 'No description.')}\n")
        markdown.append("\n---\n")

        issues = project.get("issues", [])
        for idx, issue in enumerate(issues):
            is_last = idx == len(issues) - 1
            markdown.append(format_issue(issue, is_last))
    
    return "\n".join(markdown)

def update_tasks_data(data):
    """
    A function to update all required fields of the Final Answer.
    update_id - updates the values ​​of all ids to make them consistent.
    """

    if isinstance(data, str):
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError as e:
            return f"Error: Invalid JSON string provided. Details: {e}"
    else:
        json_data = data
    
    def update_id(data):
        if "projects" in data and len(data["projects"]) > 0:
            issues = data["projects"][0]["issues"]
            starting_id = 1

            for issue in issues:
                issue["externalId"] = str(starting_id)
                starting_id += 1

        return data

    data = update_id(json_data)

    return data


def start_crew_function(query):
    global_vars.CHAT_STATUS = "crew_working"
    message = {
        "type": None,
        "from": "",
        "data": "",
        "file_name": "",
    }
    main_inputs = {
        'query': query,
    }

    #---STORY-BUILDER-CREW---

    story_builder_result = StoryBuilderCrew().crew().kickoff(inputs=main_inputs)
    story_builder_result = story_builder_result.raw
    story_builder_result = story_builder_result.replace("```json", "").replace("```", "")

    #story_builder_result = get_from_txt("story_builder_json_example")

    story_builder_result_markdown = f"```json\n{story_builder_result}\n```"
    send_message(MESSAGE_TYPES["final_answer"], "Main Crew (Final Answer)", story_builder_result_markdown)
    time.sleep(1)

    try:
        story_builder_result_json = json.loads(story_builder_result)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        message["type"] = MESSAGE_TYPES["error_message"]
        message["from"] = "Error interpreter (Story Builder Crew)"
        message["data"] = f"**Error:** The generated response from **'Story Builder Crew'** was not correctly converted to a JSON element!\n\n---\n\n**Last reply by 'Story Builder Crew':** \n\n{story_builder_result}"
        return message
    
    #---TASKS-PLANNER-CREW---

    project_block_array = story_builder_result_json['projects']
    user_stories_array = story_builder_result_json['user_stories']

    task_planner_result = TasksPlannerCrew().crew().kickoff_for_each(inputs=user_stories_array)

    task_planner_result = extract_raw_values(task_planner_result)

    if task_planner_result["status"] != "success":
        message["type"] = task_planner_result["data"]["type"]
        message["from"] = task_planner_result["data"]["from"]
        message["data"] = task_planner_result["data"]["data"]
        print(f"\n\n--message")
        print(f"{message}")
        print(f"\n\n")
        return message
    else:
        task_planner_json = task_planner_result["data"]
    
    #---PREPARATION-OF-THE-FINAL-RESULT---

    final_answer = project_block_array.copy()
    final_answer["projects"][0]["issues"] = task_planner_json
    final_answer = json.dumps(final_answer, indent=4)
    final_answer = update_tasks_data(final_answer)

    #file_name = save_in_docx(final_answer)

    final_markdown = json_to_markdown(final_answer)

    active_crew = "Sub-Crew"
    message["type"] = MESSAGE_TYPES["final_answer"]
    message["from"] = f"{active_crew} (Final Result)"
    message["data"] = final_markdown
    #message["file_name"] = file_name

    return message