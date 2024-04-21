import os

import google.generativeai as genai
from google.generativeai.types import content_types
from dotenv import load_dotenv
from uagents import Agent, Bureau, Context, Model
import instructions
from collections.abc import Iterable
import importlib

import actions # custom functions that will work on smart home devices
from utils import markdown_to_function

class Request(Model):
    command: str

class Response(Model):
    text: str

load_dotenv()

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

@tool_former.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {tool_former.name}")
    ctx.logger.info(f"With address: {tool_former.address}")

@orchestrator.on_query(model=Request, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: Request):

    # configure Gemini client --> we're using two keys so we don't get rate limited quickly
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    ctx.logger.info(_query)
    try:
        command = _query.command

        # reimport actions.py to account for any new functions that were added (by tool_former)
        # then, get all functions from actions.py so Gemini can use function calling capabilities
        importlib.reload(actions)
        all_functions = [func for func in dir(actions) if callable(getattr(actions, func))]
        functions_to_use = [getattr(actions, func) for func in all_functions if not func.startswith("__")]

        # send code to Gemini client 
        model = genai.GenerativeModel(
            'models/gemini-1.5-pro-latest', 
            tools=functions_to_use, 
            system_instruction=instructions.orchestrator_instruction,
        )

        # start chat with Gemini client (following docs...)
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

        # boolean value to check if function call was made
        has_function_call = any("function_call" in str(content.parts[0]) for content in chat.history)

        # if a function call appears in the chat history, assume successful adjustment
        if has_function_call: 
            await ctx.send(sender, Response(text="Successfully adjusted smart home."))
        # otherwise, go through tool_former to potentially generate a new function
        else:
            await ctx.send(tool_former.address, Response(text=command))

    except Exception as e:
        ctx.logger.error(f"An error occurred: {str(e)}")
        await ctx.send(sender, Response(text="Error in adjusting smart home."))

@tool_former.on_message(model=Response)
async def tool_former_message_handler(ctx: Context, sender: str, msg: Request):
    # reconfigure Gemini client --> we're using two keys so we don't get rate limited quickly
    genai.configure(api_key=os.getenv("GEMINI_API_KEY_V2"))
    ctx.logger.info(f"Time to form a new function!\n")

    try:
        request = msg.text

        # get all functions from actions.py so Gemini can use function calling capabilities
        all_functions = [func for func in dir(actions) if callable(getattr(actions, func))]
        functions_to_use = [getattr(actions, func) for func in all_functions if not func.startswith("__")]
        model = genai.GenerativeModel(
            'models/gemini-1.5-pro-latest', 
            system_instruction=instructions.tool_former_instruction,
            tools=functions_to_use,
        )

        # start chat with Gemini client (following docs...)
        chat = model.start_chat(enable_automatic_function_calling=True)
        response = chat.send_message(request, tool_config=tool_config_from_mode("none"))

        # verify that a NEW FUNCTION was made
        if response is not None and response.candidates and \
        "def" in response.candidates[0].content.parts[0].text:
            # function code from first candidate
            first_candidate = response.candidates[0]
            function_code = first_candidate.content.parts[0].text
            cleaned = markdown_to_function(markdown_text=function_code)
            function_name = cleaned.split('def ')[1].split('(')[0].strip()

            print("new function created: " + function_name + "\n" + cleaned +'\n')

            # append new function to actions.py
            with open('./actions.py', 'a') as file:
                file.write('\n' + cleaned + '\n')

            # get all functions from actions.py AGAIN (account for newly added function)
            importlib.reload(actions)
            getattr(actions, function_name)()

        # otherwise, the Tool Former did not generate a new function
        # this is usually because the user's command wasn't smart-home related...
        else:
            # Handle case where no function is generated
            ctx.logger.info("No function generated in response")

    except Exception as e:
        await ctx.send(sender, Response(text="tool_former did not create a new function"))
        ctx.logger.error(f"An error occurred: {str(e)}")


community = Bureau(port=8001)
community.add(orchestrator)
community.add(tool_former)

if __name__ == "__main__":
    community.run()
