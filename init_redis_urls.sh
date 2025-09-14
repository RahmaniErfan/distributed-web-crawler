#!/bin/bash

# Wait for Redis to be ready
echo "Waiting for Redis to start..."
until redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ping; do
  sleep 1
done
echo "Redis is ready."

# Read URLs from start_urls.txt and push them to Redis
echo "Pushing start URLs to Redis..."
while IFS= read -r url; do
  if [ -n "$url" ]; then # Check if URL is not empty
    json_url="{\"url\": \"$url\"}"
    redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" LPUSH web_spider:start_urls "$json_url"
    echo "Pushed: $url"
  fi
done < start_urls.txt

echo "All start URLs pushed to Redis."
