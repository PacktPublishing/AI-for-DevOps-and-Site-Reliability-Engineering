#!/bin/bash

# Set the constants
PROJECT_ID=$1
ACCOUNT=$2
ROLE1="roles/aiplatform.user"
ROLE2="roles/storage.admin"
SERVICES="iam.googleapis.com compute.googleapis.com notebooks.googleapis.com storage.googleapis.com aiplatform.googleapis.com"

# Check if parameters are provided
if [ -z "$PROJECT_ID" ] || [ -z "$ACCOUNT" ]; then
    echo "Usage: ./gcloud-setup.sh PROJECT_ID ACCOUNT"
    exit 1
fi

# Check if the project exists
VALID_PROJECT=`gcloud projects describe $PROJECT_ID`
if [ -z "$VALID_PROJECT" ]; then
    echo "Project $PROJECT_ID does not exist"
    exit 1
fi

# Update gcloud CLI itself
gcloud components update

# Authenticate gcloud
gcloud auth login

# Enable GCP services for the project
gcloud services enable $SERVICES

# Grant the roles to the user
gcloud projects add-iam-policy-binding $PROJECT_ID --member="user:$ACCOUNT" --role=$ROLE1
gcloud projects add-iam-policy-binding $PROJECT_ID --member="user:$ACCOUNT" --role=$ROLE2