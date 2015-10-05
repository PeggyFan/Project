
import pandas as pd
import pickle as pkl

from pymongo import MongoClient

def export_files(collection, name): 
    comments = list(db_comments.tab2.find({}, {'commentBody':1, 'web_url':1, 
                'recommendations':1, 'userLocation':1, 'editorsSelection': 1, 
                'userID':1, 'createDate':1, '_id':0})) #exclude ID
    text = []
    urls = []
    rec = []
    rec_flag = []
    locations = []
    editor = []
    userID = []
    date = []

    for i in range(len(comments)):
        if comments[i].get('commentBody') == None:
            pass
        else:
            text.append(comments[i]['commentBody'].encode('utf-8'))
            urls.append(comments[i]['web_url'])
            rec.append(comments[i]['recommendations'])
            comment = comments[i]['userLocation']
            locations.append(unicode(comment).encode("utf-8"))
            editor.append(comments[i]['editorsSelection'])
            userID.append(comments[i]['userID'])
            date.append(comments[i]['createDate'])

    text_pd = pd.Series(text)
    url_pd = pd.Series(urls)
    rec_pd = pd.Series(rec)
    locations_pd = pd.Series(locations)
    editor_pd = pd.Series(editor)
    userID_pd = pd.Series(userID)
    date_pd = pd.Series(date)

    meta = pd.concat([text_pd, url_pd, rec_pd, locations_pd, editor_pd, userID_pd, date_pd, rec_flag_pd], axis=1)
    meta.to_csv('../data/hillary_meta.csv')


# class MongoToDataFrame(object):

#     def __init__(self):
#         self.mongo_client = MongoClient()
#         # these columns will be stored in the output dataframe
#         self.columns = ['commentBody','web_url','recommendations','userLocation',
#         'editorsSelection', 'userID', 'createDate','content']
#         self.data = {col : [] for col in self.columns}
#         self.df = None

#     def create_dict(self, db_name):
#         '''
#         INPUT None
#         OUPUT DataFrame
#         Reads mongodb and inserts the required fields in a dict
#         '''
#         collection = self.mongo_client[db_comments]

#         for i in range(len(db_comments['commentBody'])):
#             for col in self.columns:
#                 self.data[col].append(db_comments[i]['commentBody'].encode('utf-8'))
#         return self.data


#     def create_df(self):
#         self.create_dict('nyt_tech')
#         self.create_dict('reuters')
#         self.df = pd.DataFrame(self.data)
#         # there are some duplicates in the db, so drop these here before further analysis
#         self.df.drop_duplicates('web_url', inplace=True)

#         self.df['headline_lower'] = self.df['headline'].map(lambda x : x.lower())
#         self.df.drop_duplicates('headline_lower', inplace=True)
#         del self.df['headline_lower']

#         #temporarily store only data for last three years
#         self.df['pub_date'] = pd.to_datetime(self.df['pub_date'])
#         self.df = self.df[self.df['pub_date'] > "2011-12-31"]
#         return self.df


#     def save_pickle_df(self, out_file):
#         '''
#         INPUT String
#         OUPUT None
#         '''
#         pkl.dump(self.df, open(out_file, "wb"))


#     def get_data_frame(self):
#         return self.df


# if __name__ == '__main__':
#     m2df = MongoToDataFrame()
#     m2df.create_df()
#     m2df.save_pickle_df("data/data_all.pkl")