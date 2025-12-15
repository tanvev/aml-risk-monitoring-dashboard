def reduce_false_positives(alert):
    signals = [
        alert["rule_score"] > 40,
        alert["ml_score"] > 70,
        alert["network_score"] > 50,
        alert["kyc_risk_score"] > 60
    ]

    return sum(signals) >= 2
