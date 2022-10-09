from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import panda as pd
import csv

with open("articles.csv") as d:
    reader=csv.reader(d)
    data=list(reader)
    articles=data[1:]

articles.sort_values(by="total_events", ascending=False)

print(articles[0:19])

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(articles['keywords'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

df = articles.reset_index()
indices = pd.Series(df.index, index=df['title'])

def getRecommendations(title, cosine_sim=cosine_sim2):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df['title'].iloc[movie_indices]