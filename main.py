import streamlit as st
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import re
from collections import Counter
from itertools import islice

# Function to fetch and parse a webpage
def fetch_page(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

# Function to count words in a specific section of a webpage
def count_words(soup, section=None):
    if section:
        elements = soup.select(section)
    else:
        elements = soup.find_all(text=True)
    
    text = ' '.join([element.strip() for element in elements if element.strip()])
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words)

# Function to categorize word counts
def categorize_word_counts(soup):
    categories = {
        'Linked Words': count_words(soup, 'a'),
        'Unlinked Words': count_words(soup, ':not(a)'),
        'Footer Linked Words': count_words(soup, 'footer a'),
        'Footer Unlinked Words': count_words(soup, 'footer :not(a)'),
        'Navigation Linked Words': count_words(soup, 'nav a'),
        'Navigation Unlinked Words': count_words(soup, 'nav :not(a)'),
        'Body Words': count_words(soup, 'body'),
        'Body Unlinked Words': count_words(soup, 'body :not(a)'),
    }
    return categories

# Function to count n-word phrases
def count_phrases(words, n):
    phrases = [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]
    return Counter(phrases)

# Function to display the analysis
def display_analysis(url, categories, phrases):
    st.subheader(f'Analysis for {url}')
    st.write('### Word Counts by Category:')
    for category, counts in categories.items():
        st.write(f'**{category}**: {sum(counts.values())} words')
        st.write(counts.most_common(10))
    
    st.write('### Phrase Counts:')
    for n, phrase_count in phrases.items():
        st.write(f'**{n}-word Phrases:**')
        st.write(phrase_count.most_common(10))

# Main function to run the app
def main():
    st.title("Website Word and Phrase Analysis Tool")
    
    urls = st.text_area("Enter your URL and competitors' URLs (one per line):").splitlines()
    
    if st.button("Analyze"):
        for url in urls:
            if url:
                soup = fetch_page(url)
                categories = categorize_word_counts(soup)
                words = re.findall(r'\b\w+\b', soup.get_text().lower())
                phrases = {1: count_phrases(words, 1), 2: count_phrases(words, 2), 3: count_phrases(words, 3)}
                display_analysis(url, categories, phrases)

if __name__ == "__main__":
    main()
