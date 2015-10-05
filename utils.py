import re
import string
import unidecode
import datetime
import json

def clean_text(text):
	#remove html links
    text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
    #remove html tags
    p = re.compile(r'<[^<]*?>')
    text = p.sub('', text)
    #remove possessives
   	text = unidecode.unidecode(text).replace("\n"," ").replace("\'s","").replace("\'t","")
   	return text

def unix_convert(x):
    	return pd.to_datetime(datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))


## Parse State data
with open('states.txt', 'r') as f:
     states = json.load(open("data/states.txt"))

def state_label(loc):
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

