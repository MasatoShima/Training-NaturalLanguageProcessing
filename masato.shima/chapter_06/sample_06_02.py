"""
Name: sample_06_02
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
	response = bottle.static_file("sample_06_03.html", root="./src/static/")

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
	name = bottle.request.params.namae

	response = json.dumps(
		{
			"greet": f"Hello World {name}"
		},
		ensure_ascii=False
	)

	return response


# **************************************************
# ----- Main Process
# **************************************************
if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	bottle.run(host="localhost", port="8701")


# **************************************************
# ----- End
# **************************************************
