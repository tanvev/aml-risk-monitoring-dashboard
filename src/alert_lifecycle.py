import pandas as pd
import os
from datetime import datetime

LIFECYCLE_FILE = "outputs/alert_lifecycle.csv"

def load_lifecycle():
    if not os.path.exists(LIFECYCLE_FILE):
        return pd.DataFrame(columns=[
            "customer_id", "status", "assigned_to",
            "last_updated", "analyst_notes"
        ])
    return pd.read_csv(LIFECYCLE_FILE)

def update_lifecycle(customer_id, status, analyst, notes=""):
    df = load_lifecycle()

    df = df[df["customer_id"] != customer_id]

    df = pd.concat([df, pd.DataFrame([{
        "customer_id": customer_id,
        "status": status,
        "assigned_to": analyst,
        "last_updated": datetime.now(),
        "analyst_notes": notes
    }])])

    df.to_csv(LIFECYCLE_FILE, index=False)
