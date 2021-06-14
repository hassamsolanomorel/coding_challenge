FROM python:3.6.13-slim as base

# Install system packages needed by this container
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev libkeyutils1 libpq-dev python-dev libyaml-dev

# Create directory for code
RUN mkdir -p /usr/src \
    && touch /usr/src/__init__.py

# Install required Python libraries
# NOTE: We should separate the service requirements from the test requirements
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Clean up system packages
RUN apt-get purge -y gcc gcc-4.9 cpp python-dev \
    && rm -rf /var/lib/apt/lists/*

# Put things in place
WORKDIR /usr/src
COPY app/ /usr/src/app
COPY ../run.py /usr/src/run.py
COPY ../.coveragerc /usr/src/.coveragerc
