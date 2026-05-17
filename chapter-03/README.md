# Chapter 03: MLOps for Containers and Edge Devices

## Summary

This chapter covers containers as the core packaging unit for MLOps. Containers solve the "works on my machine" problem by bundling code, dependencies, and runtime into one portable image. The chapter covers Docker fundamentals, container security (vulnerability scanning), serving ML models over HTTP inside containers, and deploying models to edge devices like the Coral TPU. The key MLOps pattern: **build once, run anywhere** — same container on your laptop, CI server, and cloud.

## Key Concepts

- Containers vs. VMs: containers share the OS kernel — lighter, faster, portable
- Docker image = blueprint | Docker container = running instance
- Dockerfile best practices: use slim base images, minimize layers, never store secrets
- Edge = compute that runs close to the data source (phone, sensor, TPU device)
- Coral TPU: Google's edge accelerator for TensorFlow Lite models
- Build once, run many: the MLOps container workflow

## Exercises

| Exercise | Folder | What it does |
|----------|--------|-------------|
| Flask model server with examples + metadata | [model-container/](code/model-container/) | Iris classifier with `/predict`, `/examples`, `/metadata` endpoints |

> **Coral TPU / MobileNet V2 exercises** require physical hardware (Coral USB Accelerator). Steps are documented below for reference.

## How to Run

### Locally
```bash
cd code/model-container
make all          # install, train, format, lint, test
python app.py     # runs on http://localhost:5000
```

Test the endpoints:
```bash
# See available endpoints
curl http://localhost:5000/

# Get sample inputs
curl http://localhost:5000/examples

# Get model metadata
curl http://localhost:5000/metadata

# Make a prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

### With Docker
```bash
cd code/model-container

# Build the image (trains model inside container)
make build
# or: docker build -t iris-classifier .

# Run the container
make run
# or: docker run -p 5000:5000 iris-classifier

# Test it
curl http://localhost:5000/examples
```

### Publish to Docker Hub
```bash
# Login to Docker Hub
docker login

# Tag the image with your username
docker tag iris-classifier <your-dockerhub-username>/iris-classifier:v1

# Push to Docker Hub
docker push <your-dockerhub-username>/iris-classifier:v1

# Anyone can now pull and run it
docker run -p 5000:5000 <your-dockerhub-username>/iris-classifier:v1
```

### Coral TPU / MobileNet V2 (requires hardware)
```bash
# Install Edge TPU runtime
pip install tflite-runtime

# Download MobileNet V2 TFLite model from TFHub
# Compile for Edge TPU using edgetpu_compiler
edgetpu_compiler mobilenet_v2.tflite

# Run inference on Coral device
python coral_inference.py --model mobilenet_v2_edgetpu.tflite --image photo.jpg
```

## Critical Thinking Discussion Questions

**1. Can a container perform online predictions with an edge TPU like Coral?**

Yes — with some conditions. You can run a Docker container on a device that has the Coral USB Accelerator attached, as long as: (1) the container has access to the USB device (`--device /dev/bus/usb`), (2) the Edge TPU runtime is installed inside the container, and (3) the model is compiled for the Edge TPU (`.tflite` with EdgeTPU delegate). The container handles the software environment; the TPU handles the acceleration. This is actually a good MLOps pattern — reproducible inference environment on edge hardware.

---

**2. What is a container runtime, and how does it relate to Docker?**

A container runtime is the low-level software that actually runs containers — it handles creating, starting, stopping, and deleting containers using OS primitives (namespaces, cgroups). Docker is a higher-level tool that includes a CLI, image builder, registry client, and uses a container runtime underneath. The most common runtime Docker uses is `containerd`, which itself uses `runc`. Think of it as: Docker = user-friendly wrapper, container runtime = the engine doing the actual work.

---

**3. Three good practices when creating a Dockerfile:**

1. **Use slim or alpine base images** — `python:3.11-slim` instead of `python:3.11` reduces image size and attack surface
2. **Copy requirements first, then code** — lets Docker cache the dependency layer; only rebuilds it when requirements.txt changes
3. **Never store secrets in the image** — no API keys, passwords, or `.env` files in the Dockerfile; use environment variables at runtime

---

**4. Two critical DevOps concepts from this chapter:**

1. **Build once, run anywhere** — build the container image once in CI, then deploy that exact same image to staging and production. No environment drift, no surprises.
2. **Continuous Integration** — every code change automatically builds and tests the container, catching problems before they reach production.

These are useful because they eliminate the two most common causes of production failures: environment inconsistency and untested code.

---

**5. What is "the edge"? ML examples:**

The edge is any compute that happens close to where data is generated — on the device itself — rather than sending data to a central cloud server. It reduces latency, saves bandwidth, and works offline.

ML examples at the edge:
- **Phone camera** — face unlock runs a model locally on the device, not in the cloud
- **Coral TPU on a security camera** — detects objects in real time without internet
- **Raspberry Pi in a factory** — detects defective products on a production line
- **Smart speaker** — wake-word detection runs on-device; only sends audio to cloud after activation
