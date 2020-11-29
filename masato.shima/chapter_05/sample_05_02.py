"""
Name: sample_05_02
Description:
Created by: Masato Shima
Created on: 2019/07/24
"""

# **************************************************
# ----- Import Library
# **************************************************
import os

from mylib import sqlitedatastore as datastore


# **************************************************
# ----- Main Function
# **************************************************
def main():
	# SQLite に接続
	datastore.connect()

	annotation_name = "affiliation"

	# 全てのレコードを取得し, 1レコードずつ, 格納されているアノテーションを出力
	for doc_id in datastore.get_all_ids(limit=-1):
		row = datastore.get(doc_id=doc_id, fl=["content"])
		text = row["content"]

		annotations = datastore.get_annotation(doc_id, annotation_name)

		for annotation in annotations:
			print(f"{annotation_name.upper()}: {text[annotation['begin']: annotation['end']]}")

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
