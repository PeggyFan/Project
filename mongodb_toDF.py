
import pandas as pd
import pickle as pkl
from pymongo import MongoClient

class MongoToDataFrame(object):

    def __init__(self):
        self.mongo_client = MongoClient()
        # these columns will be stored in the output dataframe
        self.columns = ['web_url','headline','pub_date','content']
        self.data = {col : [] for col in self.columns}
        self.df = None

    def create_df(self, database, collection):
        db = client[database]
        coll = db[collection]
        coll_dict = list(coll.find({}, {'commentBody':1, 'web_url':1, 
                'recommendations':1, 'userLocation':1, 'editorsSelection': 1, 
                'userID':1, 'createDate':1, '_id':0}))
        self.df = pd.DataFrame(coll_dict)

        return self.df

    def save_pickle_df(self, out_file):
        '''
        INPUT String
        OUPUT None
        '''
        pkl.dump(self.df, open(out_file, "wb"))

    def get_data_frame(self):
        return self.df


if __name__ == '__main__':

    candidates = ['hillary', 'sanders', 'biden', 'trump', 'bush', 'carson'] 
    for c in candidates:
        to_df = MongoToDataFrame()
        to_df.create_df('nyc_comments', 'tab_'+c)
        to_df.save_pickle_df('data/' + c + '_data.pkl')
        
    ##