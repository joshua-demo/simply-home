import os

import google.generativeai as genai
from dotenv import load_dotenv
from uagents import Agent, Context, Model


class TestRequest(Model):
    command: str

class Response(Model):
    text: str

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) # configure Gemini client

orchestrator = Agent(
   name="orchestrator", 
   port=8001, # 8000 is the server
   seed="orchestrator recovery phrase",
   endpoint=["http://localhost:8001/submit"],
)


@orchestrator.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {orchestrator.name}")
    ctx.logger.info(f"With address: {orchestrator.address}")
    ctx.logger.info(f"And wallet address: {orchestrator.wallet.address()}")


@orchestrator.on_query(model=TestRequest, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: TestRequest):
    ctx.logger.info(_query)
    try:
        # send code to 
        model = genai.GenerativeModel('gemini-pro')
        ctx.logger.info(_query.command)
        response = model.generate_content("What is the meaning of life?")
        await ctx.send(sender, Response(text=response.text))
    except Exception as e:
        ctx.logger.error(f"An error occurred: {str(e)}")
        await ctx.send(sender, Response(text="fail"))


if __name__ == "__main__":
    orchestrator.run()
