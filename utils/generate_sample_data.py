"""
Generate realistic sample monitoring rows for the Golden Signal Dashboard.
Run from repository root: python utils/generate_sample_data.py
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

import pandas as pd

SERVICES = [
    "api-gateway",
    "auth-service",
    "payment-service",
    "inventory-service",
    "notification-worker",
]


def _gauss(rng: random.Random, mu: float = 0.0, sigma: float = 1.0) -> float:
    return rng.gauss(mu, sigma)


def build_frame(rows_per_service: int = 48, seed: int = 42) -> pd.DataFrame:
    rng = random.Random(seed)
    rows = []
    base_time = pd.Timestamp("2025-03-01T00:00:00Z")

    for svc_idx, service in enumerate(SERVICES):
        lat_base = 80 + svc_idx * 25
        err_base = 0.2 + svc_idx * 0.15
        sat_base = 45 + svc_idx * 5

        for i in range(rows_per_service):
            ts = base_time + pd.Timedelta(minutes=15 * i)
            noise = _gauss(rng)
            spike = 1.35 if i % 17 == 0 else 1.0
            latency_p95_ms = max(10.0, lat_base * spike + noise * 18)
            traffic_rpm = max(50.0, 400 + svc_idx * 120 + noise * 60 + i * 3)
            error_rate_pct = max(
                0.0,
                err_base + abs(noise) * 0.4 + (0.8 if i % 23 == 0 else 0),
            )
            saturation_cpu_pct = min(
                99.0,
                max(5.0, sat_base + noise * 8 + (12 if i % 19 == 0 else 0)),
            )

            rows.append(
                {
                    "timestamp": ts.isoformat(),
                    "service": service,
                    "latency_p95_ms": round(latency_p95_ms, 2),
                    "traffic_rpm": round(traffic_rpm, 2),
                    "error_rate_pct": round(error_rate_pct, 3),
                    "saturation_cpu_pct": round(saturation_cpu_pct, 2),
                }
            )

    return pd.DataFrame(rows).sort_values(["timestamp", "service"]).reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Write data/sample_metrics.csv")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "data" / "sample_metrics.csv",
        help="Output CSV path",
    )
    parser.add_argument("--rows-per-service", type=int, default=48)
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    df = build_frame(rows_per_service=args.rows_per_service)
    df.to_csv(args.out, index=False)
    print(f"Wrote {len(df)} rows to {args.out}")


if __name__ == "__main__":
    main()
