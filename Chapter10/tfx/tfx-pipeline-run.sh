#!/bin/bash

LOG_FILE="tfx-pipeline.log"
CONTAINER_NAME="tfx-pipeline-$(date +%Y%m%d%H%M)"

if command -v podman &> /dev/null; then
    echo "Pipeline is running. Check the logs with 'tail -f $LOG_FILE'"
    podman run --name $CONTAINER_NAME -it rod4n4m1/tfx-pipeline:latest > $LOG_FILE
elif command -v docker &> /dev/null; then
    echo "Pipeline is running. Check the logs with 'tail -f $LOG_FILE'"
    docker run --name $CONTAINER_NAME -it rod4n4m1/tfx-pipeline:latest > $LOG_FILE
else
  echo "Podman or Docker is required. Please install either Podman or Docker."
  exit 1
fi