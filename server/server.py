import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uagents import Model
from uagents.query import query

AGENT_ADDRESS = "agent1qgpagptgy525qxnl20383gphrf42wctpw5hg6h0lsajtte9w4zl2qgumtgv"


class Request(Model):
    command: str


async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15.0)
    data = json.loads(response.decode_payload())
    command = data["text"]
    return command


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
def read_root():
    return "Hello from the Agent controller"


@app.post("/command")
async def make_agent_call(req: Request):
    try:
        res = await agent_query(req)
        return f"successful call - agent response: {res}"
    except Exception:
        return "unsuccessful agent call"