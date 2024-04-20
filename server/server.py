import json
import uvicorn

from fastapi import FastAPI
from uagents import Model
from uagents.query import query

AGENT_ADDRESS = "agent1qgpagptgy525qxnl20383gphrf42wctpw5hg6h0lsajtte9w4zl2qgumtgv"


class TestRequest(Model):
    message: str


async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15.0)
    data = json.loads(response.decode_payload())
    return data["commmand"]


app = FastAPI()


@app.get("/")
def read_root():
    return "Hello from the Agent controller"


@app.post("/submit")
async def make_agent_call(req: TestRequest):
    try:
        res = await agent_query(req)
        return f"successful call - agent response: {res}"
    except Exception:
        return "unsuccessful agent call"
    
if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)