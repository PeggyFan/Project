
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
import unidecode
import string
import pandas as pd
from utils import tokenize

class similarity(object):
    def __init__(self, df):
        self.df = df
        self.tfidfvect = TfidfVectorizer(stop_words='english', tokenizer=tokenize)
        self.tfidf_vectorized = None
        self.cond = None

    def create_document_matrix(self):
        unique_url = self.df['URL'].unique()

    #Retrieve article content
        for url in unique_url:
            html = requests.get(url).content
            soup = BeautifulSoup(html, 'html.parser')
            body = soup.find_all('p', class_= "story-body-text story-content")
            content = '\n'.join([i.text for i in soup.select('p.story-body-text')])
            body_text = unidecode.unidecode(content).replace("\n"," ").replace("\'s","").replace("\'t","")
            self.df['Article'] = unidecode.unidecode(content).replace("\n"," ").replace("\'s","").replace("\'t","")

            #Find all comments related to a given article
            self.cond = self.df['URL'] == url
            df_url = self.df[self.cond]
            documents = df_url['Comment']
            body_text = np.array(body_text)
            #Create a document matrix with the article and its comments
            documents = np.append(documents.values, body_text) #body_text is the very last element in the array
            self.tfidf_vectorized = self.tfidfvect.fit_transform(documents).toarray()

    #
    def get_similarity(self):
        similar_to_article = []
        for comment in self.tfidf_vectorized[:-1]:
            similar_to_article.append(cosine_similarity(comment, self.tfidf_vectorized[-1])[0, 0])
        self.df.loc[self.cond, 'tfidf_similarity'] = np.array(similar_to_article)
        return self.df


if __name__ == '__main__':

    candidates = ['hillary', 'sanders', 'biden', 'trump', 'bush', 'carson'] 
    for c in candidates:
        raw = pd.read_csv('data/' + c + '_scores.csv', low_memory=False)
        data = similarity(raw)
        data.create_document_matrix()
        output = data.get_similarity()
        output.iloc[:,-1].to_csv(c + '_sim_scores.csv')
