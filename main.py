import os
import requests
import gradio as gr

# Load API keys from environment variables
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
WHISPER_API_KEY = os.getenv("WHISPER_API_KEY")

# NVIDIA API endpoints
LLAMA_API_URL = "https://integrate.api.nvidia.com/v1/llama-4-scout-17b-16e-instruct"
WHISPER_API_URL = "https://integrate.api.nvidia.com/v1/whisper-large-v3"

# Function to transcribe audio
def transcribe_audio(audio_file):
    with open(audio_file, "rb") as f:
        audio_data = f.read()
    
    headers = {
        "Authorization": f"Bearer {WHISPER_API_KEY}"
    }
    files = {
        "file": ("audio.wav", audio_data, "audio/wav")
    }

    response = requests.post(WHISPER_API_URL, headers=headers, files=files)
    result = response.json()

    return result.get("text", "Transcription failed")

# Function to chat with LLaMA
def chat_with_llama(prompt):
    headers = {
        "Authorization": f"Bearer {LLAMA_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "top_p": 0.9
    }

    response = requests.post(LLAMA_API_URL, headers=headers, json=payload)
    result = response.json()

    return result.get("choices", [{}])[0].get("message", {}).get("content", "No response")

# Combined pipeline
def process(audio_file):
    transcript = transcribe_audio(audio_file)
    reply = chat_with_llama(transcript)
    return transcript, reply

# Gradio UI
gr.Interface(
    fn=process,
    inputs=gr.Audio(type="filepath"),
    outputs=["text", "text"],
    title="Audio to Chat (NVIDIA Whisper + LLaMA-4)"
).launch()
