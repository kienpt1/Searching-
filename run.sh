#!/bin/bash
docker start mysql-container
# Run Streamlit app in the background
streamlit run UI.py &

# Run FastAPI app using Uvicorn in the background
uvicorn Realease_Web:app --reload &


# pkill -f "streamlit run test1.py"
# pkill -f "uvicorn Web:app"
