#!/bin/bash

WS_NAME="sre-ml-workspace"
RG_NAME="sre-ml-rg"
LOCATION="eastus"

# Sign in to Azure
az login

# Install Azure Machine Learning extension
az extension add -n azure-cli-ml

# Create a resource group
az group create --name $RG_NAME --location $LOCATION

# Create an Azure Machine Learning workspace
az ml workspace create --workspace-name $WS_NAME \
--resource-group $RG_NAME --location $LOCATION