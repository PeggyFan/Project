##NYT Summarizer: A New York Times Comments Summarizer on Presidential Candidates


<br>
<br>
![](images_readme/NYT_summarizer1.png )
<br>
<br>

## Overview

This project uses topic modeling and data visualization to explore user discussions and sentiments on the New York Times in regards to six current presidential candidates.

- The goal is to find meaingful patterns in discussions about the candidates and detect how users feel towards various issues for individual candidates.
- For each candidate, I use sentiment analysis to classify positive and negative comments (about 25,000 comments per candidate) and topic modeling to discover issues about which users feel positive and negative towards the candidate.

My results capture the prevailing issues surrounding each candidate and showcase a typical comment for each positive and negative topic. This serves as a summarizer of the current discusssions and provides additional information on the comments' curation by New York times. 

http://nytsummarizer.us

<br>
<br>
![](images_readme/NYTsummarizer_ex2.png)
<br>
<br>

<br>
<br>
![](images_readme/NYTsummarizer_ex3.png)
<br>
<br>
 
## Process in detail
- The main features of my modeling is topic modeling by sentiments.
- For sentiment classification, I use  **`Pattern`**, a Python package that takes in a piece of text and gives a sentiment score between -1 and 1 (most negative to most positive). I perform sentiment analysis on each comment in its entirety as well as at sentence level. In the end, I choose to use sentiment score at the sentence-level since it gives better signal than score on the entire comment, which tend to be very close to zero (neutral).
- My analysis focuses on non-neutral comments and comments speficially discussed a particular candidate. I transform these comments into a corpus by tokenization and removal of stop words, and create tf-idf vectors. I use Non-negative Matrix Factorialization (NMF) for topic detection. This algorithm is chosen over alternatives such as LSA after comparing the results. NMF provides more distinct features (topic words) and more interpretable results.
- Validation is achieved by picking the optimal number of topics. I use PCA on the corpus to infer the number of components. I also try latent dirichlet allocation (LDA) and calculate the perplexity on a held-out set and the Kullback-Leibler divergence (entropy) on the clusters for a range of number of topics (5 to 20). In general the ideal number of topics falls between 5 and 10 for each model.


## Insights
- The visualization presents topics in recent news surrounding each candidate, and while comments vary, it is able to retrive a typical comment that captures the topic’s idea. 
- Exploratory analyses show that the comments on the New York Times are highly curated and balanced. It is not a good dataset for (comment-to-candidate) classification problem as the signals (sentiment, relevancy) are muted.
- As the results demonstrate, the conversations around presidential candadates are diffuse, that is, comments often mention mutiple candidates. This presents difficulty in creating distinct candidate clusters. Often times, it is easier to create issue clusters. 

**Detailed discussions on my analytical choices can be found here: http://www.peggyfan.wordpress.com**

## Repo Structure
```
.
├── App
|   ├── app.py
|   ├── static
|   └── templates
├── Data preparation
|   ├── web_scrape.py
|   └── mongodb_toDF.py
|   └── data_cleanup.py
|   └── utils.py
├── Modeling & Visualization
|   ├── topic_modeling.py
|   └── similarity.py
|   └── graphs.py

```


1. **`App`**: This directory contains the web application using Flask `app.py` , and templates of candidate's pages.
2. **`Data preparation`**: The `web_scrape.py` gets data from the New York Times Articles Search API and Community API (for user comments) and stores in MongoDB databases. `mongodb_toDF.py` transfers the data from the Mongodb databases to python in form of pandas dataframes. The `data_cleanup.py` then prepares the data for modeling and analyses, in which `utils.py` is used to accomplish major tasks such as removing non-essential characters, calculating sentiment scores, converting date field, and parsing location data.
3. **`Modeling & Visualization`** has `topic_modeling.py`, which performs topic modeling on given data and output topic key words, example texts, and number of texts.`similarities.py` calculates the similarity between each comment and its respective article to provide a measure of relevance. It was originally developed as a feature in building a candidate classifier. It then is used to demonstrate overall data patterns. `graphs.py` covers the visualization using plot.ly and cartoDB.

## Future steps
- Re-visit the classification problem by doing more feature engineering. For example, using distinct topics associated with each candidate or other measures (subjectivity) to improve classification results.
- Get more precise clustering by examining on what topics are the comments overlapping for candidates. For instance, plotting the comments on two axises each representing a topic.
- Collect data for longer period of time and combine both the comments and news cycles (articles) to predict emerging topics.
