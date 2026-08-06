# VISION - Youtube Comment Analysis
developer - BHAVISHYA SHARMA

[Video Demo](vision.mp4) <br>
[Architecture](architecture.drawio.svg)<br>
[Development Scratchpad](idea.md)<br>

## Overview
This Project focuses on clustering youtube comments and getting useful insights from them in the form of a dashboard.<br>
I didn't want to spend my useful 10-20 minutes (per video) reading comments on youtube video just to satisfy my curiosity about knowing people's reaction on that video.<br>
Later It got converted to a system for youtube creators.<br>

## Specs
API used for downloading comments : Youtube Data API v3<br>
Clustering Comments : Bertopic + Local LLM (topic 
generation)<br>
Embedding : AkshitaS/bhasha-embed-v0<br>
Frontend  : Streamlit<br>
Orchestration of Backend : Python, FastAPI server<br>
Topic Generation and Categorization : Ollama (ibm/granite-4.1-3B)<br>

## Local Setup
1. Get anaconda environment ready using environment.yml
2. Download and Setup Ollama
   1. Download ibm/granite-4.1-3B using `ollama pull ibm/granite-4.1-3b` in Terminal
3. Get your API key ready and put it in `.env` File in root dir

## Usage
1. Start the Python Server using ` uvicorn backend.orchestrate:app --host 127.0.0.1 --port 8001`
2. Start Streamlit Server using `streamlit run landingpage.py --server.runOnSave false`
3. You'll be redirected to the correct page.

## Logs
If any Error happens, you'll hear a 1 sec Beep Sound, just open both terminals to see what's wrong in case something goes wrong.


   





