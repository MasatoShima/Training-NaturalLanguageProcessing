"""
Name: sample_12_01.py
Description: 正規表現を用いて, 関係抽出を行う
Created by: Masato Shima
Created on: 2019/11/20
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import re
from typing import *

from mylib import sqlitedatastore as datastore


# **************************************************
# ----- Constants & Variables
# **************************************************
pattern = re.compile(
	r"(?P<cause>[^、はもがに]+[はもが])(?P<effect>[^はもが]+に)影響を与え"
)


# **************************************************
# ----- Main
# **************************************************
def main() -> None:
	datastore.connect()

	# - SQLite より全ての doc_id を取得
	# - doc_id に対応する文書を取得
	# - 正規表現を用いて, 関係性を抽出
	for doc_id in datastore.get_all_ids(limit=-1):
		text = datastore.get(doc_id, fl=["content"])["content"]

		for sentence, relation in extract_relation(doc_id):
			print(f"文書: {doc_id}	{text[sentence['begin']: sentence['end']]}")

			for annotation_name, annotation in relation.items():
				print(f"{annotation_name}	{text[annotation['begin']: annotation['end']]}")

			print("\n ******** \n")

	datastore.close()

	return


# **************************************************
# ----- Function extract_relation
# **************************************************
def extract_relation(doc_id: str) -> Tuple[str, Dict[str, Any]]:
	# doc_id から該当する文書を取得
	text = datastore.get(doc_id, fl=["content"])["content"]

	annotation_id = 0

	# 文を 1つずつ取得し, 正規表現に合致する箇所を抽出する
	# 抽出したものは relation に格納
	for sentence in datastore.get_annotation(doc_id, "sentence"):
		for m in pattern.finditer(text[sentence["begin"]: sentence["end"]]):
			relation = {
				"cause": {
					"begin": m.start("cause") + sentence["begin"],
					"end": m.end("cause") + sentence["begin"],
					"link": ("effect", annotation_id)
				},
				"effect": {
					"begin": m.start("effect") + sentence["begin"],
					"end": m.end("effect") + sentence["begin"],
				}
			}

			annotation_id += 1

			yield sentence, relation

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
