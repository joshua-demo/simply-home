import os

import google.generativeai as genai
from dotenv import load_dotenv
from uagents import Agent, Context, Model

import actions # custom functions that will work on smart home devices

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
        base_prompt = """
        You are a smart home assistant. Your job is to understand and execute commands securely and efficiently. 
        You are given a list of commands to choose from. The query is a command from a user that
        you need to execute. You can use the given tools to match the user request
        to the most suitable command. If the command is not in the list, you say that no suitable command was found. 

        In this case, you will receive another message: this will be a Python function that will be suitable for executing the command. You will run this new function and then send a message to the user that the smart home has been adjusted.
        """
        command = base_prompt + _query.command

        # get all functions from actions.py (got this from chatgpt)
        all_functions = [func for func in dir(actions) if callable(getattr(actions, func))]
        functions_to_use = [getattr(actions, func) for func in all_functions if not func.startswith("__")]

        ctx.logger.info(functions_to_use)

        # send code to Gemini client 
        model = genai.GenerativeModel('gemini-pro', tools=functions_to_use)

        chat = model.start_chat(enable_automatic_function_calling=True)
        chat.send_message(command)

        has_function_call = any("function_call" in str(content.parts[0]) for content in chat.history)

        # remove this eventually; this just logs the chat history for debugging purposes
        chat_history_string = ""
        for content in chat.history:
            part = content.parts[0]
            chat_history_string += f"{content.role} -> {type(part).__name__}: {part}\n"
            chat_history_string += '-'*80 + "\n"
        ctx.logger.info(chat_history_string)
        # remove above eventually....

        if has_function_call:
            await ctx.send(sender, Response(text="successfully adjusted smart home"))
        else:
            await ctx.send(sender, Response(text="no suitable function was found"))
        
        for content in chat.history:
          part = content.parts[0]
          print(content.role, "->", type(part).to_dict(part))
          print('-'*80)
    except Exception as e:
        ctx.logger.error(f"An error occurred: {str(e)}")
        await ctx.send(sender, Response(text="fail"))


if __name__ == "__main__":
    orchestrator.run()
