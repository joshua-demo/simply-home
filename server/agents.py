import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import Field
from uagents import Model
import uvicorn


class Task(Model):
  # input payload
  task: str = Field(description="")
  code: str = Field(description="")

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return({ "message": "sup" })

@app.post("/submit")
async def send_task():
    try:
        json_response = 'sup'        
        return json_response # not sure what this looks like
    except Exception as e:
        return { "error": str(e) }

@app.route("/callback")
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
    uvicorn.run("server:app", port=8000, reload=True)