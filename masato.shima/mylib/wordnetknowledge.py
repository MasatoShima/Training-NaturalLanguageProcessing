"""
Name: wordnetknowledge.py
Description: wordnet を用いた単語の類似語および類似度, 上位語・下位語を取得する
Created by: Masato Shima
Created on: 2020/01/12
"""

# **************************************************
# ----- Import Library
# **************************************************
from typing import *

from nltk.corpus import wordnet


# **************************************************
# ----- Function get_synonyms
# **************************************************
def get_synonyms(text: str) -> List[Dict[str, str], ]:
	# wordnet を用いて, 引数で渡された単語の類似語を取得する
	results = []

	# text の synset を取得
	# 取得した synset を表すテキストを取得
	for synset in wordnet.synsets(text, lang="jpn"):
		for lemma in synset.lemma_names(lang="jpn"):
			results.append({"term": lemma})

	return results


# **************************************************
# ----- Function calc_similarity
# **************************************************
def calc_similarity(text1: str, text2: str):
	# wordnet を活用して, 単語の類似度を算出する

	# それぞれの単語の synset を取得
	synsets1 = wordnet.synsets(text1, lang="jpn")
	synsets2 = wordnet.synsets(text2, lang="jpn")

	# 取得したそれぞれの synset を比較し, 最も値が大きいものを類似度として採用する
	max_sim = 0.0

	for synset1 in synsets1:
		for synset2 in synsets2:
			sim = synset1.path_similarity(synset2)

			if max_sim < sim:
				max_sim = sim

	return max_sim


# **************************************************
# ----- Function get_hypernym
# **************************************************
def get_hypernym(text: str) -> List[Dict[str, str], ]:
	# wordnet を用いて, 引数で渡された単語の上位語を取得する

	# text の synset を取得
	synsets = wordnet.synsets(text, lang="jpn")

	# それぞれの synset の上位語に相当する synset を取得し,
	# results に格納
	results = []

	for synset in synsets:
		for hypernym in synset.hypernyms():
			for lemma in hypernym.lemma_names(lang="jpn"):
				results.append({"term": lemma})

	return results


# **************************************************
# ----- Function get_hyponym
# **************************************************
def get_hyponym(text: str) -> List[Dict[str, str], ]:
	# wordnet を用いて, 引数で渡された単語の下位語を取得する

	# text の synset を取得
	synsets = wordnet.synsets(text, lang="jpn")

	# それぞれの synset の下位語に相当する synset を取得し,
	# results に格納
	results = []

	for synset in synsets:
		for hyponym in synset.hyponyms():
			for lemma in hyponym.lemma_names(lang="jpn"):
				results.append({"term": lemma})

	return results


# **************************************************
# ----- End
# **************************************************
