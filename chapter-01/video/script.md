# Chapter 01 — Video Script
## "Introduction to MLOps | Practical MLOps Series"

---

### INTRO (0:00 - 0:45)

Hey everyone, welcome to the Practical MLOps series.

In this series, we're going chapter by chapter through the book
"Practical MLOps" by Noah Gift and Alfredo Deza — and for each chapter
we'll cover the theory, write real code, and deploy real things to the cloud.

This is Chapter 1 — Introduction to MLOps.

By the end of this video you'll know:
- What MLOps actually is and why it exists
- The full CI/CD pipeline we built from scratch
- How to automatically test, lint, containerize, and load test your code

Let's get into it.

---

### PART 1 — What is MLOps? (0:45 - 2:30)

So what is MLOps?

Think about a data scientist who trains a great model in a Jupyter notebook.
It works perfectly on their laptop. Then they hand it to engineering and say
"put this in production" — and everything breaks.

That's the problem MLOps solves.

MLOps stands for Machine Learning Operations.
It's what happens when you take the best practices from software engineering —
things like version control, automated testing, CI/CD pipelines —
and apply them to machine learning systems.

Without MLOps:
- Models live in notebooks, not servers
- Deployments are manual and error-prone
- Nobody monitors if the model is still working correctly
- Results can't be reproduced

With MLOps:
- Code is versioned in Git
- Every change is automatically tested
- Models are deployed through pipelines, not by hand
- Performance is monitored continuously

The book defines it simply: MLOps is the intersection of
Machine Learning, DevOps, and Data Engineering.

---

### PART 2 — The CI/CD Pipeline We Built (2:30 - 5:00)

Now let's look at the actual code we built for this chapter.

[SHOW SCREEN — VS Code with chapter-01/code]

We built five things:

**1. A Python project with a Makefile**

The Makefile is the heart of our automation.
Instead of remembering 10 different commands, you just run:

  make install   — installs all dependencies
  make format    — auto-formats code with Black
  make lint      — checks code quality with Pylint
  make test      — runs all tests with Pytest
  make all       — does all four in one command

[SHOW Makefile]

**2. A simple Flask web app**

We have a Flask app with two endpoints:
- GET /  returns a hello message
- GET /add/3/5  returns the sum

[SHOW app.py]

**3. Tests with Pytest**

Every function has a test. If the code breaks, the test catches it
before it ever reaches production.

[SHOW test_hello.py]

**4. GitHub Actions CI — two Python versions**

This is where it gets powerful.

Every time we push to GitHub, this workflow automatically runs
on Python 3.10 AND Python 3.11 — in parallel.

It installs, formats, lints, and tests — all without us doing anything.

[SHOW .github/workflows/ci.yml]

**5. Docker container**

The Dockerfile packages the entire app into a container.
Same environment everywhere — your laptop, the server, the cloud.

[SHOW Dockerfile]

**6. Load testing with Locust**

When we push to the staging branch, Locust automatically
hammers the app with 10 users for 30 seconds to make sure
it can handle real traffic.

[SHOW locustfile.py]

---

### PART 3 — Why This Matters (5:00 - 6:30)

Let me show you the full picture.

[SHOW diagram on slide]

You write code → push to GitHub
GitHub Actions detects the push
Runs: format check → lint → tests → docker build
If everything passes → deploy to staging
Staging branch push → load test runs automatically

This entire pipeline runs without you touching anything.

That's the point of MLOps.
Not just writing good models — but building systems that
keep those models working reliably in production, automatically.

---

### OUTRO (6:30 - 7:00)

That's Chapter 1 done.

We covered what MLOps is, built a complete CI/CD pipeline,
containerized our app with Docker, and added automated load testing.

All the code is on GitHub — link in the description.

In Chapter 2 we go deeper — MLOps Foundations.
We'll build a real ML prediction API, deploy it to Azure App Service,
and set up continuous delivery so every git push auto-deploys.

If this was helpful, subscribe and I'll see you in the next one.

---
