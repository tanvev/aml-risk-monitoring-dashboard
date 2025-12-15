# src/aml_rules.py
import pandas as pd

def apply_rules(transactions):
    df = transactions.copy()
    df['rule_score'] = 0

    df.loc[df['amount'] > 200000, 'rule_score'] += 40
    df.loc[(df['is_cash'] == 1) & (df['amount'] > 50000), 'rule_score'] += 20
    df.loc[(df['amount'] >= 45000) & (df['amount'] <= 50000), 'rule_score'] += 15

    return df
