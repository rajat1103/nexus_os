#!/bin/bash
echo "🚀 Starting NEXUS OS (Backend + Frontend)..."

uvicorn main:app --host 0.0.0.0 --port 8000 &

streamlit run app/ui/dashboard.py --server.port 8501 --server.address 0.0.0.0