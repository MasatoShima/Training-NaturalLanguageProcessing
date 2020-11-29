"""
Name: sample_04_05.py
Description: sample script from chapter 4
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
	datastore.connect()

	# SQLite より id の一覧を取得
	# 1つずつ処理を進める
	for doc_id in datastore.get_all_ids(limit=-1):
		# SQLite より文章を取得
		row = datastore.get(doc_id=doc_id, fl=["content"])
		text = row["content"]

		# token を取得し, それらを出力
		print("token:")

		tokens = datastore.get_annotation(doc_id, "token")

		for token in tokens:
			print(f"    {token['POS']}    {text[token['begin']: token['end']]}")

		# chunk を取得し, それらを出力
		print("chunks:")

		chunks = datastore.get_annotation(doc_id, "chunk")

		for chunk in chunks:
			_, link = chunk["link"]
			print(f"    {text[chunk['begin']: chunk['end']]}")

			if link != -1:
				parent = chunks[link]
				print(f"     --> {text[parent['begin']: parent['end']]}")
			else:
				print(f"     --> {None}")

		print("sentences:")

		sentences = datastore.get_annotation(doc_id, "sentence")

		for sentence in sentences:
			print(f"     --> {text[sentence['begin']: sentence['end']]}")

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
