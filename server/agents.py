import os

import google.generativeai as genai
from google.generativeai.types import content_types
from dotenv import load_dotenv
from uagents import Agent, Bureau, Context, Model
import instructions
from collections.abc import Iterable
import requests
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
    ctx.logger.info(f"And wallet address: {orchestrator.wallet.address()}")
    requests.post("http://localhost:3000/api/setStep", json={"step": 0})

@tool_former.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {tool_former.name}")
    ctx.logger.info(f"With address: {tool_former.address}")

@orchestrator.on_query(model=Request, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: Request):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY")) # configure Gemini client
    ctx.logger.info(_query)
    try:
        command = _query.command

        importlib.reload(actions)
        # get all functions from actions.py ---> used to pass to Gemini clients (for function calling)
        all_functions = [func for func in dir(actions) if callable(getattr(actions, func))]
        functions_to_use = [getattr(actions, func) for func in all_functions if not func.startswith("__")]

        ctx.logger.info(functions_to_use)
        # send code to Gemini client 
        model = genai.GenerativeModel(
            'models/gemini-1.5-pro-latest', 
            tools=functions_to_use, 
            system_instruction=instructions.orchestrator_instruction,
        )
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
        '''
        chat_history_string = ""
        for content in chat.history:
            part = content.parts[0]
            chat_history_string += f"{content.role} -> {type(part).__name__}: {part}\n"
            chat_history_string += '-'*80 + "\n"
        ctx.logger.info(chat_history_string)
        # remove above eventually....
        '''

        if has_function_call:
            await ctx.send(sender, Response(text="successfully adjusted smart home"))
        else:
            # get new function(s) from tool_former
            await ctx.send(tool_former.address, Response(text=command))
        
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
    genai.configure(api_key=os.getenv("GEMINI_API_KEY_V2")) # configure Gemini client
    ctx.logger.info(f"Received message from {sender}: {msg.text}")
    requests.post("http://localhost:3000/api/setStep", json={"step": 1})
    try:
        request = msg.text
        # get all functions from actions.py ---> used to pass to Gemini clients (for function calling)
        all_functions = [func for func in dir(actions) if callable(getattr(actions, func))]
        functions_to_use = [getattr(actions, func) for func in all_functions if not func.startswith("__")]
        model = genai.GenerativeModel(
            'models/gemini-1.5-pro-latest', 
            system_instruction=instructions.tool_former_instruction,
            tools=functions_to_use,
        )
        chat = model.start_chat(enable_automatic_function_calling=True)
        
        response = chat.send_message(request, tool_config=tool_config_from_mode("none"))

        if response is not None and response.candidates:
            # Extract function code from first candidate (assuming one function)
            first_candidate = response.candidates[0]
            function_code = first_candidate.content.parts[0].text
            cleaned = markdown_to_function(markdown_text=function_code)
            function_name = cleaned.split('def ')[1].split('(')[0].strip()

            print("new function created:\n" + cleaned)

            new_function = None
            # execute the new function so we can reference it via Gemini client later
            # append new function to actions.py
            with open('./actions.py', 'a') as file:
                file.write('\n' + cleaned + '\n')

            # get all functions from actions.py AGAIN (account for new function)
            #import actions # reimport bc new function was added to actions.py
            all_functions = [func for func in dir(actions) if callable(getattr(actions, func))]
            new_functions_to_use = [getattr(actions, func) for func in all_functions if not func.startswith("__")]
            
            print(new_functions_to_use)
            # call the newly generated function through Gemini function calling
            chat = model.start_chat(enable_automatic_function_calling=True)
            response = chat.send_message(
                "Run the function that was generated for me; it should have the name " + function_name,
                tools=new_functions_to_use,
                tool_config=tool_config_from_mode("any")
            )
            as_function_call = any("function_call" in str(content.parts[0]) for content in chat.history)
            if as_function_call:
                ctx.logger.info("Calling function and settings steps to 3")
                requests.post("http://localhost:3000/api/setStep", json={"step": 3})

            ctx.logger.info(response)

        else:
            # Handle case where no function is generated
            ctx.logger.info("No function generated in response")
            
    except Exception as e:
        ctx.send(sender, Response(text="tool_former did not create a new function"))
        ctx.logger.error(f"An error occurred: {str(e)}")
        requests.post("http://localhost:3000/api/setStep", json={"step": -1})
        await ctx.send(sender, Response(text="fail"))


community = Bureau(port=8001)
community.add(orchestrator)
community.add(tool_former)

if __name__ == "__main__":
    community.run()
