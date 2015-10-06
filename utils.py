import pandas as pd
import numpy as np
import re
import string
import unidecode
import datetime
import json
from pattern.en import polarity
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
snowball = SnowballStemmer('english')

# Remove unwanted characters
def clean_text(text):
	#remove html links
    text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
    #remove html tags
    p = re.compile(r'<[^<]*?>')
    text = p.sub('', text)
    #remove possessives
    text = unidecode.unidecode(text).replace("\n"," ").replace("\'s","").replace("\'t","")
    return text

#Parse datetime data
def unix_convert(x):
    return pd.to_datetime(datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))

## Parse State data
with open('data/states.txt', 'r') as f:
     states = json.load(open('data/states.txt'))

def state_label(text):
    def get_state(x):
        x_val = x.lower().title()
        if x_val in states.values():
            return states.keys()[states.values().index(x_val)]
        elif x in states.keys():
            return x
        else:
            return None

    if get_state(loc) != None:
        return get_state(loc)
    else: 
        tokens = loc.upper().split(', ')
        if len(tokens) == 1:
            return get_state(tokens[0])
        else:
            return get_state(tokens[1])

# Tokenize
def tokenize(text):
    if text == np.nan:
        pass
    else:
        return [snowball.stem(word) for word in word_tokenize(doc.lower())]


#Get the sentiment score of the entire comment
def sentiment(text):
    return polarity(text)

#Get the sentiment score of the most extreme sentence in a given comment
def sentiment_new(text, terms):
    def sentiment(text):
        return polarity(text)
        
    def Sentences(paragraph):
        sentenceEnders = re.compile('[.!?]')
        sentenceList = sentenceEnders.split(paragraph)
        return sentenceList

    def to_filter(text, terms):
        if any(word in text for word in terms):
            return text
        else:
            return np.nan 

    target= []  
    
    for i in Sentences(text):
        if to_filter(i, terms) == None:
            pass
        else:
            target.append(i)
            
    s_max = 0
    comment_score = 0
    
    for i in target:
        if abs(sentiment(i)) > abs(s_max):
            comment_score = sentiment(i)
            s_max = sentiment(i)
    
    return comment_score