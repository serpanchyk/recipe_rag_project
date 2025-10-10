import gradio as gr
import httpx
import json
from typing import List, Dict


FASTAPI_URL = "http://localhost:8000/chat"

def chat_with_assistant(message: str, history: List[List[str]]) -> str:

    formatted_history = []
    for human, assistant in history:
        if human:
            formatted_history.append({"role": "user", "content": human})
        if assistant:
            formatted_history.append({"role": "assistant", "content": assistant})

    formatted_history.append({"role": "user", "content": message})

    try:
        response = httpx.post(
            FASTAPI_URL,
            json={"history": formatted_history},
            timeout=30.0
        )
        response.raise_for_status()

        response_data = response.json()
        return response_data.get("response", "Error: no answer from FastAPI.")

    except httpx.ConnectError:
        return "Connection error: Check whether Dockerfile is on port 8000."
    except Exception as e:
        return f"Errror API: {e}. Check Docker logs."


gr.ChatInterface(
    fn=chat_with_assistant,
    title="RAG-cook-assistant (FastAPI Client)"
).launch(server_port=7860)