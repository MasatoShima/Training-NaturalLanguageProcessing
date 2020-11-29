"""
Name: solrindexer
Description: client script for "solr"
Created by: Masato Shima
Created on: 2019/07/17
"""

# **************************************************
# ----- Import Library
# **************************************************
import json
import urllib.parse
import urllib.request


# **************************************************
# ----- Config
# **************************************************
solr_url = "http://localhost:8983/solr"

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


# **************************************************
# ----- Function put
# **************************************************
def put(collection, data):
	# データの登録を実行
	request_put = urllib.request.Request(
		url=f"{solr_url}/{collection}/update",
		data=json.dumps(data).encode("utf-8"),
		headers={"content-type": "application/json"}
	)

	with opener.open(request_put) as response:
		print(response.read().decode("utf-8"))

	# Commit
	request_commit = urllib.request.Request(
		url=f"{solr_url}/{collection}/update?softCommit=true"
	)

	with opener.open(request_commit) as response_commit:
		print(response_commit.read().decode("utf-8"))

	return


# **************************************************
# ----- Function search_annotation
# **************************************************
def search_annotation(fl_keyword_pairs, rows=100):
	query = " AND ".join(
		[
			f"({'OR'.join([f'{fl}:{keyword}' for keyword in group])})"
			for fl, keywords in fl_keyword_pairs
			for group in keywords
		]
	)

	data = {
		"q": query,
		"wt": "json",
		"rows": rows
	}

	# 検索リクエストの作成
	request = urllib.request.Request(
		url=f"{solr_url}/anno/select",
		data=urllib.parse.urlencode(data).encode("utf-8")
	)

	# 検索リクエストの実行
	with opener.open(request) as response:
		value = json.loads(response.read().decode("utf-8"))

	return value


# **************************************************
# ----- End
# **************************************************
