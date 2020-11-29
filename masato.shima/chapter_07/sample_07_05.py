"""
Name: sample_07_05
Description: 言語モデルを作成し, 出現する単語を予測する
Created by: Masato Shima
Created on: 2019/11/24
"""

# **************************************************
# ----- Import Library
# **************************************************
import os

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

	context = ("古く", "から")
	print(f"{context} =>")

	# 言語モデルを作成し, context の次に出現する単語の一覧と, そのスコアを取得
	prob_list = [
		(word, lm.score(word, context))
		for word in lm.context_counts(lm.vocab.lookup(context))
	]

	# 単語の一覧をスコアが高い順番に sort
	prob_list.sort(key=lambda x: x[1], reverse=True)

	# 単語の一覧を出力
	for word, prob in prob_list:
		print(f"{word.ljust(8)}: {prob}")

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
