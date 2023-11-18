# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install PostgreSQL development files
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the shared directory
COPY src/shared /usr/src/app/shared

# Copy the specific service files
COPY src/web_service /usr/src/app/web_service

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r ./web_service/requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5001

# Run app.py when the container launches
CMD ["python", "-m", "web_service.app"]