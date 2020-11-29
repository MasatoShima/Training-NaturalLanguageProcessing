"""
Name: sample_10_02.py
Description: 
Created by: Masato Shima
Created on: 2019/10/09
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
from typing import *

from mylib import ruleclassifier
from mylib import solrindexer as indexer
from mylib import sqlitedatastore as datastore
from mylib.annoutil import find_xs_in_y


# **************************************************
# ----- Variables
# **************************************************


# **************************************************
# ----- Data Model
# **************************************************


# **************************************************
# ----- Main
# **************************************************
def main():
	datastore.connect()

	sentences = []

	# :TODO 書籍と異なる方法で記載. 後ほど変更する
	# **** ここから ****
	for doc_id, in datastore.get_all_ids(limit=20):
		for sentence in datastore.get_annotation(doc_id, "sentence"):
			tokens = find_xs_in_y(
				datastore.get_annotation(doc_id, "token"),
				sentence
			)

			sentences.append((doc_id, sentence, tokens))
	# **** ここまで ****

	rule = ruleclassifier.get_rule()

	# 分類
	feature = ruleclassifier.convert_into_feature_using_rules(sentences, rule)

	predict = ruleclassifier.classify(feature, rule)

	for predicted, (doc_id, sentence, tokens) in zip(predict, sentences):
		if predicted == 1:
			text = datastore.get(doc_id, ["content"])["content"]

			print(predicted, text[sentence["begin"]: sentence["end"]])

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
