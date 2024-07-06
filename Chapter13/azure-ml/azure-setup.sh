#!/bin/bash
# Based on the following documentation:
# https://learn.microsoft.com/en-us/azure/machine-learning/how-to-configure-cli

USER_NAME=$1
SUBSCRIPTION_ID=$2
WS_NAME="sre-ml-workspace"
RG_NAME="sre-ml-rg"
LOCATION="eastus"

# Sign in to Azure
az login -u $USER_NAME
# Set the default subscription
az account set -s $SUBSCRIPTION_ID

# Install Azure Machine Learning extension
az extension add -n azure-cli-ml

# Create a resource group
az group create --name $RG_NAME --location $LOCATION

# Create an Azure Machine Learning workspace
az ml workspace create --workspace-name $WS_NAME \
--resource-group $RG_NAME --location $LOCATION