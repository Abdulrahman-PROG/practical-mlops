# Azure — What We Did

A running log of every Azure technology and command used throughout this study repo.

---

## Chapter 02 — Deploy ML Flask App to Azure App Service

### Technologies Used

| Technology | What it is |
|------------|-----------|
| **Azure App Service** | Managed platform to host web apps without managing servers |
| **Azure App Service Plan** | The underlying server — defines region, OS, and pricing tier |
| **Azure Resource Group** | Logical container that groups all related resources together |

### Commands

```bash
# Login with tenant ID (required for student/org accounts)
az login --tenant <your-tenant-id>

# Verify active subscription
az account show --query "{name:name, id:id}" -o table

# Check which regions your subscription allows
az policy assignment list --query "[0].parameters" -o json

# Create a resource group in an allowed region
az group create --name mlops-rg --location uaenorth

# Deploy Flask app to App Service (run from app folder)
az webapp up \
  --name flask-mlops-abdulrahman \
  --resource-group mlops-rg \
  --runtime "PYTHON:3.11" \
  --sku FREE \
  --location uaenorth

# Redeploy after any code change
az webapp up

# Delete everything to save credits
az group delete --name mlops-rg --yes --no-wait
```

### Live URL (deleted to save credits)
```
http://flask-mlops-abdulrahman.azurewebsites.net
```

### What Azure did automatically
1. Created App Service Plan (the server)
2. Created the Web App
3. Zipped and uploaded the code
4. Installed `requirements.txt`
5. Started the app

---

## Chapter 04 — ONNX Container on Azure Container Registry + Container Instances

### Technologies Used

| Technology | What it is |
|------------|-----------|
| **Azure Container Registry (ACR)** | Private Docker image registry on Azure — store and version your container images |
| **Azure Container Instances (ACI)** | Run containers directly without managing servers or Kubernetes |
| **Azure Resource Group** | Same as before — groups ACR + ACI together for easy cleanup |

### Architecture

```
Local code
    ↓
az acr build  →  Azure Container Registry (stores image)
                          ↓
              az container create  →  Azure Container Instances (runs image)
                                              ↓
                                  http://iris-onnx-abdulrahman.uaenorth.azurecontainer.io:5000
```

### Step-by-Step Commands

```bash
# 1. Login
az login --tenant 734604f1-7b61-4862-83af-872c0a345c53

# 2. Create resource group
az group create --name mlops-rg --location uaenorth

# 3. Create Azure Container Registry
az acr create \
  --name mlopsacrabdulrahman \
  --resource-group mlops-rg \
  --sku Basic \
  --admin-enabled true

# 4. Build and push image directly to ACR (no local Docker needed)
cd chapter-04/code/onnx-container
az acr build \
  --registry mlopsacrabdulrahman \
  --image iris-onnx:latest \
  .

# 5. Get ACR credentials
ACR_SERVER=$(az acr show --name mlopsacrabdulrahman --query loginServer -o tsv)
ACR_USERNAME=$(az acr credential show --name mlopsacrabdulrahman --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name mlopsacrabdulrahman --query "passwords[0].value" -o tsv)

# 6. Deploy to Azure Container Instances
az container create \
  --resource-group mlops-rg \
  --name iris-onnx-aci \
  --image mlopsacrabdulrahman.azurecr.io/iris-onnx:latest \
  --registry-login-server $ACR_SERVER \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --ports 5000 \
  --dns-name-label iris-onnx-abdulrahman \
  --cpu 1 \
  --memory 1.5

# 7. Get the live URL
az container show \
  --resource-group mlops-rg \
  --name iris-onnx-aci \
  --query ipAddress.fqdn -o tsv

# 8. Test it
curl http://<fqdn>:5000/health
curl -X POST http://<fqdn>:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'

# 9. Delete everything to save credits
az group delete --name mlops-rg --yes --no-wait
```

### Or use the deploy script
```bash
cd chapter-04/code/onnx-container
bash deploy_aci.sh    # creates ACR, builds image, deploys to ACI
bash destroy_aci.sh   # deletes everything
```

### GitHub Actions — Auto push to ACR on every commit
Add these secrets to your GitHub repo (Settings → Secrets → Actions):
- `ACR_LOGIN_SERVER` = `mlopsacrabdulrahman.azurecr.io`
- `ACR_USERNAME` = output of `az acr credential show --name mlopsacrabdulrahman --query username -o tsv`
- `ACR_PASSWORD` = output of `az acr credential show --name mlopsacrabdulrahman --query "passwords[0].value" -o tsv`

Workflow file: [azure-acr.yml](chapter-04/code/onnx-container/.github/workflows/azure-acr.yml)

---

<!-- Add future chapters below this line -->
