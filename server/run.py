import multiprocessing
import signal
import sys

import uvicorn

from server import app
from agents import community


def run_server():
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)


def run_agents():
    community.run()


def handler(sig, frame):
    server_process.terminate()
    agent_process.terminate()
    print("Processes terminated")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)

    server_process = multiprocessing.Process(target=run_server)
    agent_process = multiprocessing.Process(target=run_agents)

    server_process.start()
    agent_process.start()

    try:
        server_process.join()
        agent_process.join()
    except KeyboardInterrupt:
        pass