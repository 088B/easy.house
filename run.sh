#!/bin/bash

# იპოვე თავისუფალი port
PORT=8000
while lsof -i :$PORT >/dev/null; do
  PORT=$((PORT + 1))
done

echo "Starting server on http://127.0.0.1:$PORT"
uvicorn main:app --reload --host 127.0.0.1 --port $PORT

