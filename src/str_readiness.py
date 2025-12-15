def str_readiness(alert, network_score, behavior_shift):
    checklist = {
        "High Overall Risk": alert["overall_risk"] > 75,
        "ML Anomaly": alert["ml_score"] > 70,
        "Rule Breach": alert["rule_score"] > 40,
        "Network Risk": network_score > 50,
        "Behavioral Spike": behavior_shift
    }

    score = sum(checklist.values()) / len(checklist) * 100

    decision = (
        "STR Recommended"
        if score >= 60 else
        "Monitor / Seek More Info"
    )

    return checklist, round(score, 1), decision
