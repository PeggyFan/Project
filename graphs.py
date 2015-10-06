import plotly.tools as tls
tls.set_credentials_file(username=username, api_key=key)
credentials = tls.get_credentials_file()

import plotly.plotly as py
from plotly.graph_objs import *
from topic_modeling import Model

candidates = ['hillary', 'sanders', 'biden', 'trump', 'bush', 'carson'] 

for c in candidates:
	data = pd.read_csv('data/' + c + '_topics.csv')

	#Positive sentiment graph
	data = Data([
	    Bar(
	        y=data['pos_keys'],
	        x=data['pos_percent'],
	        text=data['pos_example'],
	        orientation = 'h',
	        marker=Marker(
	            color='rgb(224, 102, 102)',
	            opacity=0.6,       
	        ),
	        opacity=0.6, 
     
	    )
	    
	])

	layout = Layout(
	    title='Positive Sentiment',
	    xaxis=XAxis(
	        title='Proportion of comments',
	        titlefont=Font(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        )
	    ),
	    
	    width=900,
	    height=600,

	    margin=Margin( # set frame to plotting area margins
	        t=100,     #   top,
	        b=100,     #   bottom,
	        r=10,      #   right,  
	        l=250#   left
	    ),

	    yaxis=YAxis(
	        title='',
	        titlefont=Font(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        )
	    )
	)

	fig = Figure(data=data, layout=layout)
	py.iplot(fig, validate=False, filename= c + '_pos')


	#Negative sentiment graph
	data = Data([
	    Bar(
	        y=data['neg_keys'],
	        x=data['neg_percent'],
	        text=data['neg_example'],
	        orientation = 'h',
	        marker=Marker(
	            color='rgb(224, 102, 102)',
	            opacity=0.6,       
	        ),
	        opacity=0.6, 
	    )

	])

	layout = Layout(
	    title='Negative Sentiment',
	    xaxis=XAxis(
	        title='Proportion of comments',
	        titlefont=Font(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        )
	    ),
	    
	    width=900,
	    height=600,

	    margin=Margin( # set frame to plotting area margins
	        t=100,     #   top,
	        b=100,     #   bottom,
	        l=250,      #   left,
	        r=10       #   right
	    ),
	    
	    yaxis=YAxis(
	        title='',
	        titlefont=Font(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        )
	    )
	)

	fig = Figure(data=data, layout=layout)
	py.iplot(fig, validate=False, filename= c + '_neg')


#Define period by months
def period_convert(x):
    	return pd.to_datetime(datetime.datetime.fromtimestamp(x).strftime('%Y-%m'))



	#Transform date into months
	data['new_date'] = data['date'].apply(lambda x : period_convert(x))
	data['new_date'] = data['new_date'].astype(int)
	list_ = data['new_date'].unique()

	#Subset data by months
	text_count = []

	for i in list_:
	    text_count.append(data.ix[data['new_date'] == i]['Comment'])

	#Get topics and topic keywords for each month
	topics = []
	for i in range(len(text_count)):
    	keyterms = []
		model = Model(n_topics=5, df=df, vectorizer=vectorizer, vector=vector)
		model.build_model()
		examples, topic_words, num_per_topics  = model.output_data()
		keyterms.append(topic_words)
	topics.append(keyterms) 

    #Get number of comments within each month for plotting
	counts = pd.DataFrame(data['new_date'].value_counts()).reset_index()
	counts.columns = ['new_date', 'count']
	counts.sort('new_date', inplace=True)

	#Repeat the last time point for graphing
	counts.loc[-1] = np.array(['2015-10', 2014])

	#Plot in plot.ly

	trace1 = Scatter(
	        x=counts['new_date'],
	        y=counts['count'],
	        fill='tozeroy'
	)

	data = Data([trace1])

	layout = Layout(
	    title='Topic trends, 2015/07-2015/09',
	    titlefont=Font(
	            family='Arial, sans-serif',
	            size=24),
	    
	    showlegend=False,
	    xaxis=XAxis(
	        title='Time',
	    ),
	    
	    annotations=Annotations([

	        Annotation(
	            font=Font(
	            family='Open Sans',
	            size=16,
	            color='#000000'
	            ),
	                
	            x='2010',
	            y=1500,
	            xref='x',
	            yref='y',
	            text=topics[0],
	            showarrow=True,
	            arrowhead=2,
	            bgcolor='#FFF2CC',
	            opacity=0.8
	        ),
	            
	        Annotation(
	            font=Font(
	            family='Open Sans',
	            size=16,
	            color='#000000'
	            ),
	                
	            x='2011',
	            y=1500,
	            xref='x',
	            yref='y',
	            text=topics[1],,
	            showarrow=True,
	            arrowhead=2,
	            bgcolor='#EAD1DC',
	            opacity=0.8
	        ),
	        
	        Annotation(
	            font=Font(
	            family='Open Sans',
	            size=16,
	            color='#000000'
	            ),
	                
	            x='2012',
	            y=1500,
	            xref='x',
	            yref='y',
	            text=topics[1],
	            showarrow=True,
	            arrowhead=2,
	            bgcolor='#FCE5CD',
	            opacity=0.8
	        ),
	            
	    # Annotation(
	    #         font=Font(
	    #         family='Open Sans',
	    #         size=16,
	    #         color='#000000'
	    #         ),
	                
	    #         x='2013',
	    #         y=1500,
	    #         xref='x',
	    #         yref='y',
	    #         text='rand paul consistent power<br>collins madison reform',
	    #         showarrow=True,
	    #         arrowhead=2,
	    #         bgcolor='#EEEEEE',
	    #         opacity=0.8
	    #     ),
	          
	    #     Annotation(
	    #         font=Font(
	    #         family='Open Sans',
	    #         size=16,
	    #         color='#000000'
	    #         ),
	                
	    #         x='2014',
	    #         y=1500,
	    #         xref='x',
	    #         yref='y',
	    #         text='public servants afford bankrupt kleptocrats<br>infrastructure pay equity',
	    #         showarrow=True,
	    #         arrowhead=2,
	    #         bgcolor='#D9EAD3',
	    #         opacity=0.8
	    #     ),
	            
	    #     Annotation(
	    #         font=Font(
	    #         family='Open Sans',
	    #         size=16,
	    #         color='#000000'
	    #         ),
	                
	    #         x='2015',
	    #         y=1500,
	    #         xref='x',
	    #         yref='y',
	    #         text='win primary election general 2016 running<br> american resonates ages democratic',
	    #         showarrow=True,
	    #         arrowhead=2,
	    #         bgcolor='#EEEEEE',
	    #         opacity=0.8
	    #     ),
	        
	        
	        
	        ]),
	    
	    width=1300,
	    height=550,
	    
	    margin=Margin( # set frame to plotting area margins
	        t=100,     #   top,
	        b=100,     #   bottom,
	        r=20,      #   right,  
	        l=80#   left
	    ),
	    yaxis=YAxis(
	        title='Number of comments',
	        titlefont=Font(
	            family='Open Sans',
	            size=14,
	            color='#000000'
	    )
	    ))
	    
	fig = Figure(data=data, layout=layout)
	py.iplot(fig, validate=False, filename= c + '_time')
