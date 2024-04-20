import requests
from uagents import Agent, Context, Protocol, Model
from uagents.setup import fund_agent_if_low
 

# Orchestrator Agent
orchestrator = Agent(
   name="orchestrator", 
   port=8001, # 8000 is the server
   seed="orchestrator recovery phrase",
   endpoint=["http://localhost:8000/submit"],
)

fund_agent_if_low(orchestrator.wallet.address()) # https://fetch.ai/docs/guides/agents/register-in-almanacs

class Task(Model):
  # input payload
  task: str
  code: str

task_protocol = Protocol("Task Protocol")

@task_protocol.on_message(model=Task)
async def on_message(ctx: Context, sender: str, msg: Task):
    try:
      # server.py will send messages to the agent
      # the orchestrator agent receives past code + a task
      # the agent will determine if the task can be carried out
      # if not, it'll forward the task to another agent to create new functions
      ctx.logger.info(f"Received message from {sender}: {msg.dict()}")

      answer = ''
      if answer:
        response = await ctx.send(sender, "test response")
      else: # current code can't do the task...
        await ctx.send(sender, "test")

        # send code to second agent

    except Exception as e:
      # Handle any unexpected exceptions
      error_message = f"An error occurred: {str(e)}"
      await ctx.send(sender, UAgentResponse(message=error_message, type=UAgentResponseType.ERROR))

if __name__ == "__main__":
    orchestrator.run()
    print("uAgent address: ", orchestrator.address)