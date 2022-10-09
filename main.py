from flask import Flask, jsonify, request
import pandas as pd
from demographic_filtering import output
from content_filtering import getRecommendations

df = pd.read_csv('articles.csv')
articles = df[['url' , 'title' , 'text' , 'lang' , 'total_events', 'contentId']]

app = Flask(__name__)

liked_articles = []
not_liked_articles = []

def assign_val():
    m_data = {
        "url": articles.iloc[0,0],
        "title": articles.iloc[0,1],
        "text": articles.iloc[0,2] or "N/A",
        "lang": articles.iloc[0,3],
        "total_events": str(articles.iloc[0,4]),
        "contentId" : str(articles.iloc[0,5])
    }
    return m_data

@app.route("/get-article")
def get_article():

    articleInfo = assign_val()
    return jsonify({
        "data": articleInfo,
        "status": "success"
    })

@app.route("/liked-article")
def liked_article():
    global all_articles
    articleInfo = assign_val()
    liked_articles.append(articleInfo)
    all_articles.drop([0], inplace=True)
    all_articles = all_articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

@app.route("/unliked-article")
def unliked_article():
    global all_articles
    articleInfo = assign_val()
    not_liked_articles.append(articleInfo)
    all_articles.drop([0], inplace=True)
    all_articles = all_articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

@app.route("/popular-articles")
def popular_articles():
    articleInfo = []
    for index , row in output.iterrows():
        _d = {
            "url": row['url'],
            "title": row['title'],
            "text": row['text'],
            "lang": row['lang'],
            "total_events": row['total_events']
        }
        articleInfo.append(_d)

    return jsonify({
        "data": articleInfo,
        "status": "success"
    })

@app.route("/getRecommendation", methods=["GET"])
def getRecommendation(search):
    col_names=['url', 'title', 'text', 'lang', 'total_events']
    articlesRecomded = pd.DataFrame(columns=col_names)
    
    for article in liked_articles:
        output = getRecommendations(article["contentId"])
        all_recommended=all_recommended.append(output)

    articlesRecomded.drop_duplicates(subset=["title"],inplace=True)

    dataRecommended = []

    for index, row in articlesRecomded.iterrows():
        _d = {
            "url": row['url'],
            "title": row['title'],
            "text": row['text'],
            "lang": row['lang'],
            "total_events": row['total_events']
        }
        dataRecommended.append(_d)

    return jsonify({
        "data":dataRecommended,
        "status": "success"
    })