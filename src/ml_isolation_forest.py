from sklearn.ensemble import IsolationForest

def train_iforest(features):
    X = features[["total_in", "total_out", "txn_count", "in_out_ratio"]]

    if X.empty:
        raise ValueError("❌ Feature matrix is empty. Check feature engineering step.")

    model = IsolationForest(
        n_estimators=300,
        contamination=0.02,
        random_state=42
    )

    model.fit(X)

    scores = model.decision_function(X)
    features["ml_score"] = (-scores - scores.min()) / (scores.max() - scores.min()) * 100

    return features
