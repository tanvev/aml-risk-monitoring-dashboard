import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from peer_visuals import peer_boxplot
from alert_aging import add_aging
from alert_lifecycle import load_lifecycle
from network_risk import compute_network_risk
from behavior_analysis import behavioral_shift

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR = os.path.join(BASE_DIR, "outputs")

alerts = pd.read_csv(os.path.join(OUT_DIR, "top50_alerts.csv"))
customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))
transactions = pd.read_csv(os.path.join(DATA_DIR, "transactions.csv"))

# ---------------- ENRICH DATA ----------------
alerts = alerts.merge(
    customers[["customer_id", "branch"]],
    on="customer_id",
    how="left"
)

# Add synthetic alert creation date (for trends)
if "alert_created_date" not in alerts.columns:
    alerts["alert_created_date"] = pd.to_datetime(
        np.random.choice(
            pd.date_range("2024-01-01", "2024-12-31"),
            size=len(alerts)
        )
    )

alerts = add_aging(alerts, load_lifecycle())

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")
st.title("🏦 AML Risk Monitoring & Investigation Dashboard")

# ================= KPI ROW =================
k1, k2, k3, k4 = st.columns(4)
k1.metric("🚨 Total Alerts", len(alerts))
k2.metric("🔥 High Risk (>75)", (alerts["overall_risk"] > 75).sum())
k3.metric("⏱ SLA Breaches", alerts["sla_breach"].sum())
k4.metric("📊 Avg Risk", round(alerts["overall_risk"].mean(), 1))

st.divider()

# ================= TOP 50 ALERTS =================
st.subheader("🚨 Top-50 AML Alerts")

st.dataframe(
    alerts[[
        "customer_id",
        "overall_risk",
        "rule_score",
        "ml_score",
        "kyc_risk_score",
        "alert_age_days",
        "sla_breach"
    ]].sort_values("overall_risk", ascending=False),
    height=280,
    use_container_width=True
)

selected = st.selectbox(
    "🔍 Select Alert for Detailed Analysis",
    alerts.sort_values("overall_risk", ascending=False)["customer_id"]
)

alert = alerts[alerts["customer_id"] == selected].iloc[0]

st.divider()

# ================= TABS =================
tabs = st.tabs([
    "🔍 Risk Overview",
    "👥 Peer Comparison",
    "📈 Behavior",
    "🔥 Branch Heatmap",
    "💸 Money Flow",
    "📊 Alert Trends",
    "📄 STR Decision"
])

# =====================================================
# 🔍 TAB 1: RISK OVERVIEW
# =====================================================
with tabs[0]:
    network_score = compute_network_risk(transactions, selected)

    c1, c2 = st.columns(2)

    with c1:
        fig, ax = plt.subplots()
        ax.bar(
            ["Rule", "ML", "Network", "KYC"],
            [
                alert["rule_score"],
                alert["ml_score"],
                network_score,
                alert["kyc_risk_score"]
            ]
        )
        ax.set_title("Risk Component Breakdown")
        st.pyplot(fig)

    with c2:
        fig, ax = plt.subplots()
        ax.scatter(alerts["ml_score"], alerts["rule_score"], alpha=0.6)
        ax.scatter(alert["ml_score"], alert["rule_score"], color="red", s=120)
        ax.set_xlabel("ML Score")
        ax.set_ylabel("Rule Score")
        ax.set_title("ML vs Rule Landscape")
        st.pyplot(fig)

# =====================================================
# 👥 TAB 2: PEER COMPARISON
# =====================================================
with tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        st.pyplot(peer_boxplot(customers, alerts, selected, "txn_count"))
    with c2:
        st.pyplot(peer_boxplot(customers, alerts, selected, "total_out"))

# =====================================================
# 📈 TAB 3: BEHAVIOR
# =====================================================
with tabs[2]:
    past, recent = behavioral_shift(transactions, selected)

    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots()
        ax.bar(["Past", "Recent"], [past["total_amount"], recent["total_amount"]])
        ax.set_title("Total Amount Shift")
        st.pyplot(fig)

    with c2:
        fig, ax = plt.subplots()
        ax.bar(["Past", "Recent"], [past["txn_count"], recent["txn_count"]])
        ax.set_title("Transaction Count Shift")
        st.pyplot(fig)

# =====================================================
# 🔥 TAB 4: BRANCH HEATMAP
# =====================================================
with tabs[3]:
    branch_risk = alerts.groupby("branch")["overall_risk"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(7, 4))
    heat = ax.imshow(branch_risk[["overall_risk"]], cmap="Reds", aspect="auto")
    ax.set_yticks(range(len(branch_risk)))
    ax.set_yticklabels(branch_risk["branch"])
    ax.set_xticks([0])
    ax.set_xticklabels(["Avg Risk"])
    ax.set_title("Branch vs Risk Heatmap")
    st.pyplot(fig)

# =====================================================
# 💸 TAB 5: MONEY FLOW SANKEY
# =====================================================
with tabs[4]:
    flow_df = (
        transactions.groupby(["from_customer", "to_customer"])["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
        .head(10)
    )

    labels = list(pd.unique(flow_df[["from_customer", "to_customer"]].values.ravel()))
    label_index = {l: i for i, l in enumerate(labels)}

    fig = go.Figure(
        data=[go.Sankey(
            node=dict(label=labels, pad=15, thickness=20),
            link=dict(
                source=[label_index[x] for x in flow_df["from_customer"]],
                target=[label_index[x] for x in flow_df["to_customer"]],
                value=flow_df["amount"]
            )
        )]
    )
    fig.update_layout(title_text="Top Money Flows", font_size=10)
    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 📊 TAB 6: ALERT TREND
# =====================================================
with tabs[5]:
    trend = (
        alerts.groupby(alerts["alert_created_date"].dt.to_period("M"))
        .size()
        .reset_index(name="count")
    )
    trend["alert_created_date"] = trend["alert_created_date"].astype(str)

    fig, ax = plt.subplots()
    ax.plot(trend["alert_created_date"], trend["count"], marker="o")
    ax.set_title("Alert Trend Over Time")
    ax.set_xlabel("Month")
    ax.set_ylabel("No. of Alerts")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# =====================================================
# 📄 TAB 7: STR DECISION
# =====================================================
with tabs[6]:
    signals = {
        "Rule": alert["rule_score"] > 40,
        "ML": alert["ml_score"] > 70,
        "Network": network_score > 50,
        "KYC": alert["kyc_risk_score"] > 60,
        "SLA": alert["sla_breach"]
    }

    fig, ax = plt.subplots()
    ax.imshow([[int(v) for v in signals.values()]], cmap="Reds")
    ax.set_xticks(range(len(signals)))
    ax.set_xticklabels(signals.keys())
    ax.set_yticks([])
    ax.set_title("STR Signal Heatmap")
    st.pyplot(fig)

    readiness = sum(signals.values()) / len(signals) * 100
    st.metric("📄 STR Readiness (%)", round(readiness, 1))
