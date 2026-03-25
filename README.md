# Golden Signal Dashboard

Student Name: Bhavya Jain  
Registration No: 23FE10CSE00831  
Course: CSE3253 DevOps [PE6]  
Semester: VI (2025–2026)  
Project Type: Puppet / Monitoring  
Difficulty: Intermediate  

## Project Overview

The Golden Signal Dashboard is a Python Streamlit application that visualizes the four SRE golden signals—**latency**, **traffic**, **errors**, and **saturation**—using realistic sample monitoring data. It is designed for academic submission under the **Puppet / Monitoring** category and includes Docker, automated tests, GitHub Actions CI, and minimal Puppet manifests for configuration alignment.

## Problem Statement

Operators and developers often struggle to interpret scattered metrics. This project provides a single, lightweight dashboard that loads service-wise time series from a CSV file, applies clear thresholds, and surfaces **Healthy / Warning / Critical** health states alongside interactive charts.

## Objectives

- [ ] Visualize latency, traffic, errors, and saturation with charts, summary cards, and threshold-based health states  
- [ ] Provide reproducible sample data, automated tests, and GitHub Actions CI  
- [ ] Align with the Puppet / Monitoring category using Docker, documentation, and Puppet configuration samples  

## Key Features

**Feature 1** — Interactive Plotly line charts for latency, traffic, errors, and saturation, with warning/critical reference lines where applicable.  

**Feature 2** — Sidebar filters for **services** and **time window**, plus per-service health derived from thresholds.  

**Feature 3** — Reproducible sample data via `utils/generate_sample_data.py`, pytest checks, and a GitHub Actions workflow.  

## Technology Stack

### Core Technologies

Programming Language: Python  
Framework: Streamlit  
Database: None (CSV file–backed metrics)  

### DevOps Tools

Version Control: Git  
CI/CD: GitHub Actions  
Containerization: Docker  
Orchestration: Kubernetes (not used in this submission)  
Configuration Management: Puppet (sample manifests and EPP template)  
Monitoring: Application-level golden-signal dashboard (CSV-driven demo metrics)  

## Getting Started

### Prerequisites

- [ ] Docker Desktop v20.10+ *(recommended)*  
- [ ] Git 2.30+  
- [ ] Python 3.11+ *(for local runs without Docker)*  

### Installation

1. Clone the repository:

```bash
git clone https://github.com/[username]/devopsprojectgoldensignaldashboard.git
cd devopsprojectgoldensignaldashboard
```

2. Build and run using Docker:

```bash
docker build -t devopsprojectgoldensignaldashboard:latest .
docker run --rm -p 8501:8501 devopsprojectgoldensignaldashboard:latest
```

3. Access the application:

Web Interface: http://localhost:8501  

API: Not applicable (Streamlit UI reads `data/sample_metrics.csv` locally; no REST API in this submission).  

### Alternative Installation (Without Docker)

```bash
cd devopsprojectgoldensignaldashboard
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501. If `data/sample_metrics.csv` is missing, run:

```bash
python utils/generate_sample_data.py
```

## Project Structure

```text
devopsprojectgoldensignaldashboard/
├── README.md
├── app.py
├── requirements.txt
├── Dockerfile
├── .gitignore
├── LICENSE
├── data/
│   └── sample_metrics.csv
├── utils/
│   └── generate_sample_data.py
├── tests/
│   └── test_metrics_file.py
├── docs/
│   ├── architecture.md
│   ├── implementation.md
│   └── project_report.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── screenshots/
│   └── dashboard.png
└── puppet/
    ├── manifests/
    │   └── init.pp
    └── templates/
        └── dashboard.conf.epp
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory if you extend the app (optional for the base submission):

```env
APP_ENV=development
# Example placeholders — not required for CSV-only mode:
# DASHBOARD_DATA_PATH=data/sample_metrics.csv
```

### Key Configuration Files

1. `app.py` — Dashboard entrypoint and threshold constants  
2. `data/sample_metrics.csv` — Input metrics for charts and health logic  
3. `Dockerfile` — Container image for Streamlit on port 8501  
4. `puppet/manifests/init.pp` — Sample Puppet class for operator config file  

## CI/CD Pipeline

### Pipeline Stages

1. **Checkout** — Clone repository on GitHub-hosted runner  
2. **Setup Python** — Python 3.11  
3. **Install dependencies** — `pip install -r requirements.txt`  
4. **Test** — `pytest tests/ -v`  
5. **Security Scan** — Not configured in this submission *(future scope: e.g. Trivy on image)*  
6. **Deploy** — Not configured in this submission *(manual/local Docker only)*  

### Pipeline Status

![Pipeline Status](https://img.shields.io/badge/pipeline-passing-brightgreen)


## Monitoring 

### Monitoring Setup

**Dashboard:** Streamlit UI plotting latency, traffic, errors, and saturation from `data/sample_metrics.csv`.  
**Custom metrics:** File-based demo metrics; regenerate with `utils/generate_sample_data.py`.  
**Alerts:** Not implemented (thresholds are visual only in the UI).  


## Docker 

### Docker Images

```bash
# Build image
docker build -t devopsprojectgoldensignaldashboard:latest .

# Run container
docker run --rm -p 8501:8501 devopsprojectgoldensignaldashboard:latest
```

## 🚀 Live Demo
https://devopsprojectgoldensignaldashboard.streamlit.app/

## Documentation

### User Documentation

[Project Report](docs/project_report.md)  

API Documentation: Not applicable (no REST API; Streamlit reads CSV data).  

### Technical Documentation

[Architecture Overview](docs/architecture.md)  
[Implementation Guide](docs/implementation.md)  

### DevOps Documentation

Docker, CI, and Puppet notes: [Implementation Guide](docs/implementation.md)  
Troubleshooting: [Implementation Guide — Troubleshooting](docs/implementation.md#troubleshooting)  


## Development Workflow

### Git Branching Strategy

```text
main
├── develop
│   ├── feature/latency-charts
│   ├── feature/puppet-config
│   └── fix/csv-validation
└── release/v1.0.0
```

### Commit Convention

- `feat:` New feature  
- `fix:` Bug fix  
- `docs:` Documentation  
- `test:` Test-related  
- `refactor:` Code refactoring  
- `chore:` Maintenance tasks  


## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Project Challenges

1. **Balancing template breadth vs. repo simplicity** — The course template describes a large multi-folder layout; this submission uses the prescribed **flat academic tree** while keeping README sections aligned with the template.  
2. **Health logic vs. traffic** — Traffic spikes are not automatically unhealthy; health emphasizes latency, errors, and saturation.  
3. **Puppet without a full control repo** — Manifests are minimal and documented so they can be relocated into a proper module path when used with a real Puppet server.  

## Learnings

- Golden signals provide a compact mental model for service health.  
- Container images make grading and demos repeatable across machines.  
- Automated tests on CSV schema prevent silent dashboard breakage.  

## Acknowledgments

Course Instructor: Mr. Jay Shankar Sharma  
Reference materials and tutorials  
Open-source tools and libraries   
