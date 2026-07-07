FROM python:3.10-slim

WORKDIR /code

# Copy requirements and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the default Hugging Face port (7860)
EXPOSE 7860

# Run Flask on port 7860 and bind to all interfaces
CMD ["python", "app.py"]
