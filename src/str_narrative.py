def generate_str_narrative(alert, network_score, behavior, peer_pct):
    return f"""
The subject account {alert['customer_id']} was identified during transaction
monitoring due to elevated risk indicators.

The overall risk score of {alert['overall_risk']:.2f} was driven by a combination
of anomalous transactional behavior, rule-based triggers, and network patterns.

Network analysis indicates a network risk score of {network_score}, suggesting
possible pass-through or money mule characteristics.

Behavioral analysis shows a recent increase in transaction activity compared to
historical patterns.

Peer group comparison places the customer above the {peer_pct} percentile for
transaction activity within a similar profile group.

Based on the above observations, the activity is considered suspicious and is
recommended for regulatory reporting.
""".strip()
