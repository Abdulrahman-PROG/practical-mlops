# Chapter 01 — Slides Outline
## "Introduction to MLOps | Practical MLOps Series"

---

### Slide 1 — Title
**Title:** Introduction to MLOps
**Subtitle:** Practical MLOps Series — Chapter 1
**Bottom:** Book: Practical MLOps by Noah Gift & Alfredo Deza

---

### Slide 2 — What You'll Learn
- What MLOps is and why it exists
- How to set up a Python project with a Makefile
- CI/CD with GitHub Actions (multi-Python)
- Containerizing with Docker
- Automated load testing with Locust

---

### Slide 3 — The Problem
**Title:** Why does MLOps exist?

**Left side (Without MLOps):**
- Model lives in a notebook
- Manual deployment
- "Works on my machine"
- No monitoring
- Not reproducible

**Right side (With MLOps):**
- Code versioned in Git
- Automated pipelines
- Same environment everywhere
- Monitored continuously
- Fully reproducible

---

### Slide 4 — What is MLOps?
**Title:** MLOps = ML + DevOps + Data Engineering

**Center diagram (3 overlapping circles):**
- Machine Learning
- DevOps
- Data Engineering
- Center: **MLOps**

**Quote:** "MLOps is the intersection of machine learning, DevOps, and data engineering"

---

### Slide 5 — Project Structure
**Title:** What We Built

```
chapter-01/code/
├── hello.py          ← core logic
├── app.py            ← Flask web app
├── test_hello.py     ← pytest tests
├── locustfile.py     ← load test
├── Makefile          ← automation
├── Dockerfile        ← container
└── .github/
    └── workflows/
        ├── ci.yml         ← CI pipeline
        └── load-test.yml  ← staging test
```

---

### Slide 6 — The Makefile
**Title:** Makefile — One Command to Rule Them All

```makefile
make install   # pip install -r requirements.txt
make format    # black *.py
make lint      # pylint hello.py
make test      # pytest test_hello.py -v
make all       # all of the above
```

**Key point:** No more remembering commands. One word does everything.

---

### Slide 7 — GitHub Actions CI
**Title:** Automated Testing on Every Push

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11"]
```

**Flow diagram:**
```
git push → GitHub Actions triggers
               ↓
    Python 3.10 ──┬── Python 3.11
                  ↓
    install → format → lint → test → docker build
```

---

### Slide 8 — Docker
**Title:** Containerize Everything

**Why Docker?**
- Same environment on every machine
- Easy to deploy anywhere
- No "works on my machine" problems

```dockerfile
FROM python:3.11-slim
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

---

### Slide 9 — Load Testing with Locust
**Title:** Does Your App Survive Real Traffic?

**Trigger:** Push to `staging` branch
**What happens:**
- App starts automatically
- Locust hits it with 10 users for 30 seconds
- Tests `/` and `/add` endpoints

**Key point:** Performance problems caught before production

---

### Slide 10 — The Full Pipeline
**Title:** Everything Connected

```
You write code
      ↓
git push to main
      ↓
GitHub Actions: format → lint → test → docker build
      ↓
git push to staging
      ↓
Load test runs automatically (Locust)
      ↓
Confidence to deploy to production
```

---

### Slide 11 — Key Takeaways
- MLOps = treating ML code like production software
- Makefile = simple automation for any project
- CI/CD catches bugs before users see them
- Docker = reproducible environments
- Load testing = confidence under real traffic
- All of this runs **automatically** — you just push code

---

### Slide 12 — Next Chapter
**Title:** Coming Up — Chapter 2: MLOps Foundations

- Build a real ML prediction API (housing prices)
- Deploy to Azure App Service
- Set up continuous delivery with Azure Pipelines
- Traveling Salesman with real restaurant data

**Subscribe for Chapter 2!**

---
