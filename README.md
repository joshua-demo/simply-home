# Roomy
## Getting started
Before running, there will be no default house state or set python functions for the orchestrator to call
Copy the template files before running
```bash
cp home-sim/app/api/default.json home-sim/app/api/data.json 
cp server/defaultActionsTemplate.py server/actions.py 
```

## How to run
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