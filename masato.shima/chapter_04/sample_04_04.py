"""
Name: sample_04_04.py
Description: sample script from chapter 4
Created by: Masato Shima
Created on: 2019/07/24
"""

# **************************************************
# ----- Import Library
# **************************************************
import os

from mylib import cabochaparser as parser
from mylib import sqlitedatastore as datastore


# **************************************************
# ----- Main Function
# **************************************************
def main():
	datastore.connect()

	print("Success connecting 'sample.db'")

	# SQLite より id の一覧を取得
	# 1つずつ処理を進める
	for doc_id in datastore.get_all_ids(limit=-1):
		# SQLite より文章を取得
		row = datastore.get(doc_id=doc_id, fl=["content"])
		text = row["content"]

		# 取得した文章を CaboCha で係り受け構造の解析を行い,
		# 文, 文節, 単語に分割されたデータを取得
		sentences, chunks, tokens = parser.parse(text)

		print(f"parsed: doc_id={doc_id}")

		# SQLite に解析結果を保存
		datastore.put_annotation(doc_id, "sentence", sentences)
		datastore.put_annotation(doc_id, "chunk", chunks)
		datastore.put_annotation(doc_id, "token", tokens)

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
