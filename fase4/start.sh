#!/bin/bash

# Start the FastAPI backend in the background
echo "Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 8004 &

# Wait a few seconds to ensure the backend is up
sleep 5

# Start the Streamlit frontend
echo "Starting Streamlit dashboard..."
streamlit run dashboard.py --server.port 8504 --server.address 0.0.0.0
