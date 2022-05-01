FROM python:3.8-slim-buster

RUN apt-get update && apt-get -y install git && apt-get -y install curl && apt-get -y install nano

# Update PIP & install package/requirements
RUN python -m pip install --upgrade pip
RUN pip install faust-streaming
RUN pip install requests

# Copy application files:
WORKDIR /app
COPY . /app

# Execute the machine learning pipeline:
CMD faust -A streaming_app worker -l info
