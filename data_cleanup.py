import pandas as pd
from pattern.en import sentiment, polarity
from utils import clean_text, unix_convert, state_label

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

## Read longitude and latitude data for states
longlat = pd.read_csv('data/longlat.csv', error_bad_lines=False)

## Data transformation
terms= [['Hillary', 'Rodham', 'Mrs.Clinton'],
['Bernie', 'Sanders', 'Mr.Sanders'],
['Joe', 'Biden', 'Vice President'],
['Donald', 'Trump', 'Mr.Trump'].
['Jeb', 'Bush', 'Governor'],
['Ben', 'Carson', 'Dr.Carson']
]

candidates = ['hillary', 'sanders', 'biden', 'trump', 'bush', 'carson'] 

for index, c in candidates:
    data = pd.read_csv('data/'+c+'_meta.csv')
    data[pd.isnull(data['Comment'])] = ""
    data = data.drop_duplicates('Comment')
    data['candidate'] = c
    data['date'] = data['date'].apply(lambda x : unix_convert(x))
    data['Comment'] = data['Comment'].apply(lambda x: clean_text(str(x)))
    data['Sentiment_raw'] = data.apply(lambda row: sentiment(row['Comment']), axis = 1)
    data['Sentiment'] = data.apply(lambda row: sentiment_new(row['Comment'], terms[index]), axis = 1)
    data['State'] = data.apply(lambda row: state_label(str(row['Locations'])), axis = 1))
    data = pd.merge(data, longlat, how='left', on='State')
    data.to_csv('data/'+c+'_scores.csv')

## Saving a master version of all candidate data
hilary = pd.read_csv('data/hilary_scores.csv')
sanders = pd.read_csv('data/sanders_scores.csv') ###
biden = pd.read_csv('data/biden_scores.csv')
trump = pd.read_csv('data/trump_scores.csv')
bush = pd.read_csv('data/bush_scores.csv')
carson = pd.read_csv('data/carson_scores.csv') ###

master = pd.concat([hilary, sanders, biden, trump, bush, carson])

## Master data clean- up
master['EditorPick'] = master['EditorPick'].apply(lambda x: 0 if x == 'False' else x)
master['EditorPick'] = master['EditorPick'].apply(lambda x: 1 if x == 'True' else x)
master['EditorPick'] = master['EditorPick'].astype(float)
master['Recommendations'] = master['Recommendations'].apply(lambda x: 0 if type(x) == str else x)
master.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis = 1, inplace= True)
master.to_csv('data/master.csv')
