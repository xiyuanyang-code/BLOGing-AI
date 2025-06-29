#!/bin/bash

echo "Stopping backend (Flask) and frontend (HTTP/HTTPS) servers..."

# Kill backend (Flask) process
pkill -f "python3.*src/backend/app.py"

# Kill frontend (http.server) process (both HTTP and HTTPS)
pkill -f "python3 -m http.server"

echo "All servers have been stopped."