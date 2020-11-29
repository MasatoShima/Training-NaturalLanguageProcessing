"""
Name: word2vec.py
Description: 
Created by: Masato Shima
Created on: 2019/09/25
"""

# **************************************************
# ----- Import Library
# **************************************************
import gensim
from typing import *


# **************************************************
# ----- Variables
# **************************************************
model = gensim.models.Word2Vec("./data/ja.bin")


# **************************************************
# ----- Data Model
# **************************************************


# **************************************************
# ----- Function get_synonyms
# **************************************************
def get_synonyms(text):
	results = []

	for word, sim in model.most_similar(text, topn=10):
		results.append(
			{
				"term": word,
				"similarity": sim
			}
		)

	return results


# **************************************************
# ----- Function calc_similarity
# **************************************************
def calc_similarity(text1, text2):
	sim = model.similarity(text1, text2)

	return sim


# **************************************************
# ----- Function analogy
# **************************************************
def analogy(xy1, x2):
	x1, y1 = xy1

	results = []

	for word, sim in model.most_similar(positive=[y1, x1], negative=[x2], topn=10):
		results.append(
			{
				"term": word,
				"similarity": sim
			}
		)

	return results


# **************************************************
# ----- End
# **************************************************
