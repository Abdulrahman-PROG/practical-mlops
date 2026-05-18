#!/bin/bash
# Deploy the ONNX container to Azure Container Instances
# Run this script after the image is pushed to ACR

ACR_NAME="mlopsacrabdulrahman"
RESOURCE_GROUP="mlops-rg"
LOCATION="uaenorth"
CONTAINER_NAME="iris-onnx-aci"
IMAGE="${ACR_NAME}.azurecr.io/iris-onnx:latest"

echo "Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

echo "Creating Azure Container Registry..."
az acr create \
  --name $ACR_NAME \
  --resource-group $RESOURCE_GROUP \
  --sku Basic \
  --admin-enabled true

echo "Getting ACR credentials..."
ACR_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

echo "ACR Login Server: $ACR_SERVER"

echo "Building and pushing image to ACR..."
az acr build \
  --registry $ACR_NAME \
  --image iris-onnx:latest \
  .

echo "Deploying to Azure Container Instances..."
az container create \
  --resource-group $RESOURCE_GROUP \
  --name $CONTAINER_NAME \
  --image $IMAGE \
  --registry-login-server $ACR_SERVER \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --ports 5000 \
  --dns-name-label iris-onnx-abdulrahman \
  --cpu 1 \
  --memory 1.5

echo ""
echo "Deployed! App is live at:"
az container show \
  --resource-group $RESOURCE_GROUP \
  --name $CONTAINER_NAME \
  --query ipAddress.fqdn -o tsv
