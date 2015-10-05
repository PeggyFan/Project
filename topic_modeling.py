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
%matplotlib inline

class Model(object):

    def __init__(self, n_topics, df=None,
                 vectorizer=None, vector=None, outdir='data/'):
        self.n_topics = n_topics
        self.n_features = n_features
        self.df = df
        self.vectorizer = vectorizer
        self.vector = vector
        self.outdir = outdir

        #self.candidates = ['hillary', 'sanders', 'biden', 'trump', 'bush', 'carson'] 
	
        self.model = None
        self.matrix = None
        #Output file names:
        #self.model_file = self.outdir + c + '.csv'


	def remove_abb(self, text):
	    terms = [('mrs. ', ''), ('mr. ', ''), ('ms. ',''), ('dr. ',''), ('sen. ','')]
	    for k, v in mapping:
    		self.text = text.replace(k, v)
	     return self.text

	def vectorize(self):
		self.vectorizer = TfidfVectorizer(tokenizer=tokenize, stop_words = 'english')
		self.vector = self.vectorizer.fit_transform(df['Comment'].values).toarray()
    	return self.vectorizer, self.vector

    def build_model(self):
        self.vectorizer, self.vector = self.vectorize()
        self.model = NMF(n_components=self.n_topics).fit(self.vector)

	    self.features = self.vectorizer.get_feature_names()
	    self.matrix = nmf.transform(self.vectorizer)
	    
	    return self.matrix, self.model.components_, self.features

	def output_data(self):
	    examples = []
	    comment = []
	    topic_words = []

	    index = self.matrix.argmax(axis=0)
	    df = df.reset_index()
	    examples.append(df.ix[index]['Comment'].values)
	    np.sort(self.matrix, axis =1)

	    for i in range(self.n_topics):
	        comment.append(len(self.matrix[:,i][self.matrix[:,i] > 0.05]))
	    
	    num_per_topics = len(comments)

	    for topic in self.model.components_:
	        topic_words.append(" ".join([self.features[i]
	                for i in topic.argsort()[:-5 -1:-1]]))

	    return self.examples, self.topic_words, self.num_per_topics 

	def to_df(self):
		dat = list(izip(self.topic_words, self.examples))
		data = pd.DataFrame(list(izip(dat, self.num_per_topics)))
		data1 = [['keys', 'examples']] = data[0].apply(pd.Series)
		data1.rename(columns={1:'num'}, inplace=True)
		data1.drop(0, axis = 1, inplace=True)
		return data1

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
		pos = data[data['Sentiment'] > 0.2]
		neg = data[data['Sentiment'] < -0.1]
		dfs = [neg, pos]
		new_dfs= []

	    for idf in dfs:
	        model = Model(n_topics=10, df=df, vectorizer=vectorizer, vector=vector)
	        model.build_model()
	        model.output_data()
	        new_dfs.append(model.to_df)

		dataframe = combine_df(new_dfs[0], new_dfs[1])
		dataframe.to_csv('data/' + c + 'topics.csv')



####################################################
################### Original codes
####################################################
vectorizer = TfidfVectorizer(stop_words='english')
list_ = [pos, neg]
examples = []
num_per_topics = []
topics = []

for i in list_: 
    V = vectorizer.fit_transform(i['Comment'].values).toarray()
    features = vectorizer.get_feature_names()
    nmf = NMF(n_components=n).fit(V)
    matrix = nmf.transform(V)
    index = matrix.argmax(axis=0)
    i = i.reset_index()
    examples.append(i.ix[index]['Comment'].values)
    matrix = nmf.transform(V)
    np.sort(matrix, axis =1)
    values = []
    keyterms = []

    for i in range(10):
        values.append(len(matrix[:,i][matrix[:,i] > 0.05]))

    print("##################################################")
    for topic_idx, topic in enumerate(nmf.components_, 1):
        print("Topic #%d:" % topic_idx)
        print(" ".join([features[i]
                for i in topic.argsort()[:-5 -1:-1]]))

        keyterms.append(" ".join([features[i]
                for i in topic.argsort()[:-5 -1:-1]]))

    num_per_topics.append(values)
    topics.append(keyterms)

pos_examples = examples[0]
pos1= list(izip(topics[0], pos_examples))
data_pos = pd.DataFrame(list(izip(pos1, num_per_topics[0])))
data_pos[['pos_keys', 'pos_ex']] = data_pos[0].apply(pd.Series)
data_pos.rename(columns={1:'pos_num'}, inplace=True)
data_pos.drop(0, axis = 1, inplace=True)

neg_examples = examples[1]
neg1= list(izip(topics[1], neg_examples))
data_neg = pd.DataFrame(list(izip(neg1, num_per_topics[1])))
data_neg[['neg_keys', 'neg_ex']] = data_neg[0].apply(pd.Series)
data_neg.rename(columns={1:'neg_num'}, inplace=True)
data_neg.drop(0, axis = 1, inplace=True)

