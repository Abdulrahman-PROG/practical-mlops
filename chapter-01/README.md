# Chapter 01: Introduction to MLOps

## Summary

MLOps applies DevOps principles to machine learning — automating testing, deployment, and monitoring of models. The key idea is treating ML code like production software: lint it, test it, containerize it, and ship it through a CI/CD pipeline.

## Key Concepts

- MLOps = DevOps for ML (automation, reproducibility, monitoring)
- Makefile as a task runner: `install`, `format`, `lint`, `test`
- GitHub Actions for CI across multiple Python versions
- Docker for containerizing ML apps
- Load testing with Locust to validate performance under traffic

## Exercises

| Exercise | Files |
|----------|-------|
| Python scaffolding with Makefile, linting, testing | [code/](code/) |
| CI with GitHub Actions (Python 3.10 & 3.11) | [.github/workflows/ci.yml](code/.github/workflows/ci.yml) |
| Docker container build | [Dockerfile](code/Dockerfile) |
| Load test on staging branch push | [locustfile.py](code/locustfile.py), [.github/workflows/load-test.yml](code/.github/workflows/load-test.yml) |

## Critical Thinking Discussion Questions

**1. What problems does a CI system solve?**

Without CI, developers integrate code manually and rarely — leading to "integration hell" where merging large changes breaks everything at once. CI solves this by automatically running tests on every push, catching bugs early when they're cheap to fix. It also enforces code quality (linting, formatting) and gives the team confidence that the main branch always works.

---

**2. Why is a CI system essential for both SaaS products and ML systems?**

For SaaS, CI ensures every code change is tested before reaching users — preventing downtime and regressions. For ML systems the stakes are higher: a broken model can silently produce wrong predictions without any obvious error. CI for ML also tests data pipelines, model training scripts, and inference code — not just application logic. Without it, ML systems degrade quietly.

---

**3. Why are cloud platforms ideal for analytics? How do data engineering and DataOps help?**

Analytics needs elastic compute (big queries, training jobs) and storage (data lakes, warehouses) that you only pay for when you use them — exactly what cloud provides. On-premise infrastructure is either over-provisioned (expensive) or under-provisioned (slow). Data engineering builds the pipelines that move and transform raw data into something usable. DataOps applies CI/CD principles to those pipelines — versioning, testing, and automating data flows so analytics results are reliable and reproducible.

---

**4. How does deep learning benefit from the cloud? Is it feasible without it?**

Deep learning requires GPUs/TPUs for training, massive datasets for storage, and distributed compute for large models — all available on-demand in the cloud. Without cloud, you'd need to buy and maintain expensive hardware that sits idle between experiments. For a student or small team, training a serious model without cloud is nearly impossible. Even large companies use cloud because buying enough GPUs to match cloud scale is cost-prohibitive and inflexible.

---

**5. What is MLOps and how does it enhance ML engineering?**

MLOps is the practice of applying software engineering discipline — CI/CD, testing, monitoring, version control — to the full ML lifecycle: data, training, deployment, and retraining. Without MLOps, models are trained in notebooks, deployed manually, and never monitored. They drift, break silently, and can't be reproduced. MLOps turns a one-time experiment into a maintainable, production-grade system that improves over time.

---

## File Structure

```
code/
├── hello.py          # core logic
├── app.py            # Flask web app
├── test_hello.py     # pytest tests
├── locustfile.py     # Locust load test
├── Makefile          # install / format / lint / test / load-test
├── requirements.txt
├── Dockerfile
└── .github/
    └── workflows/
        ├── ci.yml         # runs on push to main (Python 3.10 & 3.11)
        └── load-test.yml  # runs on push to staging
```
