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
