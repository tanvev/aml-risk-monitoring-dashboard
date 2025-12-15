import os
import pandas as pd
from aml_rules import apply_rules
from feature_engineering import build_features
from ml_isolation_forest import train_iforest
from alert_explanations import generate_explanation
from false_positive_filter import reduce_false_positives


# -------- Path handling (IMPORTANT FIX) --------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(OUT_DIR, exist_ok=True)

# -------- Load data --------
customers_path = os.path.join(DATA_DIR, "customers.csv")
transactions_path = os.path.join(DATA_DIR, "transactions.csv")

if not os.path.exists(transactions_path):
    raise FileNotFoundError("❌ transactions.csv not found. Run data_generator.py first.")

customers = pd.read_csv(customers_path)
transactions = pd.read_csv(transactions_path)

print("✅ Data loaded")

# -------- AML rules --------
transactions = apply_rules(transactions)

rule_scores = (
    transactions.groupby("from_customer")["rule_score"]
    .sum()
    .reset_index()
    .rename(columns={"from_customer": "customer_id"})
)


# -------- Features + ML --------
features = build_features(transactions, customers)
print("Feature rows:", len(features))
print(features.head())
features = train_iforest(features)

final = features.merge(rule_scores, on="customer_id", how="left").fillna(0)
# Ensure missing columns exist
if "network_score" not in final.columns:
    final["network_score"] = 0

# Generate alert explanations
final["alert_reason"] = final.apply(generate_explanation, axis=1)

final["overall_risk"] = (
    0.3 * final["kyc_risk_score"]
    + 0.4 * final["ml_score"]
    + 0.3 * final["rule_score"]
)

final["is_actionable"] = final.apply(reduce_false_positives, axis=1)

final = final[final["is_actionable"] == True]

top50 = final.sort_values("overall_risk", ascending=False).head(50)

out_path = os.path.join(OUT_DIR, "top50_alerts.csv")
top50.to_csv(out_path, index=False)

print(f"✅ top50_alerts.csv generated at {out_path}")
