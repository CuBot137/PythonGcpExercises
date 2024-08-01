FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for Google Cloud credentials
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/key.json"

# Expose port 8080 to the outside world
EXPOSE 8081

# Run app.py when the container launches
CMD ["python", "main.py"]
