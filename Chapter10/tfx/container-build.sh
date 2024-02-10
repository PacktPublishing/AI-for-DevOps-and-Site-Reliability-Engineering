#!/bin/bash

# Build the container image

if command -v podman &> /dev/null; then
    podman build -t tfx-pipeline .
elif command -v docker &> /dev/null; then
    docker build -t tfx-pipeline .
else
  echo "Podman or Docker is required. Please install either Podman or Docker."
  exit 1
fi