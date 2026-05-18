#!/bin/bash
# Delete all Azure resources to save credits

az group delete --name mlops-rg --yes --no-wait
echo "Deleting resource group mlops-rg (ACR + ACI)... done"
