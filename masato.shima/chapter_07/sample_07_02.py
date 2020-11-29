"""
Name: sample_07_02
Description: コサイン類似度を算出する
Created by: Masato Shima
Created on: 2019/09/11
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from mylib import sqlitedatastore as datastore


# **************************************************
# ----- Main
# **************************************************
def main():
	# SQLite に接続
	datastore.connect()

	data = []
	doc_ids = []

	# doc_id を 1つずつ取得し, それに含まれている単語の原形を取得
	for doc_id in datastore.get_all_ids(limit=-1):
		lemmas = [
			token["lemma"]
			for token in datastore.get_annotation(doc_id, "token")
		]

		data.append(" ".join(lemmas))
		doc_ids.append(doc_id)

	# TF-IDF を算出
	vectorizer = TfidfVectorizer(analyzer="word", max_df=0.9)
	vectors = vectorizer.fit_transform(data)

	# コサイン類似度を算出
	sim = cosine_similarity(vectors)

	# doc_id と, それに対するコサイン類似度の算出結果を紐づけ
	docs = zip(doc_ids, sim[0])

	# doc_id ごとに コサイン類似度にもとづく類似度の高い文書を表示
	# まずは, doc_id に紐づく meta データを取得
	for doc_id, similarity in sorted(docs, key=lambda x: x[1], reverse=True):
		meta_info = json.loads(
			datastore.get(doc_id, ["meta_info"])["meta_info"]
		)

		title = meta_info["title"]

		# doc_id とコサイン類似度にもとづく類似度の高い文書, その値を出力
		print(doc_id, title, similarity)

	datastore.close()

	return


# **************************************************
# ----- Main Process
# **************************************************
if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	main()


# **************************************************
# ----- End
# **************************************************
