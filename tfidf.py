from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity

import numpy as np
import pandas as pd


df = pd.read_csv("fardanews2-14001.csv")
docs=df['article.title'].to_list()
print(type(docs))

#corpus = [x for x in df.to_dict(orient='index').values()]
#docs = [row['title'] for row in corpus if len(str(row.get('title'))) > 10]


vectorizer = TfidfVectorizer()
tfidf_docs = vectorizer.fit_transform(docs)


# query
query = 'حذف فقر'
tfidf_query = vectorizer.transform([query])[0]

# similarities
cosines = []
for d in tfidf_docs:
  cosines.append(float(cosine_similarity(d, tfidf_query)))
  
# sorting
k = 10
sorted_ids = np.argsort(cosines)
for i in range(k):
  cur_id = sorted_ids[-i-1]
  print(docs[cur_id], cosines[cur_id])
  