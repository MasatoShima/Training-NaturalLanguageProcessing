"""
Name: sample_07_01.py
Description: TF-IDF を算出する
Created by: Masato Shima
Created on: 2019/09/11
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer

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

	# doc_id ごとに TF-IDF の値が高い単語を表示
	# まずは, doc_id に紐づく meta データを取得
	for doc_id, vec in zip(doc_ids, vectors.toarray()):
		# meta データから doc_id に紐づく title を取得
		meta_info = json.loads(
			datastore.get(doc_id, ["meta_info"])["meta_info"]
		)

		title = meta_info["title"]

		print(doc_id, title)

		# TF-IDF を出力
		for w_id, tf_idf in sorted(enumerate(vec), key=lambda x: x[1], reverse=True)[:10]:
			lemma = vectorizer.get_feature_names()[w_id]

			print(f"\t{lemma}: {tf_idf}")

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
