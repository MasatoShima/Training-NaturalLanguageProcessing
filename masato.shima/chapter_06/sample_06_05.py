"""
Name: sample_06_05
Description:
Created by: Masato Shima
Created on: 2019/08/28
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import json
import bottle


# **************************************************
# ----- Variables
# **************************************************


# **************************************************
# ----- Function index_html
# **************************************************
@bottle.route("/")
def index_html():
	response = bottle.static_file("sample_06_06.html", root="./src/static/")

	return response


# **************************************************
# ----- Function static
# **************************************************
@bottle.route("/file/<filename:path>")
def static(filename):
	response = bottle.static_file(filename, root="./src/static/")

	return response


# **************************************************
# ----- Function get
# **************************************************
@bottle.get("/get")
def get():
	data = {
		"collection": {
			"entity_types": [
				{
					"type": "Person",
					"bgColor": "#7fa2ff",
					"borderColor": "darken"
				}
			]
		},
		"annotation": {
			"text": "Ed 0'Kelly was the man who shot the man who shot Jesse James",
			"entities": [
				[
					"T1",
					"Person",
					[[0, 11]]
				],
				[
					"T2",
					"Person",
					[[20, 23]]
				],
				[
					"T3",
					"Person",
					[[37, 40]]
				],
				[
					"T4",
					"Person",
					[[50, 61]]
				]
			]
		}
	}

	return json.dumps(data, ensure_ascii=False, indent=4)


# **************************************************
# ----- Main Process
# **************************************************
if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	bottle.run(host="localhost", port="8702")


# **************************************************
# ----- End
# **************************************************
