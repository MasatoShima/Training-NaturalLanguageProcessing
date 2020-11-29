"""
Name: sample_05_01
Description:
Created by: Masato Shima
Created on: 2019/07/24
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import re

from mylib import sqlitedatastore as datastore


# **************************************************
# ----- Main Function
# **************************************************
def main():
	# 抽出する際に, 指定する正規表現のパターンを作成
	pattern = [
		r".+?大学",
		r".+?学会",
		r".+?協会",
	]

	pattern = re.compile(r"|".join(pattern))

	annotation_name = "affiliation"

	# SQLite に接続
	client = datastore.connect()

	# アノテーションを格納するための column を作成（該当するテーブルがない場合のみ, 作成）
	columns = [i[1] for i in client.execute(f"PRAGMA table_info(docs)")]

	if annotation_name not in columns:
		client.execute(
			f"ALTER TABLE docs ADD COLUMN '{annotation_name}' 'BLOB'"
		)

		client.commit()

		print(f"Create new column: {annotation_name}")

	else:
		print(f"Already exist table column: {annotation_name}")

	# SQLite より 1レコードずつ取得し, アノテーションを付与
	# その後, それらを SQLite に格納する
	for doc_id in datastore.get_all_ids(limit=-1):
		annotations = create_annotation(doc_id, pattern)

		datastore.put_annotation(doc_id, annotation_name, annotations)

	datastore.close()

	return


# **************************************************
# ----- Function create_annotation
# **************************************************
def create_annotation(doc_id, pattern):
	# doc_id に対応する 1レコードを取得
	row = datastore.get(doc_id=doc_id, fl=["content"])
	text = row["content"]

	# 付与したアノテーションを格納する list
	annotations = []

	# 1文節ごと（ == chunk ）ごとに正規表現を用いて, 該当する単語を抽出
	# 該当するものがあれば, それをアノテーションとして, 付与する
	for chunk in datastore.get_annotation(doc_id, "chunk"):
		chunk_str = text[chunk["begin"]: chunk["end"]]

		m = pattern.search(chunk_str)

		if not m:
			continue

		annotation = {
			"begin": chunk["begin"] + m.start(),
			"end": chunk["end"] + m.end()
		}

		print(text[annotation["begin"]: annotation["end"]])

		annotations.append(annotation)

	return annotations


# **************************************************
# ----- Main Process
# **************************************************
if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	main()


# **************************************************
# ----- End
# **************************************************
