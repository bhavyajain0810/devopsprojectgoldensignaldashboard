"""Tests for sample metrics data and health threshold helpers."""

from pathlib import Path

import pandas as pd
import pytest

# Import app module from repository root when pytest is run from project root
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import app  # noqa: E402


REQUIRED_COLUMNS = [
    "timestamp",
    "service",
    "latency_p95_ms",
    "traffic_rpm",
    "error_rate_pct",
    "saturation_cpu_pct",
]


@pytest.fixture
def metrics_path() -> Path:
    return ROOT / "data" / "sample_metrics.csv"


def test_sample_metrics_file_exists(metrics_path: Path) -> None:
    assert metrics_path.is_file(), "data/sample_metrics.csv must exist for the dashboard"


def test_sample_metrics_schema_and_non_empty(metrics_path: Path) -> None:
    df = pd.read_csv(metrics_path)
    for col in REQUIRED_COLUMNS:
        assert col in df.columns, f"Missing column: {col}"
    assert len(df) > 0, "Sample data should contain at least one row"
    assert df["service"].nunique() >= 1


def test_timestamps_parse_as_datetime(metrics_path: Path) -> None:
    df = pd.read_csv(metrics_path)
    parsed = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    assert parsed.notna().all(), "All timestamps must be valid ISO datetimes"


def test_health_status_known_values() -> None:
    assert app.health_for_row(100, 2.0, 50.0) in ("Healthy", "Warning", "Critical")
    assert app.health_for_row(600, 0.1, 50.0) == "Critical"
    assert app.health_for_row(100, 0.1, 50.0) == "Healthy"


def test_load_metrics_returns_dataframe(metrics_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)
    df = app.load_metrics()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
