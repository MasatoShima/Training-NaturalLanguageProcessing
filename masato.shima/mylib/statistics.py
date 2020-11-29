"""
Name: Masato Shima
Description: 
Created by: Masato Shima
Created on: 2019/11/24
"""

# **************************************************
# ----- Import Library
# **************************************************
from typing import *

from nltk.lm import Vocabulary
from nltk.lm.models import MLE
from nltk.util import ngrams

from mylib import sqlitedatastore as datastore
from mylib.annoutil import find_xs_in_y


# **************************************************
# ----- Function create_language_model
# **************************************************
def create_language_model(
		doc_ids: List[str, ],
		n: int = 3
) -> MLE:
	sentences = []

	# doc_id を 1つず処理していく
	for doc_id in doc_ids:
		# doc_id に紐づく単語を取得
		all_tokens = datastore.get_annotation(doc_id, "token")

		# doc_id に紐づく文を取得
		# find_xs_in_y を使用し, 文に含まれている単語のみを抽出し, sentences に格納
		for sentence in datastore.get_annotation(doc_id, "sentence"):
			tokens = find_xs_in_y(all_tokens, sentence)

			sentences.append(["__BOS__"] + [token['lemma'] for token in tokens] + ["__EOS__"])

	# ボキャブラリを作成
	vocab = Vocabulary([word for sentence in sentences for word in sentence])

	# n-gram を利用して, 1組 n 個の単語の組み合わせ作成
	ngram = [ngrams(sentence, n) for sentence in sentences]

	# MLE というモデルを用いて, 言語モデルを作成
	lm = MLE(order=n, vocabulary=vocab)
	lm.fit(ngram)

	return lm


# **************************************************
# ----- Function calc_prob
# **************************************************
def calc_prob(
		lm: MLE,
		lemmas,
		n: int = 3
) -> float:
	probability = 1.0

	for ngram in ngrams(lemmas, n):
		prob = lm.score(
			lm.vocab.lookup(ngram[-1]),
			lm.vocab.lookup(ngram[:-1])
		)

		prob = max(prob, 1e-8)

		probability *= prob

	return probability


# **************************************************
# ----- End
# **************************************************
