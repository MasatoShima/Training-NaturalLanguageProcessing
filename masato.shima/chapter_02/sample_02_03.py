"""
Name: sample_02_03
Description: sample script from chapter 2
Created by: Masato Shima
Created on: 2019/06/19
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import urllib.request
import cchardet
from bs4 import BeautifulSoup


# **************************************************
# ----- Config
# **************************************************
url = "https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC"


# **************************************************
# ----- Main Function
# **************************************************
def main():
	with urllib.request.urlopen(url) as response:
		data_bytes = response.read()
		data_string = data_bytes.decode(cchardet.detect(data_bytes)["encoding"])
		data_parsed = BeautifulSoup(data_string, "html.parser")

	# HP の title を取得
	title = data_parsed.head.title
	print("[title]: ", title.text, "\n")

	# HP 内の特定の要素名に対応する値を取得
	for block in data_parsed.find_all(["p", "h1", "h2", "h3", "h4"]):
		print("[block]: ", block.text.strip())

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
