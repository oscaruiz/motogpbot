FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy only the requirements file initially to leverage Docker cache
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --pre

# Copy the rest of the application code
COPY src/ /app/src/

# Run bot.py when the container launches
CMD ["python", "/app/src/bot.py"]
