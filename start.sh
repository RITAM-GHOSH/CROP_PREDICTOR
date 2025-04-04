#!/bin/bash

# Use PORT from environment or default to 5000
PORT="${PORT:-5000}"

# Run streamlit with specified port
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
