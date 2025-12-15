import pandas as pd
import os
from datetime import datetime

AUDIT_FILE = "outputs/audit_trail.csv"

def log_action(customer_id, action, analyst):
    if not os.path.exists(AUDIT_FILE):
        df = pd.DataFrame(columns=[
            "timestamp", "customer_id", "action", "analyst"
        ])
    else:
        df = pd.read_csv(AUDIT_FILE)

    df.loc[len(df)] = [
        datetime.now(),
        customer_id,
        action,
        analyst
    ]

    df.to_csv(AUDIT_FILE, index=False)


def get_audit(customer_id):
    if not os.path.exists(AUDIT_FILE):
        return None

    df = pd.read_csv(AUDIT_FILE)
    return df[df["customer_id"] == customer_id]
