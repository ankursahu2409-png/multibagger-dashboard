import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def score_stocks(df):
    scaler = MinMaxScaler()
    pos_cols = ['Revenue_Growth_YoY', 'Profit_Growth_YoY', 'ROCE', 'ROE', 'Promoter_Holding']
    df[pos_cols] = scaler.fit_transform(df[pos_cols])
    df['Debt_Equity_Score'] = 1 - scaler.fit_transform(df[['Debt_Equity']])
    df['PEG_Score'] = 1 - scaler.fit_transform(df[['PEG_Ratio']])
    df['Multibagger_Score'] = (
        df['Revenue_Growth_YoY'] * 0.2 +
        df['Profit_Growth_YoY'] * 0.2 +
        df['ROCE'] * 0.15 +
        df['ROE'] * 0.15 +
        df['Promoter_Holding'] * 0.1 +
        df['Debt_Equity_Score'] * 0.1 +
        df['PEG_Score'] * 0.1
    )
    return df.sort_values(by='Multibagger_Score', ascending=False)