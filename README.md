##NYT Summarizer: A New York Times Comments Summarizer on Presidential Candidates


<br>
<br>
![](images_readme/Late_summer.png)
<br>
<br>

## Overview

This project uses topic modeling and data visualization to explore user discussions and sentiments on the New York Times in regards to six current presidential candidates.

The goal is to find meaingful patterns in discussions about the candidates and detect how users feel towards various issues for individual candidates. For each candidate, I use sentiment analysis to classify positive and negative comments (about 25,000 comments per candidate) and topic modeling to discover issues about which users feel positive and negative towards the candidate.

My results capture the prevailing issues surrounding each candidate and showcase a typical comment for each positive and negative topic. This serves as a summarizer of the current discusssions and provides additional information on the comments' curation by New York times. 

http://nytsummarizer.us

## Process in detail
The main features of my modeling is sentiment classification and topic words.
For sentiment classification, I use Pattern, a Python package that takes in a piece of text and gives a sentiment score between -1 and 1 (most negative to most positive). I performed sentiment analysis on each comment in its entirety as well as at sentence level. In the end, I choose to use sentiment score at the sentence-level since it gives better signal than score on the entire comment, which tend to be very close to zero (neutral).

I use Non-negative Matrix Factorialization 

What algorithms and techniques did you use?
How did you validate your results?
What interesting insights did you gain?


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
|   └── graphs.py

```


1. **`App`**: This directory contains the web application using Flask `app.py` , and templates of candidate's pages.
2. **`Data preparation`**: The `web_scrape.py` gets data from the New York Times Articles Search API and Community API (for user comments) and stores in MongoDB databases. `mongodb_toDF.py` transfers the data from the Mongodb databases to python in form of dataframes. The `data_cleanup.py` then prepares the data for modeling and analyses in which `utils.py` is used to accomplish major tasks such as removing non-essential characters, calculating sentiment scores, converting the date field, and parsing location data.
3. **`Modeling & Visualization`** has `topic_modeling.py`, which performs topic modeling on given data and output topic key words, example texts, and number of texts. `graphs.py` covers the visualization using plot.ly


