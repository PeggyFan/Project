import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import gensim
from gensim import corpora, models, similarities, matutils
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models.ldamodel import LdaModel
import scipy.stats as stats
import random
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from numpy.linalg import svd
scaler = StandardScaler()
from collections import defaultdict

data = pd.read_csv('../data/' + candidate '_scores.csv') #load the data for each candidate
data1 = data[(data['Sentiment'] < -0.1) | (data['Sentiment'] > 0.2)] #keep only non-neutral comments
data1[pd.isnull(data['Comment'])] = ""

### PCA
def pca_train(text):
    content = text 
    texts = [[word for word in comment.lower().split() if word not in stopwords.words('english')]
        for comment in content]
    vectorizer = TfidfVectorizer(stop_words='english')
    V = vectorizer.fit_transform(data1['Comment'].values).toarray()
    X_train = scaler.fit_transform(V)
    pca = PCA(n_components=30)
    X_pca = pca.fit_transform(X_train)
    return X_pca

X_pca = pca_train(data1['Comment'].values)

def scree_plot(pca, title=None):
    num_components = pca.n_components_
    ind = np.arange(num_components)
    vals = pca.explained_variance_ratio_
    plt.figure(figsize=(12, 10), dpi=250)
    ax = plt.subplot(111)
   
    ax.set_ylim(0, max(vals)+0.05)
    ax.set_xlim(0-0.45, 8+0.45)

    ax.set_xlabel("Principal Component", fontsize=12)
    ax.set_ylabel("Variance Explained (%)", fontsize=12)

    if title is not None:
        plt.title(title, fontsize=16)

scree_plot(X_pca, title = "PCA")

## Using gensim's LDA model

## Remove words that appear only once
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1]
          for text in texts]

# Create TF-IDF for LDA
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
model = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=5)
model.print_topics(5)

grid = defaultdict(list)
    
# Shuffle corpus and split into 80% training the 20% test sets
cp = list(corpus)
random.shuffle(cp)
p = int(len(cp) * .8)
cp_train = cp[0:p]
cp_test = cp[p:]
parameter_value = [5, 10, 15, 20, 25] # Number of topics to be compared

# Calculate Perplexity for each parameter value
for i in parameter_value:
    lda = gensim.models.ldamodel.LdaModel(corpus=cp_train, id2word=dictionary, num_topics=i,
                                          update_every=1, chunksize=1000, passes=2)
        
    perplex = model.bound(cp_test)
    print "Perplexity: %s" % perplex
    grid[i].append(perplex)
    
    per_word_perplex = np.exp2(-perplex / sum(cnt for document in cp_test for _, cnt in document))
    print "Per-word Perplexity: %s" % per_word_perplex
    grid[i].append(per_word_perplex)

data = pd.DataFrame(grid)

# Use KL Divergence to check resulting clusters

# Define KL function
def sym_kl(p,q):
    return np.sum([stats.entropy(p,q),stats.entropy(q,p)])

l = np.array([sum(cnt for _, cnt in doc) for doc in corpus])

def kl_calc(corpus, dictionary, max_topics, min_topics=1, step=1):
    kl = []
    for i in range(min_topics,max_topics,step):
        lda = models.ldamodel.LdaModel(corpus=corpus,id2word=dictionary,num_topics=i)
        m1 = lda.expElogbeta
        U,cm1,V = np.linalg.svd(m1)

        #Document-topic matrix
        lda_topics = lda[corpus]
        m2 = matutils.corpus2dense(lda_topics, lda.num_topics).transpose()
        cm2 = l.dot(m2)
        cm2 = cm2 + 0.0001
        cm2norm = np.linalg.norm(l)
        cm2 = cm2/cm2norm
        kl.append(sym_kl(cm1,cm2))
    return kl


kl = kl_calc(corpus,dictionary,max_topics=30)

# Plot kl divergence against the numbers of topics
plt.figure(figsize=(15,10))
plt.plot(kl)
plt.ylabel('Symmetric KL Divergence', fontsize = 18)
plt.xlabel('Number of Topics', fontsize = 18)
plt.title('Evaluating number of topics', fontsize = 22)
plt.savefig('kldiv.png', bbox_inches='tight')
