# Use Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app/ ./app/

# Expose Gradio port
EXPOSE 7860

# Run the app
CMD ["python", "./app/main.py"]
