"""
Name: sample_07_07
Description: 言語モデルを作成し, 「日本語らしさ」を推定する
Created by: Masato Shima
Created on: 2019/11/24
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import random

from mylib import cabochaparser as parser
from mylib import sqlitedatastore as datastore
from mylib import statistics


# **************************************************
# ----- Function main
# **************************************************
def main():
	# SQLite に接続
	datastore.connect()

	# 言語モデルを作成
	lm = statistics.create_language_model(
		datastore.get_all_ids(limit=-1),
		n=3
	)

	text = "古くから人が居住する。"

	sentences, chunks, tokens = parser.parse(text)

	probabilities = set([])

	for i in range(1000):
		tokens_ = tokens[1:]

		random.shuffle(tokens_)

		tokens_shuffle = [tokens[0]] + tokens_

		lemmas = ["__BOS__"] + [token["lemma"] for token in tokens_shuffle] + ["__EOS__"]

		shuffled_text = "".join(
			[
				text[token["begin"]: token["end"]]
				for token in tokens_shuffle
			]
		)

		probability = statistics.calc_prob(lm, lemmas, n=3)
		probabilities.add((probability, shuffled_text))

	for probability, shuffled_text in sorted(list(probabilities), reverse=True)[:20]:
		print(f"{probability}: {shuffled_text}")

	datastore.close()

	return


# **************************************************
# ----- Main
# **************************************************
if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	main()


# **************************************************
# ----- End
# **************************************************
