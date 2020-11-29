"""
Name: sample_07_08
Description: トピックモデル（ LDA ）を用いて, テキストを分類する
Created by: Masato Shima
Created on: 2019/09/11
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import json
import itertools
import logging

from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel

from mylib import sqlitedatastore as datastore
from mylib.annoutil import find_xs_in_y


# **************************************************
# ----- logging
# **************************************************
logging.basicConfig(
	format="%(asctime)s: %(levelname)s : %(message)s",
	level=logging.INFO
)


# **************************************************
# ----- Main
# **************************************************
def main():
	# SQLite に接続
	datastore.connect()

	# dic_id を1つずつ取得し, その doc_id 内の文章ごとに含まれる単語の原形を sentences に格納
	sentences = []

	for doc_id in datastore.get_all_ids(limit=-1):
		all_tokens = datastore.get_annotation(doc_id, "token")

		for sentence in datastore.get_annotation(doc_id, "sentence"):
			tokens = find_xs_in_y(all_tokens, sentence)

			sentences.append(
				[
					token["lemma"] for token in tokens
					if token.get("NE") == "O"
				]
			)

	# 分析に使用する記事が少ないため, 20文を 1つの文書として扱うように sentence を結合
	n_sent = 20

	docs = [
		list(itertools.chain.from_iterable(sentences[i: i + n_sent]))
		for i in range(0, len(sentences), n_sent)
	]

	# LDA の計算に使用する単語を選定
	# - 出現頻度が 2つ未満の文書の場合, その単語は計算に使用しない（ no_below=2 ）
	# - 出現頻度が 3割以上の文書の場合, その単語は計算に使用しない（ no_above=0.3 ）
	dictionary = Dictionary(docs)
	dictionary.filter_extremes(no_below=2, no_above=0.3)

	# 単語の集まりを doc2bow method を用いて, 所定のデータ型に変換
	corpus = [dictionary.doc2bow(doc) for doc in docs]

	# LDA モデルを作成
	lda = LdaModel(corpus, num_topics=10, id2word=dictionary, passes=10)

	# 主題の確認
	# Topic の一覧を出力
	# Topic の一覧と合わせて, その Topic の中で確率値の大きい単語上位 10個を出力
	for topic in lda.show_topics(num_topics=-1, num_words=10):
		print(f"Topic id: {topic[0]}    Word: {topic[1]}")

	# 記事の主題分布の推定
	# doc_id ごとに確率値の大きい Topic を出力
	for doc_id in datastore.get_all_ids(limit=-1):
		meta_info = json.loads(
			datastore.get(doc_id=doc_id, fl=["meta_info"])["meta_info"]
		)

		title = meta_info["title"]
		print(title)

		doc = [
			token["lemma"] for token in datastore.get_annotation(doc_id, "token")
			if token.get("NE") == "O"
		]

		topics = sorted(
			lda.get_document_topics(dictionary.doc2bow(doc)),
			key=lambda x: x[1],
			reverse=True
		)

		for topic in topics:
			print(f"    Topic id: {topic[0]}    Prob: {topic[1]}")

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
