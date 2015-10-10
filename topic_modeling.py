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
    '''
    INPUT Number of topics, DataFrame
	'''
        self.n_topics = n_topics
        self.df = df
        self.model = None
        self.matrix = None
        self.features = None

	# Build the vectorizer and create the TF-IDF matrix
    def build_model(self):
        vectorizer = TfidfVectorizer(tokenizer=tokenize, stop_words = 'english')
        vector = vectorizer.fit_transform(self.df['Comment'].values).toarray()
        self.model = NMF(n_components=self.n_topics).fit(vector)
        self.features = vectorizer.get_feature_names()
        self.matrix = self.model.transform(self.vectorizer)

    # From the matrix, retrieve top example, topics words, and number of comments per topics 
	def output_data(self):
		'''
        OUTPUT DataFrame
        '''
	    self.examples = []
	    self.comment = []
	    self.topic_words = []

	    # Retrieve the comment most relevant to each topic
	    index = self.matrix.argmax(axis=0)
	    self.df = self.df.reset_index()
	    self.examples.append(self.df.ix[index]['Comment'].values)
	    np.sort(self.matrix, axis =1)

	    # Retrieve all comments that are relevant to each topic
	    for i in range(self.n_topics):
	        self.comment.append(len(self.matrix[:,i][self.matrix[:,i] > 0.05]))
	    
	    self.num_per_topics = len(comments)

		# Retrieve top 10 topic words
	    for topic in self.model.components_:
	        topic_words.append(" ".join([self.features[i]
	                for i in topic.argsort()[:-10-1:-1]])) 

	    return self.examples, self.topic_words, self.num_per_topics 

	# Combine the examples, topic words, and number of comments per topic into a single dataframe
	
	def to_df(self):
		'''
	    OUTPUT DataFrame
		'''
		dat = list(izip(self.topic_words, self.examples))
		data = pd.DataFrame(list(izip(dat, self.num_per_topics)))
		data[['keys', 'examples']] = data[0].apply(pd.Series)
		data.rename(columns={1:'num'}, inplace=True)
		data.drop(0, axis = 1, inplace=True)
		return data

	# Combine positive sentiment dataframe and negative sentiment dataframe 
	def combine_df(df_pos, df_neg):
		'''
	    INPUT DataFrame, DataFrame
	    OUTPUT DataFrame
		'''
		comments = pd.concat([df_pos, df_neg], axis = 1)
		comments.columns = ['pos_key', 'pos_example', 'pos_num', 'neg_key', 'neg_example', 'neg_num']
		comments['pos_percent'] = comments['pos_num']/comments['pos_num'].sum()
		comments['neg_percent'] = comments['neg_num']/comments['neg_num'].sum()
		return comments


if __name__ == '__main__':
    candidates = ['hillary', 'sanders', 'biden', 'trump', 'bush', 'carson'] 
    
    for c in candidates:
        data = pd.read_csv('data/' + c + '_scores.csv')
        data[pd.isnull(data['Comment'])] = ""
        
        # Retrieving more negative (<-0.1) and more positive (>0.2) comments, ignore neutral comments
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
