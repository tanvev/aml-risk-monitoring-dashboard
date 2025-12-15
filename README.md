# AML Risk Monitoring & Investigation Dashboard
Link- https://aml-risk-monitoring-dashboard.streamlit.app/
An end-to-end **Anti-Money Laundering (AML) risk analytics and investigation system** that simulates how banks detect, analyze, and investigate suspicious financial activity.

This project integrates **rule-based checks, machine learning signals, network analysis, behavioral analytics, and visual dashboards** to replicate a real-world AML monitoring and investigation workflow.

---
## Project Highlights

- End-to-end AML monitoring and investigation system
- Visual-first analyst dashboard (risk, behavior, network, trends)
- Money mule detection using transaction network analysis
- Alert aging and SLA breach monitoring
- Peer-group benchmarking with box plots
- STR decision support using explainable signals
---

## Overview

The objective of this project is to design a **visual-first AML analyst dashboard** that prioritizes:

* Explainability of alerts
* Reduction of false positives
* Analyst-driven investigation
* Regulatory-aligned decision support

The system mirrors the structure and logic of AML platforms used in banks and financial institutions.

---

## Key Features

### Risk Detection and Scoring

* Rule-based transaction monitoring
* Machine learning anomaly detection (Isolation Forest)
* Network-based money mule risk scoring
* KYC risk integration
* Composite overall risk score for alert prioritization

---

### Visual Analytics Dashboard

* Top 50 AML alerts ranked by risk
* Risk component breakdown (Rule, ML, Network, KYC)
* ML vs Rule score scatter plot
* Branch-wise risk heatmap
* Alert aging and SLA breach indicators
* Alert trend analysis over time

---

### Peer Group Analysis

* Peer group definition based on:

  * Same branch
  * Similar income band (±30%)
* Box plots showing deviation in:

  * Transaction count
  * Total outgoing transaction amount
* Clear visual identification of abnormal customer behavior

---

### Behavioral Change Detection

* Comparison of recent activity (last 30 days) versus historical baseline
* Visual analysis of:

  * Transaction count changes
  * Transaction amount changes
* Helps identify sudden behavioral shifts

---

### Money Flow Analysis

* Sankey diagram representing aggregated money flows
* Visualizes fund movement between accounts
* Supports identification of aggregation and pass-through patterns

---

### STR Decision Support

* STR signal heatmap covering:

  * Rule breaches
  * ML anomalies
  * Network risk
  * KYC risk
  * SLA breaches
* STR readiness score (percentage)
* Designed to assist analysts in regulatory reporting decisions

---

### Alert Lifecycle and Compliance

* Alert aging calculation
* SLA breach detection (7-day threshold)
* Audit-friendly lifecycle tracking

---

## Why This Project Matters

This system is designed to reflect **real AML practices in banks**, with emphasis on:

* Analyst-centric workflows
* Explainable risk indicators
* Visual decision support
* Compliance and audit readiness

It is suitable for:

* AML and compliance internships
* Risk and data analyst roles
* FinTech and BFSI interviews
* Academic capstone or final-year projects

---

## Project Structure

```
aml-project/
│
├── data/
│   ├── customers.csv
│   └── transactions.csv
│
├── outputs/
│   ├── top50_alerts.csv
│   ├── alert_lifecycle.csv
│   └── str_reports/
│
├── src/
│   ├── aml_pipeline.py
│   ├── network_risk.py
│   ├── behavior_analysis.py
│   ├── peer_visuals.py
│   ├── alert_aging.py
│   ├── alert_lifecycle.py
│   └── streamlit_app.py
│
├── requirements.txt
└── README.md
```

---

## Technology Stack

* Python
* Pandas, NumPy – data processing
* Scikit-learn – machine learning (Isolation Forest)
* NetworkX – transaction network analysis
* Matplotlib, Plotly – data visualization
* Streamlit – interactive dashboard

---

## Setup Instructions

### Step 1: Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the AML pipeline

```bash
python src/aml_pipeline.py
```

### Step 4: Launch the dashboard

```bash
streamlit run src/streamlit_app.py
```

---

## Example Use Cases

* Identify high-risk customers across branches
* Detect potential money mule behavior
* Prioritize alerts based on risk and SLA
* Compare customer activity against peer groups
* Support Suspicious Transaction Report (STR) decisions

---

## Future Enhancements

* Graph database integration (Neo4j) for large-scale network analysis
* Supervisor approval and escalation workflows
* Model drift monitoring
* Advanced false-positive reduction techniques
* Dark-mode analyst dashboard

---


## Disclaimer

This project uses **synthetic data only** and is intended strictly for **educational purposes**.
It does not represent real customers, accounts, or financial activity.

