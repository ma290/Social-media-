import requests
import gradio as gr

# Function to transcribe audio using Whisper Large v3
def transcribe_and_generate(audio_file, api_key):
    whisper_url = "https://integrate.api.nvidia.com/v1/whisper-large-v3"
    llama_url = "https://integrate.api.nvidia.com/v1/llama-4-scout-17b-16e-instruct"

    headers = {"Authorization": f"Bearer {api_key}"}

    # 1. Transcribe audio
    with open(audio_file, "rb") as f:
        files = {"file": f}
        whisper_response = requests.post(whisper_url, headers=headers, files=files)

    try:
        whisper_response.raise_for_status()
        transcript = whisper_response.json().get("text", "")

        # 2. Use transcript in LLM
        payload = {
            "messages": [
                {"role": "system", "content": "You are a content expert who turns audio into engaging social media posts."},
                {"role": "user", "content": f"Convert this transcript into a social media post:\n\n{transcript}"}
            ],
            "temperature": 0.7,
            "top_p": 0.9
        }

        llama_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        llama_response = requests.post(llama_url, headers=llama_headers, json=payload)
        llama_response.raise_for_status()
        content = llama_response.json()["choices"][0]["message"]["content"]

        return transcript, content

    except Exception as e:
        return f"Error: {str(e)}", ""

# Gradio interface
gr.Interface(
    fn=transcribe_and_generate,
    inputs=[
        gr.Audio(label="Upload Audio", type="filepath"),
        gr.Textbox(label="NVIDIA API Key", type="password")
    ],
    outputs=[
        gr.Textbox(label="Transcript"),
        gr.Textbox(label="Generated Social Media Post")
    ],
    title="All-in-One: Audio to Post Generator (NVIDIA Whisper + LLaMA 4 Scout)"
).launch(share=True, debug=True)
