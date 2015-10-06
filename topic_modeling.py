import pandas as pd
import numpy as np 
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from itertools import *
import matplotlib.pyplot as plt
import re
import string
import unidecode
from sklearn.decomposition import NMF
import datetime
from utils import tokenize

class Model(object):

    def __init__(self, n_topics, df):
        self.n_topics = n_topics
        self.df = df
        self.model = None
        self.matrix = None

	def remove_abb(self, text):
	    terms = [('mrs. ', ''), ('mr. ', ''), ('ms. ',''), ('dr. ',''), ('sen. ','')]
	    for k, v in mapping:
    		text = text.replace(k, v)
	    return text

    def build_model(self):
        vectorizer = TfidfVectorizer(tokenizer=tokenize, stop_words = 'english')
        vector = vectorizer.fit_transform(self.df['Comment'].values).toarray()
        self.model = NMF(n_components=self.n_topics).fit(vector)
        self.features = vectorizer.get_feature_names()
        self.matrix = self.model.transform(self.vectorizer)
	    
	    #return self.matrix, self.model.components_, self.features

	def output_data(self):
	    self.examples = []
	    self.comment = []
	    self.topic_words = []

	    index = self.matrix.argmax(axis=0)
	    self.df = self.df.reset_index()
	    self.examples.append(self.df.ix[index]['Comment'].values)
	    np.sort(self.matrix, axis =1)

	    for i in range(self.n_topics):
	        self.comment.append(len(self.matrix[:,i][self.matrix[:,i] > 0.05]))
	    
	    self.num_per_topics = len(comments)

	    for topic in self.model.components_:
	        topic_words.append(" ".join([self.features[i]
	                for i in topic.argsort()[:-5 -1:-1]]))

	    return self.examples, self.topic_words, self.num_per_topics 

	def to_df(self):
		dat = list(izip(self.topic_words, self.examples))
		data = pd.DataFrame(list(izip(dat, self.num_per_topics)))
		data[['keys', 'examples']] = data[0].apply(pd.Series)
		data.rename(columns={1:'num'}, inplace=True)
		data.drop(0, axis = 1, inplace=True)
		return data

	def combine_df(df_pos, df_neg):
		comments = pd.concat([df_pos, df_neg], axis = 1)
		comments.columns = ['pos_key', 'pos_example', 'pos_num', 'neg_key', 'neg_example', 'neg_num']
		comments['pos_keys'] = comments['pos_keys'].apply(lambda x : remove_abb(x))
		comments['neg_keys'] = comments['neg_keys'].apply(lambda x : remove_abb(x))
		comments['pos_percent'] = comments['pos_num']/comments['pos_num'].sum()
		comments['neg_percent'] = comments['neg_num']/comments['neg_num'].sum()


if __name__ == '__main__':
    candidates = ['hillary', 'sanders', 'biden', 'trump', 'bush', 'carson'] 
    
    for c in candidates:
        data = pd.read_csv('data/' + c + '_scores.csv')
        data[pd.isnull(data['Comment'])] = ""
        pos = data[data['Sentiment'] > 0.2]
        neg = data[data['Sentiment'] < -0.1]
        dfs = [neg, pos]
        new_dfs= []

        model = Model(n_topics=10, df=data)
        model.build_model()
        model.output_data()
        new_dfs.append(model.to_df)
        dataframe = combine_df(new_dfs[0], new_dfs[1])
        dataframe.to_csv('data/' + c + 'topics.csv')
