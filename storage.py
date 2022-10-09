from main import Flask,jsonify, request
import csv

app = Flask(__name__)

articles=[]
likedArticles=[]
dislikedArticles=[]
with open("articles.csv") as d:
    reader=csv.reader(d)
    data=list(reader)
    articles=data[1:]

@app.route("/", methods=["GET"])
def getArticles():
    return jsonify({
        "data": articles[0],
        "status": 'success'
    }),200

@app.route("/liked-article")
def liked_article():
    article_info = articles[0]
    likedArticles.append(article_info)
    articles.drop([0], inplace=True)
    articles = articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

@app.route("/disliked-article",)
def disliked_article():
    article_info = articles[0]
    dislikedArticles.append(article_info)
    articles.drop([0], inplace=True)
    articles = articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

if __name__=="__main__":
    app.run()