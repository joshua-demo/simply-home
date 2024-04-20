import json
from flask import Flask, request, jsonify
from uagents import Model
from flask_cors import CORS
from pydantic import Field
import os

class Task(Model):
  # input payload
  task: str
  code: str

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def root():
    return({ "message": "sup" })

@app.route("/submit", methods=["POST"])
async def send_task():
    try:
        json_response = "sup"
        
        return json_response # not sure what this looks like
    except Exception as e:
        return { "error": str(e) }

@app.route("/callback", methods=["POST"])
def agent_callback():
    """
    This endpoint is called by external agents when it receives a message.
    """
    #print(request.get_json())
    try:
        print()
        #agent_adapter.process_response(request.get_json())
    except AgentAdapterError as e:
        return {}

    return {}

if __name__ == "__main__":
    app.run(debug=True, port=8000)