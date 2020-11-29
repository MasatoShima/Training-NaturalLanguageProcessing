"""
Name: sample_06_08
Description: 
Created by: Masato Shima
Created on: 2019/09/11
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import re
import json
import bottle
from typing import *

from mylib import sqlitedatastore as datastore


# **************************************************
# ----- Variables
# **************************************************


# **************************************************
# ----- Data Model
# **************************************************


# **************************************************
# ----- Function index_html
# **************************************************
@bottle.route("/")
def index_html():
	response = bottle.static_file(
		filename="sample_06_09.html",
		root="./src/static/"
	)

	return response


# **************************************************
# ----- Function static
# **************************************************
@bottle.route("/file/<filename:path>")
def static(filename):
	response = bottle.static_file(
		filename=filename,
		root="./src/static/"
	)

	return response


# **************************************************
# ----- Function get
# **************************************************
@bottle.get("/get")
def get():
	doc_id = bottle.request.params.id
	names = bottle.request.params.name.split()

	row = datastore.get(doc_id, fl=["content"])
	text = row["content"]

	data = {
		"collection": {
			"entity_types": []
		},
		"annotation": {
			"text": text,
			"entities": [],
			"relations": []
		}
	}

	mapping = {}

	for name in names:
		annos = datastore.get_annotation(doc_id, name)

		for i, anno in enumerate(annos):
			data["collection"]["entity_types"].append(
				{
					"type": name,
					"bgColor": "#7fa2ff",
					"borderColor": "darken"
				}
			)

			ti = f"T{len(data['annotation']['entities']) + 1}"

			data["annotation"]["entities"].append(
				[
					ti,
					name,
					[[anno["begin"], anno["end"]]]
				]
			)

			mapping[(name, i)] = ti

	return


# **************************************************
# ----- Main Process
# **************************************************
if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	bottle.run(host="localhost", port="8703")


# **************************************************
# ----- End
# **************************************************
