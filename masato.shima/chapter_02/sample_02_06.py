"""
Name: sample_02_06.py
Description: sample script from chapter 2
Created by: Masato Shima
Created on: 2019/07/03
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import cchardet
import urllib.request

from mylib import scrape


# **************************************************
# ----- Main Function
# **************************************************
def main():
	url = "https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC"

	with urllib.request.urlopen(url) as response:
		data_bytes = response.read()
		data_string = data_bytes.decode(cchardet.detect(data_bytes)["encoding"])

		text, title = scrape.scrape(data_string)

		print(f"[title]: {title}")
		print(f"[text]: {text[:1000]}")

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
