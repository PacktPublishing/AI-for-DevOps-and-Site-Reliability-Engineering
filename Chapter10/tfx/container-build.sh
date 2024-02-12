#!/bin/bash

# Build the container image
CONTAINER_ORG="rod4n4m1"
CONTAINER_NAME="tfx-pipeline"
CONTAINER_VERSION="0.2.1"

if command -v podman &> /dev/null; then
    podman build -t $CONTAINER_ORG/$CONTAINER_NAME:$CONTAINER_VERSION .
elif command -v docker &> /dev/null; then
    docker build -t $CONTAINER_ORG/$CONTAINER_NAME:$CONTAINER_VERSION .
else
  echo "Podman or Docker is required. Please install either Podman or Docker."
  exit 1
fi