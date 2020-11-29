"""
Name: sample_03_07
Description: sample script from chapter 3
Created by: Masato Shima
Created on: 2019/07/17
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import json

from mylib import sqlitedatastore as datastore
from mylib import solrindexer as indexer


# **************************************************
# ----- Main Function
# **************************************************
def main():
	datastore.connect()

	data = []

	for doc_id in datastore.get_all_ids(limit=-1):
		row = datastore.get(doc_id, ["id", "content", "meta_info"])

		# Solr へ登録するデータ構造へ変換
		meta_info = json.loads(row["meta_info"])

		data.append({
			"id": str(row["id"]),
			"doc_id_i": row["id"],
			"content_txt_ja": row["content"],
			"title_txt_ja": meta_info["title"],
			"url_s": meta_info["url"]
		})

	# Solr への登録を実行
	indexer.put("doc", data)

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
