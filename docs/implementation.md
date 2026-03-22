# Implementation Guide — Golden Signal Dashboard

## Runtime stack

- **Python 3.11+**
- **Streamlit** — UI shell
- **Pandas** — CSV loading and aggregation
- **Plotly** — interactive charts
- **Pytest** — tests in `tests/`

## Data schema

`data/sample_metrics.csv` columns:

| Column | Meaning |
|--------|---------|
| `timestamp` | ISO 8601 UTC timestamp |
| `service` | Logical service name (e.g. `api-gateway`) |
| `latency_p95_ms` | End-to-end style latency, 95th percentile (ms) |
| `traffic_rpm` | Requests per minute |
| `error_rate_pct` | Error percentage (0–100 scale) |
| `saturation_cpu_pct` | CPU utilization proxy (%) |

Regenerate the file:

```bash
python utils/generate_sample_data.py
```

## Thresholds (health)

Defined in `app.py`:

| Signal | Warning | Critical |
|--------|---------|----------|
| Latency (p95) | ≥ 200 ms | ≥ 500 ms |
| Errors | ≥ 1% | ≥ 5% |
| Saturation (CPU) | ≥ 70% | ≥ 85% |

Traffic is shown on charts and summary averages but does not drive the red/yellow/green health label by itself.

## Local run (without Docker)

```bash
cd devopsprojectgoldensignaldashboard
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open **http://localhost:8501**.

## Docker deployment

From the repository root:

```bash
docker build -t devopsprojectgoldensignaldashboard:latest .
docker run --rm -p 8501:8501 devopsprojectgoldensignaldashboard:latest
```

Browse to **http://localhost:8501**.

## CI

GitHub Actions workflow **`.github/workflows/ci.yml`** installs `requirements.txt` and runs:

```bash
pytest tests/ -v
```

## Puppet (sample)

`puppet/manifests/init.pp` defines class `golden_signal_dashboard` that writes `/etc/golden-signal-dashboard/dashboard.conf` using `inline_epp` with the same parameter shape as `puppet/templates/dashboard.conf.epp`.

For a real control repository, place these files under a module such as `modules/golden_signal_dashboard/` and use `include golden_signal_dashboard` on target nodes.

## Troubleshooting

- **“Data file not found”** — Ensure `data/sample_metrics.csv` exists; run `python utils/generate_sample_data.py`.
- **Port already in use** — Change the host port: `docker run -p 8600:8501 ...` or pass Streamlit flags when running locally.
- **Empty charts** — Widen the sidebar time window or select more services.

## Future scope (not implemented)

- Live scrape from Prometheus or OpenTelemetry
- Authentication and multi-tenant RBAC
- Alert routing to email/Slack
