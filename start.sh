#!/bin/bash

# Start the backend server in the background
echo "Starting Uvicorn server..."
cd /app
uvicorn app.main:app --host 127.0.0.1 --port 8000 &

# Start the nginx server in the foreground
echo "Starting Nginx server..."
nginx -g 'daemon off;'
