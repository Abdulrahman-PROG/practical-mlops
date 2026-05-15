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

<!-- Add future chapters below this line -->
