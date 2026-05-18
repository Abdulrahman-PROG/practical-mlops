# Chapter 04: Continuous Delivery for Machine Learning Models

## Summary

This chapter is about automating the full journey of an ML model from training to production. The core idea is that every step — packaging, testing, building, and deploying — should be automated and triggered by code changes. It covers containerizing ML models with Docker, pushing images to registries, using ONNX for model portability, and two controlled rollout strategies: blue-green and canary deployments. Cloud pipelines (SageMaker, Azure ML) are shown as alternatives to GitHub Actions for more complex ML workflows.

## Key Concepts

- Packaging a model = wrapping it with its dependencies in a Docker container so it runs identically everywhere
- ONNX = Open Neural Network Exchange — a standard format to run models from any framework (sklearn, PyTorch, TensorFlow) with one runtime
- CI/CD pipeline = automated chain: code push → test → build container → push to registry → deploy
- Blue-green deployment = two identical environments; switch traffic after verification
- Canary deployment = gradually route a small % of traffic to new model, monitor, then increase
- Shift left = catch errors earlier in the pipeline, not at production

## Exercises

| Exercise | Folder | What it does |
|----------|--------|-------------|
| Flask container + GitHub Actions CI | [flask-container/](code/flask-container/) | Iris classifier in Docker, auto-tested on every push |
| ONNX container → Docker Hub | [onnx-container/](code/onnx-container/) | ONNX model served via Flask, auto-pushed to Docker Hub on push to main |

## How to Run

### Exercise 1 — Flask Container

```bash
cd code/flask-container
make all          # install, train, format, lint, test
make build        # docker build -t iris-flask-cd .
make run          # docker run -p 5000:5000 iris-flask-cd

# Test
curl http://localhost:5000/health
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

### Exercise 2 — ONNX Container → Docker Hub

```bash
cd code/onnx-container
make all          # install, train onnx model, format, lint, test
make build        # docker build -t iris-onnx .
make run          # docker run -p 5000:5000 iris-onnx

# Push manually
make push         # tags and pushes to b0daelbanna/iris-onnx:v1
```

#### Setup Docker Hub secrets in GitHub (for auto-push on every commit)

1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Add two secrets:
   - `DOCKERHUB_USERNAME` = `b0daelbanna`
   - `DOCKERHUB_TOKEN` = your Docker Hub access token
     (Docker Hub → Account Settings → Security → New Access Token)
3. Every push to `main` will now automatically build and push the image to:
   `b0daelbanna/iris-onnx:latest` and `b0daelbanna/iris-onnx:<commit-sha>`

### Four Checks to Verify a Packaged Model Container

These are built into the CI workflow:

```bash
# 1. Container builds successfully
docker build -t iris-flask-cd .

# 2. Health endpoint responds with 200
curl --fail http://localhost:5000/health

# 3. Predict endpoint returns valid JSON
curl -X POST http://localhost:5000/predict ...

# 4. Lint passes — no code quality issues
pylint --disable=R,C app.py
```

## Blue-Green vs Canary Deployment

### Blue-Green
```
Production (Blue) ──── 100% traffic
Staging   (Green) ──── 0% traffic  ← new model deployed here

After testing:
Production (Blue) ──── 0% traffic
Staging   (Green) ──── 100% traffic  ← instant switch
```
- Safe: easy to roll back (just switch back)
- Expensive: need two full environments running

### Canary
```
Model v1 ──── 90% traffic
Model v2 ──── 10% traffic  ← new model gets a slice

If metrics look good:
Model v1 ──── 50% → 0%
Model v2 ──── 50% → 100%
```
- Gradual: real users test the new model
- Safer for ML: catch accuracy/drift issues before full rollout
- Preferred for ML models because a bad model can be silent — it doesn't crash, it just predicts wrong

## Critical Thinking Discussion Questions

**1. Four critical checks to verify a packaged model container:**

1. **Health endpoint** — `GET /health` returns 200, confirming the app started and model loaded
2. **Prediction endpoint** — `POST /predict` with known input returns correct output and valid JSON
3. **Port is exposed and reachable** — container is actually listening on the right port
4. **Lint/format check** — code quality passes before the image is built

---

**2. Blue-green vs canary — which is better?**

Blue-green is simpler and faster to roll back — flip a switch and you're done. Canary is safer for ML because it exposes the new model to real traffic gradually, letting you catch accuracy degradation or unexpected behavior before it affects everyone. For ML models specifically, canary is preferred — a bad model doesn't throw errors, it just makes wrong predictions silently, so gradual rollout with monitoring is the right approach.

---

**3. Cloud pipelines vs GitHub Actions — three differences:**

| | GitHub Actions | Cloud Pipelines (SageMaker/Azure ML) |
|---|---|---|
| **Purpose** | General CI/CD for code | Purpose-built for ML workflows |
| **ML features** | None built-in | Model registry, data versioning, experiment tracking |
| **Step reuse** | YAML jobs | Reusable pipeline components with typed inputs/outputs |

Cloud pipelines also handle distributed training, GPU provisioning, and data lineage out of the box — things GitHub Actions wasn't designed for.

---

**4. What does packaging a container mean? Why is it useful?**

Packaging = taking your model + code + dependencies + runtime and bundling them into a single Docker image that runs identically on any machine. It's useful because it eliminates environment drift — the exact same image runs on your laptop, CI server, and production cloud. No more "it worked in dev but broke in prod."

---

**5. Three characteristics of packaged ML models:**

1. **Reproducible** — same image always produces the same predictions, regardless of where it runs
2. **Versioned** — each image is tagged (e.g. `v1`, `git-sha`) so you can roll back to any previous version
3. **Self-contained** — the model, its dependencies, and the serving code are all in one artifact; no external setup required
