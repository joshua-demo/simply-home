import json
from flask import Flask, request, jsonify
from uagents import Model
from flask_cors import CORS
from pydantic import Field
from utils import AgentProtocolAdapter, AgentAdapterError
import os

class Task(Model):
  # input payload
  task: str
  code: str

agent_adapter = AgentProtocolAdapter(endpoint="http://localhost:8000")
app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def root():
    return({ "message": "sup" })

@app.route("/submit", methods=["POST"])
async def send_task():
    try:
        res = await agent_adapter.send_message("agent1qgpagptgy525qxnl20383gphrf42wctpw5hg6h0lsajtte9w4zl2qgumtgv", Task(task="test", code="test"))
        json_response = json.loads(res)
        
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