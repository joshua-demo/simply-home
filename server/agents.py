import os
from google.generativeai.types import content_types

import google.generativeai as genai
from dotenv import load_dotenv
from uagents import Agent, Bureau, Context, Model
import instructions
from collections.abc import Iterable
import requests

import actions # custom functions that will work on smart home devices

class Request(Model):
    command: str

class Response(Model):
    text: str

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) # configure Gemini client

orchestrator = Agent(
   name="orchestrator", 
   seed="orchestrator recovery phrase",
   endpoint=["http://localhost:8001/submit"],
)

tool_former = Agent(
    name="tool_former",
    seed="tool_former recovery phrase",
    endpoint=["http://localhost:8001/submit"],
)

def tool_config_from_mode(mode: str, fns: Iterable[str] = ()):
    """Create a tool config with the specified function calling mode."""
    return content_types.to_tool_config(
        {"function_calling_config": {"mode": mode, "allowed_function_names": fns}}
    )

@orchestrator.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {orchestrator.name}")
    ctx.logger.info(f"With address: {orchestrator.address}")
    ctx.logger.info(f"And wallet address: {orchestrator.wallet.address()}")
    requests.post("http://localhost:3000/api/setStep", json={"step": 0})

@tool_former.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {tool_former.name}")
    ctx.logger.info(f"With address: {tool_former.address}")
    ctx.logger.info(f"And wallet address: {tool_former.wallet.address()}")


@orchestrator.on_query(model=Request, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: Request):
    ctx.logger.info(_query)
    try:
        command = _query.command

        # get all functions from actions.py (got this from chatgpt)
        all_functions = [func for func in dir(actions) if callable(getattr(actions, func))]
        functions_to_use = [getattr(actions, func) for func in all_functions if not func.startswith("__")]

        ctx.logger.info(functions_to_use)

        # send code to Gemini client 
        model = genai.GenerativeModel('models/gemini-1.5-pro-latest', tools=functions_to_use, system_instruction=instructions.orchestrator_instruction)
        chat = model.start_chat(enable_automatic_function_calling=True)
        chat.send_message(
            command, 
            tool_config=tool_config_from_mode("auto"), 
            safety_settings={
                'HATE': 'BLOCK_NONE',
                'HARASSMENT': 'BLOCK_NONE',
                'SEXUAL' : 'BLOCK_NONE',
                'DANGEROUS' : 'BLOCK_NONE'
            }
        )

        has_function_call = any("function_call" in str(content.parts[0]) for content in chat.history)
        if has_function_call:
            ctx.logger.info("Calling function and settings steps to 3")
            requests.post("http://localhost:3000/api/setStep", json={"step": 3})

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
            # get new function(s) from tool_former
            await ctx.send(tool_former.address, Response(text=command))

            await ctx.send(sender, Response(text="no suitable function was found"))
        
        for content in chat.history:
          part = content.parts[0]
          print(content.role, "->", type(part).to_dict(part))
          print('-'*80)
    except Exception as e:
        ctx.logger.error(f"An error occurred: {str(e)}")
        requests.post("http://localhost:3000/api/setStep", json={"step": -1})
        await ctx.send(sender, Response(text="fail"))

@tool_former.on_message(model=Response)
async def tool_former_message_handler(ctx: Context, sender: str, msg: Request):
    ctx.logger.info(f"Received message from {sender}: {msg.text}")
    requests.post("http://localhost:3000/api/setStep", json={"step": 1})
    try:
        request = msg.text
        model = genai.GenerativeModel('models/gemini-1.5-pro-latest', system_instruction=instructions.tool_former_instruction)
        chat = model.start_chat(enable_automatic_function_calling=True)
        function = chat.send_message(request, tool_config=tool_config_from_mode("none"))
        ctx.logger.info(f"Function generated: {function}")
        as_function_call = any("function_call" in str(content.parts[0]) for content in chat.history)
        if as_function_call:
            ctx.logger.info("Calling function and settings steps to 3")
            requests.post("http://localhost:3000/api/setStep", json={"step": 3})
    except Exception as e:
        ctx.logger.error(f"An error occurred: {str(e)}")
        requests.post("http://localhost:3000/api/setStep", json={"step": -1})
        await ctx.send(sender, Response(text="fail"))


community = Bureau(port=8001)
community.add(orchestrator)
community.add(tool_former)

if __name__ == "__main__":
    community.run()
