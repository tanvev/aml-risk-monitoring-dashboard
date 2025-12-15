import pandas as pd
from datetime import datetime

SLA_DAYS = 7

def add_aging(alerts, lifecycle):
    alerts = alerts.copy()

    if lifecycle.empty or "last_updated" not in lifecycle.columns:
        alerts["alert_age_days"] = 0
        alerts["sla_breach"] = False
        return alerts

    lifecycle = lifecycle.copy()
    lifecycle["last_updated"] = pd.to_datetime(lifecycle["last_updated"], errors="coerce")

    alerts = alerts.merge(
        lifecycle[["customer_id", "last_updated"]],
        on="customer_id",
        how="left"
    )

    alerts["last_updated"] = alerts["last_updated"].fillna(datetime.now())
    alerts["alert_age_days"] = (
        datetime.now() - alerts["last_updated"]
    ).dt.days

    alerts["sla_breach"] = alerts["alert_age_days"] > SLA_DAYS

    return alerts
