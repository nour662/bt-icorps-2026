FROM python:3.11-slim

# docker's working directory
WORKDIR /code

# install system dependencies
RUN apt-get update && app-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# install python requirements
COPY requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy the project app folder into the container
COPY ./app /code/app