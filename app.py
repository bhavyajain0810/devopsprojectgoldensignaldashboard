"""
Golden Signal Dashboard — Streamlit app (Latency, Traffic, Errors, Saturation).
Loads metrics from data/sample_metrics.csv.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_FILE = Path(__file__).resolve().parent / "data" / "sample_metrics.csv"

# Thresholds (documented in docs/implementation.md)
LATENCY_WARNING_MS = 200
LATENCY_CRITICAL_MS = 500
ERROR_WARNING_PCT = 1.0
ERROR_CRITICAL_PCT = 5.0
SAT_WARNING_PCT = 70.0
SAT_CRITICAL_PCT = 85.0


def load_metrics(csv_path: Path | None = None) -> pd.DataFrame:
    path = csv_path or DATA_FILE
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df


def health_for_row(latency_ms: float, error_rate_pct: float, saturation_cpu_pct: float) -> str:
    """Aggregate health from errors, latency, and saturation (CPU)."""
    if (
        latency_ms >= LATENCY_CRITICAL_MS
        or error_rate_pct >= ERROR_CRITICAL_PCT
        or saturation_cpu_pct >= SAT_CRITICAL_PCT
    ):
        return "Critical"
    if (
        latency_ms >= LATENCY_WARNING_MS
        or error_rate_pct >= ERROR_WARNING_PCT
        or saturation_cpu_pct >= SAT_WARNING_PCT
    ):
        return "Warning"
    return "Healthy"


def health_color(status: str) -> str:
    return {"Healthy": "#2ecc71", "Warning": "#f39c12", "Critical": "#e74c3c"}.get(
        status, "#95a5a6"
    )


def main() -> None:
    st.set_page_config(
        page_title="Golden Signal Dashboard",
        page_icon="📡",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("Golden Signal Dashboard")
    st.caption("Latency · Traffic · Errors · Saturation — sample observability view")

    try:
        df = load_metrics()
    except FileNotFoundError:
        st.error(f"Data file not found: `{DATA_FILE}`. Run `python utils/generate_sample_data.py`.")
        return

    services = sorted(df["service"].dropna().unique().tolist())
    sidebar = st.sidebar
    sidebar.header("Filters")
    selected = sidebar.multiselect("Services", options=services, default=services)

    if not selected:
        st.warning("Select at least one service.")
        return

    by_service = df[df["service"].isin(selected)].sort_values("timestamp").reset_index(drop=True)
    max_idx = max(len(by_service) - 1, 0)
    time_range = sidebar.slider(
        "Time window (row index, after service filter)",
        min_value=0,
        max_value=max_idx,
        value=(0, max_idx),
    )
    lo, hi = time_range
    filtered = by_service.iloc[lo : hi + 1]

    if filtered.empty:
        st.warning("No rows in the selected window.")
        return

    last = filtered.sort_values("timestamp").groupby("service", as_index=False).tail(1)

    def row_health(row: pd.Series) -> str:
        return health_for_row(
            float(row["latency_p95_ms"]),
            float(row["error_rate_pct"]),
            float(row["saturation_cpu_pct"]),
        )

    last = last.copy()
    last["health"] = last.apply(row_health, axis=1)

    c1, c2, c3, c4 = st.columns(4)
    avg_lat = filtered["latency_p95_ms"].mean()
    avg_traffic = filtered["traffic_rpm"].mean()
    avg_err = filtered["error_rate_pct"].mean()
    avg_sat = filtered["saturation_cpu_pct"].mean()

    c1.metric("Avg latency (p95)", f"{avg_lat:.1f} ms")
    c2.metric("Avg traffic", f"{avg_traffic:.0f} req/min")
    c3.metric("Avg error rate", f"{avg_err:.2f} %")
    c4.metric("Avg saturation (CPU)", f"{avg_sat:.1f} %")

    st.subheader("Service health (latest point per service)")
    for _, row in last.iterrows():
        st.markdown(
            f"**{row['service']}** — "
            f"<span style='color:{health_color(row['health'])};font-weight:600'>{row['health']}</span>",
            unsafe_allow_html=True,
        )

    st.divider()
    st.subheader("Trends")

    ts = filtered.sort_values("timestamp")
    fig_lat = px.line(
        ts,
        x="timestamp",
        y="latency_p95_ms",
        color="service",
        title="Latency (p95, ms)",
        markers=True,
    )
    fig_lat.add_hline(y=LATENCY_WARNING_MS, line_dash="dash", line_color="orange")
    fig_lat.add_hline(y=LATENCY_CRITICAL_MS, line_dash="dash", line_color="red")

    fig_traffic = px.line(
        ts,
        x="timestamp",
        y="traffic_rpm",
        color="service",
        title="Traffic (requests per minute)",
        markers=True,
    )

    fig_err = px.line(
        ts,
        x="timestamp",
        y="error_rate_pct",
        color="service",
        title="Errors (%)",
        markers=True,
    )
    fig_err.add_hline(y=ERROR_WARNING_PCT, line_dash="dash", line_color="orange")
    fig_err.add_hline(y=ERROR_CRITICAL_PCT, line_dash="dash", line_color="red")

    fig_sat = px.line(
        ts,
        x="timestamp",
        y="saturation_cpu_pct",
        color="service",
        title="Saturation (CPU %)",
        markers=True,
    )
    fig_sat.add_hline(y=SAT_WARNING_PCT, line_dash="dash", line_color="orange")
    fig_sat.add_hline(y=SAT_CRITICAL_PCT, line_dash="dash", line_color="red")

    st.plotly_chart(fig_lat, use_container_width=True)
    st.plotly_chart(fig_traffic, use_container_width=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(fig_err, use_container_width=True)
    with col_b:
        st.plotly_chart(fig_sat, use_container_width=True)

    with st.expander("Threshold reference"):
        st.markdown(
            f"""
| Signal | Warning | Critical |
|--------|---------|----------|
| Latency (p95) | ≥ {LATENCY_WARNING_MS} ms | ≥ {LATENCY_CRITICAL_MS} ms |
| Errors | ≥ {ERROR_WARNING_PCT}% | ≥ {ERROR_CRITICAL_PCT}% |
| Saturation (CPU) | ≥ {SAT_WARNING_PCT}% | ≥ {SAT_CRITICAL_PCT}% |
| Traffic | (informational) | — |
"""
        )


if __name__ == "__main__":
    main()
