import pandas as pd
import pickle as pkl
from utils import clean_text, unix_convert, state_label, sentiment, sentiment_new

## Read longitude and latitude data for states

class Data_transform(object):

    def __init__(self, df):
        self.df = df
        # these columns will be stored in the output dataframe
        self.longlat = pd.read_csv('data/longlat.csv', error_bad_lines=False)
    ## Data transformation

    def df_transform(self, terms):    
        self.df[pd.isnull(self.df['Comment'])] = ""
        self.df = self.df.drop_duplicates('Comment')
        self.df['date'] = self.df['date'].apply(lambda x : unix_convert(x))
        self.df['Comment'] = self.df['Comment'].apply(lambda x: clean_text(str(x)))
        self.df['Sentiment_raw'] = self.df.apply(lambda row: sentiment(row['Comment']), axis = 1)
        self.df['Sentiment'] = self.df.apply(lambda row: sentiment_new(row['Comment'], terms), axis = 1)
        self.df['State'] = self.df.apply(lambda row: state_label(str(row['Locations'])), axis = 1)
        self.df = pd.merge(self.df, self.longlat, how='left', on='State')

    def save_df(self, out_file):
        '''
        INPUT String
        OUPUT None
        '''
        pkl.dump(self.df, open(out_file, "wb"))

if __name__ == '__main__':
    
    terms= [['Hillary', 'Rodham', 'Mrs.Clinton'],
    ['Bernie', 'Sanders', 'Mr.Sanders'],
    ['Joe', 'Biden', 'Vice President'],
    ['Donald', 'Trump', 'Mr.Trump'],
    ['Jeb', 'Bush', 'Governor'],
    ['Ben', 'Carson', 'Dr.Carson']
    ]

    candidates = ['hillary', 'sanders', 'biden', 'trump', 'bush', 'carson'] 

    for index, c in candidates:
        raw = pd.read_csv('data/' + c + '_meta.csv')
        data = Data_transform(raw)
        data.df_transform(terms[index])
        data.save_df('data/' + c + 'scores.csv')


## Saving a master version of all candidate data
# hilary = pd.read_csv('data/hilary_scores.csv')
# sanders = pd.read_csv('data/sanders_scores.csv') ###
# biden = pd.read_csv('data/biden_scores.csv')
# trump = pd.read_csv('data/trump_scores.csv')
# bush = pd.read_csv('data/bush_scores.csv')
# carson = pd.read_csv('data/carson_scores.csv') ###

# master = pd.concat([hilary, sanders, biden, trump, bush, carson])

# ## Master data clean- up
# master['EditorPick'] = master['EditorPick'].apply(lambda x: 0 if x == 'False' else x)
# master['EditorPick'] = master['EditorPick'].apply(lambda x: 1 if x == 'True' else x)
# master['EditorPick'] = master['EditorPick'].astype(float)
# master['Recommendations'] = master['Recommendations'].apply(lambda x: 0 if type(x) == str else x)
# master.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis = 1, inplace= True)
# master.to_csv('data/master.csv')
