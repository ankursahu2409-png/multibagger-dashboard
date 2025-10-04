from transformers import pipeline
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
sentiment_model = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")

def clean_text(text):
    text = re.sub(r'http\S+|[^a-zA-Z\s]', '', text)
    text = text.lower()
    return ' '.join([word for word in text.split() if word not in stopwords.words('english')])

def analyze_sentiment(text):
    cleaned = clean_text(text)
    result = sentiment_model(cleaned)[0]
    tone = result['label']
    if tone == 'Positive': return 1
    elif tone == 'Negative': return -1
    else: return 0