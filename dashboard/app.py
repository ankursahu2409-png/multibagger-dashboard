import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from screener.scoring import score_stocks
from sentiment.analyzer import analyze_sentiment
from news.fetcher import fetch_headlines  # <-- New module

st.set_page_config(page_title="Multibagger Stock Dashboard", layout="wide")
st.title("📊 Multibagger Stock Analyzer")

# Sidebar filters
st.sidebar.header("🔍 Filter Stocks")
min_roe = st.sidebar.slider("Minimum ROE (%)", 0, 30, 10)
max_de_ratio = st.sidebar.slider("Max Debt/Equity", 0.0, 1.0, 0.5)
min_sentiment = st.sidebar.slider("Minimum Sentiment Score", -1, 1, 0)

# CSV upload
st.sidebar.header("📁 Upload Your CSV")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Load data
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
else:
    st.info("ℹ️ Using sample data until a CSV is uploaded.")
    df = pd.DataFrame({
        'Stock': ['Tech Inc', 'Revenue Growth Co', 'Stable Earnings Ltd', 'New Product Corp'],
        'Revenue_Growth_YoY': [0.15, 0.25, 0.05, 0.30],
        'Profit_Growth_YoY': [0.10, 0.12, 0.08, 0.05],
        'Debt_Equity': [0.5, 0.3, 0.4, 0.6],
        'ROCE': [14, 18, 10, 12],
        'ROE': [12, 16, 9, 11],
        'Promoter_Holding': [0.60, 0.70, 0.55, 0.40],
        'PEG_Ratio': [1.5, 1.2, 1.8, 2.0]
    })

# Fetch headlines + sentiment with spinner
api_key = "d790a960246149cab2d304c3adb7421c"

with st.spinner("🔄 Fetching live headlines and analyzing sentiment..."):
    df['Headlines'] = df['Stock'].apply(lambda name: fetch_headlines(name, api_key, max_articles=3))
   def average_sentiment(headlines):
    scores = [analyze_sentiment(h) for h in headlines if h]
    return round(sum(scores) / len(scores), 3) if scores else 0

df['Sentiment_Score'] = df['Headlines'].apply(average_sentiment)
df['Headline'] = df['Headlines'].apply(lambda hlist: hlist[0] if hlist else "No headline found")

# Score stocks
scored_df = score_stocks(df)
scored_df['Multibagger_Score'] += df['Sentiment_Score'] * 0.1

# Apply filters
filtered_df = scored_df[
    (scored_df['ROE'] >= min_roe) &
    (scored_df['Debt_Equity'] <= max_de_ratio) &
    (scored_df['Sentiment_Score'] >= min_sentiment)
]

# Tabs for layout
tab1, tab2, tab3, tab4 = st.tabs(["📊 Scored Results", "📈 Financials", "🧠 Sentiment", "📰 News"])

with tab1:
    st.subheader("Multibagger Scores")
    st.dataframe(filtered_df[['Stock', 'Multibagger_Score', 'Sentiment_Score']].sort_values(by='Multibagger_Score', ascending=False))
    st.bar_chart(filtered_df.set_index('Stock')['Multibagger_Score'])

    # Export button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered Results", data=csv, file_name="filtered_stocks.csv", mime="text/csv")

with tab2:
    st.subheader("Raw Financial Metrics")
    st.dataframe(filtered_df[['Stock', 'ROE', 'ROCE', 'Debt_Equity', 'PEG_Ratio', 'Promoter_Holding']])

with tab3:
    st.subheader("Sentiment Breakdown")
    st.dataframe(filtered_df[['Stock', 'Headline', 'Sentiment_Score']])
    
with tab4:
    st.subheader("Latest Headlines per Stock")
    for i, row in filtered_df.iterrows():
        st.markdown(f"**{row['Stock']}**")
        headlines = row.get('Headlines', [])
        if isinstance(headlines, list):
            for h in headlines:
                st.markdown(f"- {h}")
        else:
            st.markdown("- No headlines found")
        st.markdown("---")

# Footer
st.markdown("---")
st.caption("Built by Ankur • Powered by Streamlit + FinBERT + NewsAPI")