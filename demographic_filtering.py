import numpy as np
import csv

with open("articles.csv") as d:
    reader=csv.reader(d)
    data=list(reader)
    articles=data[1:]

articles.sort_values(by="total_events", ascending=False)

output=list(articles[["url", "title", "text", "lang", "total_events"]].head(20))