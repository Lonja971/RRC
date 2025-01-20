import os, json
from flask import Flask, jsonify, request, Blueprint, send_from_directory
from flask_cors import CORS
from tools.human_input_tool import submit_answer
from start_crews import start_crew_function
import global_vars
from dotenv import load_dotenv
load_dotenv()

print(f"--Active LLM : {os.getenv('OPENAI_MODEL_NAME')}")

#---CONSTANTS---

new_message = False
last_message = {
    "from": None,
    "data": None,
    "type": None
}

#---MAIN-BLUEPRINT---

main_blueprint = Blueprint('send_message', __name__)

@main_blueprint.route('/download/<filename>', methods=['GET', 'POST'])
def download_file(filename):
    try:
        return send_from_directory(
            "../data",
            filename,
            as_attachment=True
        )
    except FileNotFoundError:
        return jsonify({
            'status': '404',
            'message': f'Файл {filename} не знайдено.'
        }), 200

@main_blueprint.route('/api/send_message/', methods=['POST'])
def send_message_route():
    data = request.json

    if global_vars.CHAT_STATUS == "crew_working":
        message = {
            "from": "Assistant (Crew Working)",
            "data": "Crew is working...",
            "type": "message"
        }
        return jsonify(message)
    elif global_vars.CHAT_STATUS == None:
        query = data.get('query')
        final_result = start_crew_function(query)
        global_vars.CHAT_STATUS = None

        message = {
            "type": final_result["type"],
            "from": final_result["from"],
            "data": final_result["data"],
            "file_name": final_result["file_name"]
        }
        return jsonify(message)
    elif global_vars.CHAT_STATUS == 'user_answer':
        global_vars.CHAT_STATUS = "crew_working"
        query = data.get('query')
        submit_answer(query)
        message = {
            "from": "",
            "data": "",
            "type": ""
        }
        return jsonify(message)
    else:
        print(f"--A method selection error occurred in send_message.")

@main_blueprint.route('/api/return_answer/', methods=['GET'])
def return_answer():
    global new_message
    global last_message

    if request.is_json:
        message = request.get_json()
        
        MISSING_FIELDS = []

        if "from" not in message or not message["from"]:
            MISSING_FIELDS.append("from")
        if "data" not in message or not message["data"]:
            MISSING_FIELDS.append("data")

        if MISSING_FIELDS:
            return jsonify({"error": f"Missing or empty fields: {', '.join(MISSING_FIELDS)}"}), 400

        new_message = True
        last_message["from"] = message["from"]
        last_message["data"] = message["data"]
        last_message["type"] = message["type"]

        return jsonify({"message": "Message saved"}), 200
    else:
        if new_message:
            new_message = False
            message = {
                "type": last_message["type"],
                "from": last_message["from"],
                "data": last_message["data"]
            }
            return jsonify(message), 200
        else:
            return jsonify({"message": None, "crew_status": global_vars.CHAT_STATUS}), 200
    
#---FLASK-SERVER---

app = Flask(__name__)
CORS(app)

app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(port=os.getenv("FLASK_PORT"))