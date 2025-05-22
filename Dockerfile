# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Expose port for Gradio
EXPOSE 8000

# Run the app (replace app.py with your file if named differently)
CMD ["python", "main.py"]
