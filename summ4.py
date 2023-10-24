import io
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from textblob import TextBlob
import streamlit as st
from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup


#nltk.download('punkt')
#nltk.download('stopwords')


def summarize(text, n):
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    # Remove stop words and punctuation
    stop_words = stopwords.words('english')
    words = [word for word in words if word.isalnum() and word not in stop_words]

    # Calculate the frequency of each word
    frequency = defaultdict(int)
    for word in words:
        frequency[word] += 1

    # Rank the sentences by their total word frequency
    rankings = defaultdict(int)
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in frequency:
                rankings[i] += frequency[word]

    # Sort the sentences by their rankings and return the top n
    top_sentences = sorted(rankings, key=rankings.get, reverse=True)[:n]
    summary = [sentences[i] for i in top_sentences]
    return ' '.join(summary)


def analyze_sentiment(text):
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

def main():
    st.title("Text Analysis and Chatbot")

    # Sidebar options
    page = st.sidebar.radio(
        "Select a page:", ("Summarize Random Text", "Summarize Document", "Sentiment Analysis", "Browse News"))

    if page == "Summarize Random Text":
        summarize_random_text_page()
    elif page == "Summarize Document":
        summarize_document_page()
    elif page == "Sentiment Analysis":
        sentiment_analysis_page()
    elif page == "Browse News":
        browse_news_page()
   


        


def summarize_random_text_page():
    st.header("Summarize Random Text")

    # Text input
    text = st.text_area("Enter some text to summarize", height=200)

    # Summarize random text
    if st.button("Summarize"):
        if text:
            summary = summarize(text, 3)
            st.success("Summary:\n" + summary)
        else:
            st.warning("Please enter some text to summarize.")


def summarize_document_page():
    st.header("Summarize Document")

    # File input
    file = st.file_uploader("Upload a file", type=["txt", "html", "pdf"])

    # Summarize document contents
    if st.button("Summarize") and file is not None:
        if file.type == "text/plain":
            # Read text file
            text = io.TextIOWrapper(file, encoding='utf-8').read()
            summary = summarize(text, 3)
            st.success("Summary:\n" + summary)
        elif file.type == "text/html":
            # Read HTML file
            html = io.TextIOWrapper(file, encoding='utf-8').read()
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()
            summary = summarize(text, 3)
            st.success("Summary:\n" + summary)
        elif file.type == "application/pdf":
            # Read PDF file
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            summary = summarize(text, 3)
            st.success("Summary:\n" + summary)
        else:
            st.warning("Invalid file format. Please upload a valid text, HTML, or PDF file.")


def sentiment_analysis_page():
    st.header("Sentiment Analysis")

    # Text input
    text = st.text_area("Enter text")
    
    # Analyze sentiment
    if st.button("Analyze"):
        sentiment = analyze_sentiment(text)
        st.success("Sentiment: " + sentiment)
        


NEWS_API_KEY = "e05736f97c6145ea8ee21de806432e24"   #https://newsapi.org/

def browse_news_page():
    st.header("Browse Google News")

    # Search query input
    query = st.text_input("Enter your search query")

    # Search news and display results
    if st.button("Search"):
        if query:
            news_url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
            response = requests.get(news_url)
            data = response.json()

            articles = data.get("articles", [])

            for article in articles:
                title = article.get("title")
                link = article.get("url")
                description = article.get("description")
                st.write(f"**Title:** [{title}]({link})")
                st.write(f"**Description:** {description}")
                st.write("---")
        else:
            st.warning("Please enter a search query.")
            


if __name__ == "__main__":
    main()
