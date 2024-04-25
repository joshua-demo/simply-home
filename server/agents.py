import os
import json

import google.generativeai as genai
from google.generativeai.types import content_types
from dotenv import load_dotenv
from uagents import Agent, Bureau, Context, Model
from collections.abc import Iterable
import requests
import importlib

import modules.instructions as instructions
import modules.actions as actions # custom functions that will work on smart home devices
from modules.utils import markdown_to_function

class Request(Model):
    command: str

class Response(Model):
    text: str
    command: str = None
    message: str = None
    status: int = None
    function_name: str = None
    

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

feedback_agent = Agent(
    name="feedback_agent",
    seed="feedback_agent recovery phrase",
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
    
@feedback_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {feedback_agent.name}")
    ctx.logger.info(f"With address: {feedback_agent.address}")

@orchestrator.on_query(model=Request, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: Request):
    requests.post("http://localhost:3000/api/setStep", json={"step": 0})

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
        if has_function_call:
            ctx.logger.info("Calling function and settings steps to 3")
            requests.post("http://localhost:3000/api/setStep", json={"step": 3})

        # if a function call appears in the chat history, assume successful adjustment
        if has_function_call: 
            await ctx.send(sender, Response(text="Successfully adjusted smart home.", command=command))
        # otherwise, go through tool_former to potentially generate a new function
        else:
            await ctx.send(tool_former.address, Response(text=command, command=command))

    except Exception as e:
        ctx.logger.error(f"An error occurred: {str(e)}")
        await ctx.send(sender, Response(text="Error in adjusting smart home.", command=command))

@tool_former.on_message(model=Response)
async def tool_former_message_handler(ctx: Context, sender: str, msg: Request):
    requests.post("http://localhost:3000/api/setStep", json={"step": 1})
    # reconfigure Gemini client --> we're using two keys so we don't get rate limited quickly
    genai.configure(api_key=os.getenv("GEMINI_API_KEY_V2"))
    # get all functions from actions.py so Gemini can use function calling capabilities
    all_functions = [func for func in dir(actions) if callable(getattr(actions, func))]
    functions_to_use = [getattr(actions, func) for func in all_functions if not func.startswith("__")]
    model = genai.GenerativeModel(
        'models/gemini-1.5-pro-latest', 
        system_instruction=instructions.tool_former_instruction,
        tools=functions_to_use,
    )
    
    try:
        if (sender == orchestrator.address):
            ctx.logger.info(f"Time to form a new function!\n")
            request = msg.text
            command = msg.command

            # start chat with Gemini client (following docs...)
            chat = model.start_chat(enable_automatic_function_calling=True)
            response = chat.send_message(request, tool_config=tool_config_from_mode("none"), safety_settings={'HATE': 'BLOCK_NONE','HARASSMENT': 'BLOCK_NONE','SEXUAL' : 'BLOCK_NONE','DANGEROUS' : 'BLOCK_NONE'})

            # verify that a NEW FUNCTION was made
            if response is not None and response.candidates and \
            "def" in response.candidates[0].content.parts[0].text:
                # function code from first candidate
                first_candidate = response.candidates[0]
                function_code = first_candidate.content.parts[0].text
                cleaned = markdown_to_function(markdown_text=function_code)
                function_name = cleaned.split('def ')[1].split('(')[0].strip()

                print("new function created: " + function_name + "\n" + cleaned +'\n')

                # verify the generated function with the feedback loop agent
                await ctx.send(feedback_agent.address, Response(text=cleaned, command=command, function_name=function_name))
                ctx.logger.info(f"Sent new function to feedback agent for verification")

            # otherwise, the Tool Former did not generate a new function
            # this is usually because the user's command wasn't smart-home related...
            else:
                # Handle case where no function is generated
                ctx.logger.info("No function generated in response")
        else:
            
            # logic for receiving message from feedback agent
            if (msg.status == 200):
                # passed the feedback loop, so run the function
                ctx.logger.info(f"Code passed feedback loop")
                # get all functions from actions.py AGAIN (account for newly added function)

                # append new function to actions.py
                with open('./modules/actions.py', 'a') as file:
                    file.write('\n' + msg.text + '\n')
                
                importlib.reload(actions)
                requests.post("http://localhost:3000/api/setStep", json={"step": 3})
                getattr(actions, msg.function_name)()
            else:
                # didn't pass the feedback loop, so reiterate and send back to the feedback loop for further testing
                ctx.logger.info(f"Code failed feedback loop")
                # start chat with Gemini client (following docs...)
                request = f"The function you previously generated failed the feedback loop. The error message was: {msg.message}. Your old code is: {msg.text}. You need to refactor the code to pass the feedback loop while accomplishing the same command, which is {msg.command}."
                chat = model.start_chat(enable_automatic_function_calling=True)
                response = chat.send_message(request, tool_config=tool_config_from_mode("none"), safety_settings={'HATE': 'BLOCK_NONE','HARASSMENT': 'BLOCK_NONE','SEXUAL' : 'BLOCK_NONE','DANGEROUS' : 'BLOCK_NONE'})
                await ctx.send(feedback_agent.address, Response(text=msg.text, command=msg.command, function_name=msg.function_name))

    except Exception as e:
        await ctx.send(orchestrator.address, Response(text="Error creating a new function"))
        ctx.logger.error(f"An error occurred: {str(e)}")
        requests.post("http://localhost:3000/api/setStep", json={"step": -1})
        await ctx.send(sender, Response(text="fail"))

@feedback_agent.on_message(model=Response)
async def feedback_agent_message_handler(ctx: Context, sender: str, msg: Response):
    requests.post("http://localhost:3000/api/setStep", json={"step": 2})
    genai.configure(api_key=os.getenv("GEMINI_API_KEY_V3"))
    
    ctx.logger.info(f"Starting feedback process")
    try:
        function = msg.text
        command = msg.command

        model = genai.GenerativeModel(
            'models/gemini-1.5-pro-latest', 
            system_instruction=instructions.feedback_agent_instruction,
            generation_config={"response_mime_type": "application/json"}
        )

        message = f"The description of what the function should be doing is: {function}. The code of the command is {command}."

        chat = model.start_chat()
        response_str = chat.send_message(message, tool_config=tool_config_from_mode("none"), safety_settings={'HATE': 'BLOCK_NONE','HARASSMENT': 'BLOCK_NONE','SEXUAL' : 'BLOCK_NONE','DANGEROUS' : 'BLOCK_NONE'})
        # Load the JSON string
        response_json = json.loads(response_str.text)

        # Access message and status directly from the JSON object
        message_json = response_json['message']
        status_json = response_json['status']
        
        ctx.logger.info(f"message {message_json} with status code {status_json}")
        await ctx.send(tool_former.address, Response(text=function, command=command, message=message_json, status=status_json, function_name=msg.function_name))
        
    except Exception as e:
        ctx.logger.error(f"An error occurred: {str(e)}")

community = Bureau(port=8001)
community.add(orchestrator)
community.add(tool_former)
community.add(feedback_agent)

if __name__ == "__main__":
    community.run()
