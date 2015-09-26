
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np
from nltk.corpus import stopwords
from nltk import word_tokenize
from sklearn.metrics.pairwise import linear_kernel
from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
import unidecode
import string
from nltk.stem.snowball import SnowballStemmer
snowball = SnowballStemmer('english')
import pandas as pd

master = pd.read_csv('data/master.csv', low_memory=False)

unique_url = master['URL'].unique()

def tokenize(doc):
    return [snowball.stem(word) for word in word_tokenize(doc.lower())]

tfidfvect = TfidfVectorizer(stop_words='english', tokenizer=tokenize)


for url in unique_url:
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find_all('p', class_= "story-body-text story-content")
    content = '\n'.join([i.text for i in soup.select('p.story-body-text')])
    body_text = unidecode.unidecode(content).replace("\n"," ").replace("\'s","").replace("\'t","")
    master['Article'] = unidecode.unidecode(content).replace("\n"," ").replace("\'s","").replace("\'t","")

    cond = master['URL'] == url
    master_url = master[cond]
    documents = master_url['Comment']
    body_text = np.array(body_text)

    documents = np.append(documents.values, body_text) #body_text is the very last element in the array

    tfidf_vectorized = tfidfvect.fit_transform(documents).toarray()

    similar_to_article = []
    for comment in tfidf_vectorized[:-1]:
        similar_to_article.append(cosine_similarity(comment, tfidf_vectorized[-1])[0, 0])
  
    master.loc[cond, 'tfidf_similarity'] = np.array(similar_to_article)


master.iloc[:,-1].to_csv('master_sum.csv')




