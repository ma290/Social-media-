import gradio as gr
import whisper
import os
import requests

# App state
global_api_key = ""

# Load Whisper model
whisper_model = whisper.load_model("large")

# Transcribe audio
def transcribe_audio(audio_path):
    result = whisper_model.transcribe(audio_path)
    return result["text"]

# Generate content using Llama-4-Scout via NVIDIA API
def generate_with_llama(prompt, content_type, tone):
    global global_api_key
    headers = {
        "Authorization": f"Bearer {global_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-4-scout",
        "prompt": f"Generate a {content_type} in a {tone} tone from this: {prompt}",
        "temperature": 0.7
    }
    response = requests.post("https://integrate.api.nvidia.com/v1/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("text", "No output.")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# All-in-One Social Media Content Generator")

    with gr.Row():
        api_key_input = gr.Textbox(placeholder="Enter NVIDIA API Key", type="password", label="API Key")
        set_key_btn = gr.Button("Set API Key")
        status_text = gr.Textbox(label="Status", interactive=False)

    def set_key(key):
        global global_api_key
        global_api_key = key
        return "API Key set. You can now use the app."

    set_key_btn.click(fn=set_key, inputs=api_key_input, outputs=status_text)

    with gr.Tab("Voice Input"):
        audio = gr.Audio(source="upload", label="Upload Audio/Video")
        trans_btn = gr.Button("Transcribe & Generate")

    with gr.Tab("Text Input"):
        text_input = gr.Textbox(lines=4, placeholder="Paste or type text here")
        text_btn = gr.Button("Generate Content")

    content_type = gr.Dropdown(["Blog post", "Summary", "LinkedIn caption", "Twitter caption", "TikTok caption", "Email draft"], label="Content Type")
    tone = gr.Dropdown(["Casual", "Formal", "Witty"], label="Tone")

    output = gr.Textbox(lines=15, label="Generated Output")

    def transcribe_and_generate(audio_file, content_type, tone):
        if not global_api_key:
            return "Please set the API key first."
        text = transcribe_audio(audio_file)
        return generate_with_llama(text, content_type, tone)

    def generate_from_text(text_input, content_type, tone):
        if not global_api_key:
            return "Please set the API key first."
        return generate_with_llama(text_input, content_type, tone)

    trans_btn.click(fn=transcribe_and_generate, inputs=[audio, content_type, tone], outputs=output)
    text_btn.click(fn=generate_from_text, inputs=[text_input, content_type, tone], outputs=output)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:demo", host="0.0.0.0", port=7860, factory=True)
