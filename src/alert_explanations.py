# src/alert_explanations.py

def generate_explanation(row):
    reasons = []

    if row["rule_score"] > 50:
        reasons.append("High rule-based risk: large or structured transactions detected")

    if row["ml_score"] > 70:
        reasons.append("Anomalous transaction behaviour compared to peer group")

    if row.get("network_score", 0) > 50:
        reasons.append("Suspicious network pattern: possible mule or circular transactions")

    if row["kyc_risk_score"] > 60:
        reasons.append("High inherent customer risk based on KYC profile")

    if not reasons:
        reasons.append("Moderate composite risk based on combined indicators")

    return " | ".join(reasons)
