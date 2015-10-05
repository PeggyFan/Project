#NYT Summarizer: A New York Times Comments Summarizer on Presidential Candidates

Data visualization using topic modeling to explore what the comments discuss and how posters feel about each candidate.

<br>
<br>
![](images_readme/Late_summer.png)
<br>
<br>
Before I go into the motivation, the data, and the modeling process, I would like to explain verbally and visually the directory structure of this repo.

## Repo Structure

This project repo is divided into three main directories: App, GetData, and Recommender.

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


