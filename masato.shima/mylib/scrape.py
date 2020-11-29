"""
Name: scrape
Description:　crawling from web page and scraping text
Created by: Masato Shima
Created on: 2019/07/03
"""

# **************************************************
# ----- Import Library
# **************************************************
import re
import unicodedata
from bs4 import BeautifulSoup


# **************************************************
# ----- Function scrape
# **************************************************
def scrape(html):
	data_parsed = BeautifulSoup(html, "html.parser")

	# HP 内の特定の要素名に対応する値を取得
	for block in data_parsed.find_all(["p", "h1", "h2", "h3", "h4"]):
		if (len(block.text.strip()) > 0
			and block.text.strip()[-1] not in ["。", "！"]):
			block.append("<__EOS__>")

	# 本文の抽出
	text = "\n".join(
		[
			cleanse(block.text.strip())
			for block in data_parsed.find_all(["p", "h1", "h2", "h3", "h4"])
			if len(block.text.strip()) > 0
		]
	)

	# タイトルの抽出
	title = cleanse(data_parsed.title.text.replace(" - Wikipedia", ""))

	return text, title


# **************************************************
# ----- Function cleanse
# **************************************************
def cleanse(text):
	translation_table = str.maketrans(dict(zip("()!", "（）！")))

	text = unicodedata.normalize("NFKC", text)
	text = text.translate(translation_table)
	text = re.sub(r"\s+", " ", text)

	return text


# **************************************************
# ----- End
# **************************************************
