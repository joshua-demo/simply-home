# Roomy
Smart homes offer a set of basic device functionalities that users can use to build complex routines. But intelligent automatons require manual set up and normal interactions are handled with dashboards because voice assistants are flaky.

Roomy is an AI powered smarter home proof of concept. We apply the tool forming and auto GPT concepts to build an intelligent assistant capable of handling complex, and opinionated interactions.
![System Design](https://github.com/joshua-demo/simply-home/assets/79354255/a9a707d0-a22f-47fe-8020-dfe8150c836c)

Roomy uses an orchestrator model to understand the users request and apply it to the most relevant command(s). If there are no commands that handle the user's request, the orchestrator calls the tool former. The tool former generates a new function building on the previous functions and it appends it to the set of functions for the orchestrator to call from. The tool former goes through a feedback cycle with a feedback agent until the tool former generates a function that compiles and meets the user's request (if possible). As roomy is used and it generates more functions it continuous to augment and improve it's abilities until it has a minimal amount of function creations. Power users can then write their own functions in python for the orchestrator to call, or they can edit python functions created by the tool former.

Roomy is a winning hackathon project from LA Hacks 2024, written by [Mauricio Curiel](https://github.com/Luceium), [Jonathan Nguyen](https://github.com/jonathanguven), [Steven Le](https://github.com/steeevin88), and [Joshua Demo](https://github.com/joshua-demo).
Roomy won the [Fetch.ai](https://fetch.ai/) company challenge. Check out our [Devpost Submission](https://devpost.com/software/harmonichomes).
## What's next?
### TODO
- fine tune models & improve prompt engineering per model
- allow the orchestrator to handle questions by making the distinction between commands and questions (answering questions using RAG)
- enable complex functions including event based calls (ie. when temp < 50 or time=="8:45PM")
- move to smaller models that can be run locally on dedicated hardware
- enable control over real smart home devices (looking into home assistant integration)

### Contribute
- Please open up issues for feature requests and bug reports
- Fork and submit PRs to contribute changes directly

## How to run
#### Getting started
Before running, there will be no default house state or set python functions for the orchestrator to call
Copy the template files before running
```bash
cp home-sim/app/api/default.json home-sim/app/api/data.json 
cp server/defaultActionsTemplate.py server/actions.py 
```

Note that all commands are from the root directory of the repo
### Front End
#### Home-Portal
```bash
cd home-portal;
bun run dev;
```
#### Home-Sim
```bash
cd home-sim;
bun run dev;
```
### Back End
You will need to create and set up a virtual environment before running our scripts.
```bash
cd server;
python -m venv venv;
# Download the dependencies
pip install -r requirements.txt;
```
#### Fast API Server
```bash
cd server;
source venv/bin/activate;
uvicorn server:app --reload;
```
#### Agents
```bash
cd server;
source venv/bin/activate;
python agents.py;
```
Note that agents.py will not hot reload so you will need to kill it and restart it to reflect updates.
