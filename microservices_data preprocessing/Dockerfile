# Use the official Python base image
FROM python:3.9

# Install Java (Required for PySpark)
RUN apt-get update && apt-get install -y default-jdk

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script and credentials
COPY preprocess_container.py .
COPY big-test-449715-2b0e9010365e.json credentials.json

# Set environment variables
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

# Run the script
CMD ["python", "preprocess_container.py"]
