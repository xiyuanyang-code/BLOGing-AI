#!/bin/bash

# Start backend (Flask) on port 5000
echo "Starting backend on port 5000..."
nohup python3 ./src/backend/app.py > ./log/backend.log 2>&1 &

# Start frontend (simple HTTP server) on port 8000
echo "Starting frontend on port 8000..."
cd ./src/frontend || echo "Error, no such files or directories"
nohup python3 -m http.server 8000 > ../../log/frontend.log 2>&1 &

echo "Backend: http://127.0.0.1:5000"
echo "Frontend: http://127.0.0.1:8000"
echo "Both servers are running in the background."