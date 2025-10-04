import pandas as pd
from sentiment.analyzer import analyze_sentiment
from screener.scoring import score_stocks

# Sample stock data
df = pd.DataFrame({
    'Stock': ['Tech Inc', 'Revenue Growth Co', 'Stable Earnings Ltd', 'New Product Corp'],
    'Revenue_Growth_YoY': [0.15, 0.25, 0.05, 0.30],
    'Profit_Growth_YoY': [0.10, 0.12, 0.08, 0.05],
    'Debt_Equity': [0.5, 0.3, 0.4, 0.6],
    'ROCE': [14, 18, 10, 12],
    'ROE': [12, 16, 9, 11],
    'Promoter_Holding': [0.60, 0.70, 0.55, 0.40],
    'PEG_Ratio': [1.5, 1.2, 1.8, 2.0],
    'Headline': [
        "Tech Inc reports strong earnings",
        "Revenue Growth Co's Q2 beats estimates",
        "Stable Earnings Ltd maintains steady performance",
        "New Product Corp faces regulatory issues"
    ]
})

# Apply sentiment analysis
df['Sentiment_Score'] = df['Headline'].apply(analyze_sentiment)

# Score and adjust
scored_df = score_stocks(df)
scored_df['Multibagger_Score'] += df['Sentiment_Score'] * 0.1

# Show results
print(scored_df[['Stock', 'Multibagger_Score']])