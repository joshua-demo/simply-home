cd home-sim && bun run dev && cd ..;
cd home-portal && bun run dev && cd ..;
cd server && python agents.py && uvicorn server.py  && echo "running all services"
echo "running all services"
