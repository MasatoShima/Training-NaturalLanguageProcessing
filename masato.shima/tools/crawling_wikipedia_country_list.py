"""
Name: Masato Shima
Description: 
Created by: Masato Shima
Created on: 2019/11/24
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import requests
import lxml.html


# **************************************************
# ----- Constants & Variables
# **************************************************
URL = "https://ja.wikipedia.org/wiki/国の一覧"
DIR_OUTPUT = "./"


# **************************************************
# ----- Main
# **************************************************
def main():
	# Wikipedia に記載されている「国の一覧」ページから各国のページへの URL を取得
	text = requests.get(URL).text
	text_parsed = lxml.html.fromstring(text)

	elements = text_parsed.xpath("//*[@id=\"mw-content-text\"]/div/table[2]/tbody/tr/td[1]/b[2]/a")

	for element in elements:
		# URL を取得
		url_country = element.attrib["href"]

		# 各国のページを読み込み
		text_country = requests.get(f"https://ja.wikipedia.org/{url_country}").text
		text_country_parsed = lxml.html.fromstring(text_country)

		# ページの title を取得
		# 各国のページを html ファイルとして, 保存する際のファイル名に使用する
		title = text_country_parsed.xpath("//title")[0].text

		# 読み込んだ各国のページをファイルに保存
		with open(f"{DIR_OUTPUT}{title}.html", "w") as file:
			file.write(text_country)

		print(f"Saved page: {title}")

	return


# **************************************************
# ----- Process Main
# **************************************************
if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	main()


# **************************************************
# ----- End
# **************************************************
