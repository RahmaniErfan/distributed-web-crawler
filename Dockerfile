# Use an official Python runtime as a parent image
FROM python:3.9-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install redis-cli for the init_urls service
RUN apt-get update && apt-get install -y redis-tools && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app
RUN sed -i 's/\r$//' init_redis_urls.sh

# Set environment variables for Scrapy
ENV PYTHONUNBUFFERED 1

# Command to run the Scrapy spider (this will be overridden by docker-compose)
# The command needs to be run from the directory containing scrapy.cfg
CMD ["scrapy", "crawl", "web_spider"]
