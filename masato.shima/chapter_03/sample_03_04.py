"""
Name: sample_03_04
Description: sample script from chapter 3
Created by: Masato Shima
Created on: 2019/07/17
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import glob
import json
import urllib.parse

from mylib import scrape
from mylib import sqlitedatastore as datastore


# **************************************************
# ----- Main Function
# **************************************************
def main():
	datastore.connect()

	values = []

	for file in glob.glob("./../data/html/*.html"):
		with open(file, encoding="utf-8") as f:
			html = f.read()

			text, title = scrape.scrape(html)

			url = f"http://ja.wikipedia.org/wiki/{urllib.parse.quote(title)}"

			value = (
				text,
				json.dumps({"url": url, "title": title}, ensure_ascii=False)
			)

			values.append(value)

			print(f"scrape: {title}")

	datastore.put(values)

	print(list(datastore.get_all_ids(limit=-1)))

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
