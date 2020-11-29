"""
Name: sample_12_02.py
Description: 係り受け構造の解析結果を用いて, 関係抽出を行う
Created by: Masato Shima
Created on: 2019/11/20
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
from typing import *

from mylib import sqlitedatastore as datastore
from mylib.annoutil import find_xs_in_y


# **************************************************
# ----- Main
# **************************************************
def main():
	client = datastore.connect()

	# アノテーションを格納するための column を作成（該当するテーブルがない場合のみ, 作成）
	columns = [i[1] for i in client.execute(f"PRAGMA table_info(docs)")]

	new_columns = [
		"cause",
		"effect"
	]

	for new_column in new_columns:
		if new_column not in columns:
			client.execute(
				f"ALTER TABLE docs ADD COLUMN '{new_column}' 'BLOB'"
			)

			client.commit()

			print(f"Create new column: {new_column}")

		else:
			print(f"Already exist table column: {new_column}")

	# - SQLite より全ての doc_id を取得
	# - doc_id に対応する文書を取得
	# - 正規表現を用いて, 関係性を抽出
	for doc_id in datastore.get_all_ids(limit=-1):
		text = datastore.get(doc_id, fl=["content"])["content"]

		annotations = {}

		for sentence, relation in extract_relation(doc_id):
			print(f"文書	{doc_id}	{text[sentence['begin']: sentence['end']]}")

			for annotation_name, annotation in relation.items():
				print(f"{annotation_name}	{text[annotation['begin']: annotation['end']]}\n")

				annotations.setdefault(annotation_name, []).append(annotation)

		for annotation_name, annotation in annotations.items():
			datastore.put_annotation(doc_id, annotation_name, annotation)

	datastore.close()

	return


# **************************************************
# ----- Function extract_relation
# **************************************************
def extract_relation(doc_id: str):
	# 文章, 文, 文節, 単語を取得
	text = datastore.get(doc_id, fl=["content"])["content"]

	all_chunks = datastore.get_annotation(doc_id, "chunk")
	all_tokens = datastore.get_annotation(doc_id, "token")

	annotation_id = 0

	# 1文ずつ loop で処理を行う
	for sentence in datastore.get_annotation(doc_id, "sentence"):
		# 文中に出現する文節, 単語を取得
		chunks = find_xs_in_y(all_chunks, sentence)
		tokens = find_xs_in_y(all_tokens, sentence)

		# 1文節ずつ loop で処理を行う
		for chunk in chunks:
			# 文節中に出現する単語を取得
			chunk_tokens = find_xs_in_y(tokens, chunk)

			# 単語の原型が動詞の「与える」であるものを取得
			# 該当するものがない場合は, 次の文節の処理へ
			check = [
				chunk_token["lemma"] == "与える"
				for chunk_token in chunk_tokens
			]

			if not any(check):
				continue

			# 「与える」の文節を「影響を」の文節が修飾しているか否かを探索する
			# 該当するものがない場合は, 次の文節の処理へ
			affect, affect_token = find_child(
				parent=chunk,
				chunks_in_sentence=chunks,
				tokens_in_sentence=tokens,
				text=text,
				all_chunks=all_chunks,
				child_cond={"text": ["影響を"]}
			)

			if affect is None:
				continue

			# 影響元を取得
			# 該当するものがない場合は, 次の文節の処理へ
			cause, cause_token = find_child(
				parent=chunk,
				chunks_in_sentence=chunks,
				tokens_in_sentence=tokens,
				text=text,
				all_chunks=all_chunks,
				child_cond={
					"pos1": ["助詞"],
					"lemma1": ["は", "も", "が"],
					"pos2_ng": ["助詞"]
				}
			)

			if cause is None:
				continue

			# 影響先を取得
			# 該当するものがない場合は, 次の文節の処理へ
			effect, effect_token = find_child(
				parent=chunk,
				chunks_in_sentence=chunks,
				tokens_in_sentence=tokens,
				text=text,
				all_chunks=all_chunks,
				child_cond={
					"pos1": ["助詞"],
					"lemma1": ["に"],
					"pos2_ng": ["助詞"]
				}
			)

			if effect is None:
				continue

			# 影響元, 影響先を relation 変数に格納
			# 該当する文とともに yield で呼び出し元に値を返す
			relation = {
				"cause": {
					"begin": cause["begin"],
					"end": cause["end"],
					"link": ("effect", annotation_id)
				},
				"effect": {
					"begin": effect["begin"],
					"end": effect["end"]
				}
			}

			annotation_id += 1

			yield sentence, relation

	return


# **************************************************
# ----- Function find_child
# **************************************************
def find_child(
		parent,
		chunks_in_sentence,
		tokens_in_sentence,
		text,
		all_chunks,
		child_cond
) -> Tuple:
	for child in chunks_in_sentence:
		_, link = child["link"]

		if (link == -1 or
			all_chunks[link] != parent):
			continue

		child_tokens = find_xs_in_y(tokens_in_sentence, child)

		if text[child["begin"]: child["end"]] in child_cond.get("text", []):
			return child, child_tokens

		if (child_tokens[-1]["POS"] in child_cond.get("pos1", []) and
			child_tokens[-1]["lemma"] in child_cond.get("lemma1", []) and
			child_tokens[-2]["POS"] not in child_cond.get("pos2_ng", [])):
			return child, child_tokens

	return None, None


# **************************************************
# ----- Main Process
# **************************************************
if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	main()


# **************************************************
# ----- End
# **************************************************
