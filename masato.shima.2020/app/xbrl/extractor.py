"""
Name: extractor.py
Created by: Masato Shima
Created on: 2020/11/28
Description:
"""

# **************************************************
# ----- Import Library
# **************************************************
import io
import json
import os
import re
from collections import defaultdict
from typing import Dict, List, Union

import lxml.etree


# **************************************************
# ----- Constants & variables
# **************************************************
DIR_DATA = "../../data/"

NUMBERS = [
	"①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩",
	"⑪", "⑫", "⑬", "⑭", "⑮", "⑯", "⑰", "⑱", "⑲", "⑳",
	"㉑", "㉒", "㉓", "㉔", "㉕", "㉖", "㉗", "㉘", "㉙", "㉚",
	"㉛", "㉜", "㉝", "㉞", "㉟", "㊱", "㊲", "㊳", "㊴", "㊵",
	"㊶", "㊷", "㊸", "㊹", "㊺", "㊻", "㊼", "㊽", "㊾", "㊿"
]


# **************************************************
# ----- Function main
# **************************************************
def main():

	samples = [
		(
			f"{DIR_DATA}8001/"
			f"有価証券報告書－第96期(平成31年4月1日－令和2年3月31日)/S100ITS8/XBRL/PublicDoc/"
			f"0102010_honbun_jpcrp030000-asr-001_E02497-000_2020-03-31_01_2020-06-19_ixbrl.htm"
		)
	]

	for sample in samples:
		xbrl = load_lxml(sample)

		contents = extract_sentences(xbrl)

		print(json.dumps(contents, ensure_ascii=False, indent=4))

	return


# **************************************************
# ----- Function load_lxml
# **************************************************
def load_lxml(path: str) -> io.BytesIO:
	with open(path, "rb") as file:
		xbrl = file.read()
		xbrl = io.BytesIO(xbrl)

	return xbrl


# **************************************************
# ----- Function extract_sentences
# **************************************************
def extract_sentences(
		xbrl: io.BytesIO
) -> Dict[str, Union[List[str], Dict[str, List[str]]]]:
	# xbrl を parse
	tree = lxml.etree.parse(xbrl)

	# xbrl の名前空間を取得
	namespaces = {
		str(key): str(value) for key, value in tree.getroot().nsmap.items()
	}

	# xpath にもとづき, 要素を取得
	# 要素の取得とともに, 文書構成の解析も行う
	matches = tree.xpath(
		"//ix:nonNumeric[@name='jpcrp_cor:BusinessRisksTextBlock']/*",
		namespaces=namespaces
	)

	contents = defaultdict(list)

	title = None

	for match in matches:
		content = lxml.etree.tostring(match, method="text", encoding="utf-8").decode()
		content = content.strip()

		if re.match(r"^（.+）.*", content):
			title = content
			contents[title] = []
		elif content:
			contents[title].append(content)

	# xbrl より取得した要素の含まれる文書の構成が nest したものとなっている場合,
	# それらの解析も行う
	pattern = "|".join(NUMBERS)

	for title, content in contents.items():
		check = [re.match(fr"^({pattern})", c) for c in content]

		if any(check):
			title_sub = None

			# :TODO type check による warning を解決すること
			contents[title] = {title_sub: []}

			for c in content:
				if re.match(fr"^({pattern})", c):
					title_sub = c
					contents[title][title_sub] = []
				else:
					contents[title][title_sub].append(c)

	return contents


# **************************************************
# ----- Main
# **************************************************
if __name__ == "__main__":
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	main()


# **************************************************
# ----- End
# **************************************************
