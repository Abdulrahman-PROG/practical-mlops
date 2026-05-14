# Chapter 02: MLOps Foundations

## Summary

This chapter builds the foundational skills for MLOps: Linux/Bash basics, cloud computing concepts, Python essentials, math for ML (descriptive statistics, optimization), and core ML concepts (supervised, unsupervised, reinforcement learning). It ends with a full end-to-end example of deploying an ML pipeline using GitHub, CI/CD, and a cloud platform.

## Key Concepts

- Bash scripting and Linux fundamentals are non-negotiable for MLOps
- Cloud = elastic compute + storage + managed services on demand
- A data science workflow has four stages: Ingest → EDA → Modeling → Conclusion
- MLOps closes the gap between "model in notebook" and "model in production"
- Kaizen: continuous, small improvements applied to ML projects

## Exercises

| Exercise | Folder | What it does |
|----------|--------|-------------|
| Hello World Flask app with CI | [hello-flask/](code/hello-flask/) | Flask app with Makefile, linting, tests, GitHub Actions CI |
| ML prediction Flask app | [ml-flask/](code/ml-flask/) | Linear regression model served via Flask `/predict` endpoint |
| Traveling Salesman with real API | [traveling-salesman/](code/traveling-salesman/) | TSP solver using restaurant coords from OpenStreetMap |

## How to Run

**Hello Flask:**
```bash
cd code/hello-flask
make all          # install, format, lint, test
python app.py     # runs on http://localhost:5000
```

**ML Flask (housing price prediction):**
```bash
cd code/ml-flask
make all          # install, train model, format, lint, test
python app.py     # runs on http://localhost:5000
# Test it:
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"size_sqft": 1500, "bedrooms": 3}'
```

**Traveling Salesman:**
```bash
cd code/traveling-salesman
make all          # install, format, lint, test
python tsp.py Cairo   # fetches real restaurants and finds optimal route
```

## Azure Deployment — MLOps Pipeline from Zero

Deploy the ML Flask app to Azure App Service with continuous delivery.

### Prerequisites
- Azure account with active subscription
- Azure CLI installed (`brew install azure-cli`)

### Step 1 — Login to Azure
```bash
az login --tenant <your-tenant-id>
# verify subscription
az account show --query "{name:name, id:id}" -o table
```

### Step 2 — Check allowed regions for your subscription
```bash
az policy assignment list --query "[0].parameters" -o json
```

### Step 3 — Create a resource group
```bash
az group create --name mlops-rg --location uaenorth
```
> Use a region allowed by your subscription policy (e.g. `uaenorth`, `francecentral`)

### Step 4 — Deploy the app
```bash
cd chapter-02/code/ml-flask

az webapp up \
  --name flask-mlops-abdulrahman \
  --resource-group mlops-rg \
  --runtime "PYTHON:3.11" \
  --sku FREE \
  --location uaenorth
```

Azure will automatically:
1. Create an App Service Plan (the server)
2. Create the Web App
3. Zip and upload your code
4. Install `requirements.txt`
5. Start the app

### Step 5 — Test the live app
```bash
# Check it's running
curl http://flask-mlops-abdulrahman.azurewebsites.net/

# Get a prediction
curl -X POST http://flask-mlops-abdulrahman.azurewebsites.net/predict \
  -H "Content-Type: application/json" \
  -d '{"size_sqft": 1500, "bedrooms": 3}'
```

### Step 6 — Redeploy after changes
Any time you change the code, just run:
```bash
az webapp up
```
Azure remembers the defaults from the previous deploy.

### What was deployed

```
Your Mac  →  az webapp up  →  Azure App Service (UAE North)
                                      │
                              mlops-rg (resource group)
                                      │
                              abdoelbanna240_asp (App Service Plan)
                                      │
                              flask-mlops-abdulrahman (Web App)
                                      │
                              http://flask-mlops-abdulrahman.azurewebsites.net
```

### Live URL
```
http://flask-mlops-abdulrahman.azurewebsites.net
```

---

## Critical Thinking Discussion Questions

**1. GPU company: buy hardware vs. stay on cloud?**

The "buy hardware" argument has merit — if you're running GPUs 24/7, the per-hour cloud cost can exceed ownership cost within 2–3 years. Access to specialized hardware faster is also real. But the "stay on cloud" argument wins in most cases: owning hardware means bearing the full operational burden (cooling, networking, failure, upgrades), losing elasticity for burst workloads, and locking into today's GPU generation. The right answer depends on utilization rate and team capacity. A hybrid approach — reserved cloud instances for baseline, on-demand for spikes — is often optimal.

---

**2. Successful on-premise data center vs. cloud-native: who's right?**

The Red Hat engineer's data center success is real — but it's fragile. Losing data center engineers to Google (brain drain) and having no disaster recovery plan are existential risks for an e-commerce company. The Google architect is correct: owning infrastructure is a liability disguised as an asset when your core business is not infrastructure. A single unrecoverable outage during peak sales season costs far more than years of cloud bills. The e-commerce company should migrate.

---

**3. AWS Lambda vs. AWS Elastic Beanstalk — key differences:**

| | Lambda | Elastic Beanstalk |
|---|---|---|
| Model | Serverless, event-driven | Managed PaaS, always-on |
| Scaling | Automatic, per-request | Auto-scaling groups |
| Cost | Pay per invocation | Pay for EC2 time |
| Cold start | Yes (latency spike) | No |
| Best for | Short tasks, event triggers | Long-running web apps, APIs |
| MLOps fit | Lightweight inference, triggers | Full model serving APIs |

---

**4. Why is a managed file service (EFS / Google Filestore) useful in MLOps?**

ML workflows across multiple machines need shared access to the same datasets, model artifacts, and checkpoints. A managed file service acts as a shared filesystem — training nodes read the same data, checkpoints are written to one place, and serving nodes pick up the latest model without manual copying. It solves the "where does the model live?" problem in distributed MLOps pipelines cleanly and without building custom sync logic.

---

**5. How can Kaizen be applied to ML projects?**

Kaizen asks: *can we do better this week?* Applied to ML: pick one thing to improve each iteration — data quality, feature engineering, model evaluation, deployment speed, or monitoring coverage. Don't try to fix everything at once. Track a baseline metric, make a small targeted change, measure the result. Over time, small consistent improvements compound into a production-grade system. This is exactly how the best ML teams operate: not big-bang rewrites, but steady incremental progress.
