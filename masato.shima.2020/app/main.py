"""
Name: main.py
Created by: Masato Shima
Created on: 2020/12/09
Description:
"""

# **************************************************
# ----- Import Library
# **************************************************
import json

import text as text_tmp
import xbrl as xbrl_tmp

# from app.text import extractor
# from app.xbrl import parser


# **************************************************
# ----- Constants & Variables
# **************************************************
DIR_DATA = "../data/"


# **************************************************
# ----- Function main
# **************************************************
def main() -> None:
	samples = [
		(
			f"{DIR_DATA}8001/"
			f"有価証券報告書－第96期(平成31年4月1日－令和2年3月31日)/S100ITS8/XBRL/PublicDoc/"
			f"0102010_honbun_jpcrp030000-asr-001_E02497-000_2020-03-31_01_2020-06-19_ixbrl.htm"
		)
	]

	for sample in samples:
		# XBRL データより該当する箇所の文章を抽出
		xbrl = xbrl_tmp.parser.load_lxml(sample)

		contents = xbrl_tmp.parser.extract_sentences(xbrl)

		print(json.dumps(contents, ensure_ascii=False, indent=4))

		# 抽出した文章を参照し, rules にもとづき, 情報を抽出
		for key, item in contents.items():
			if isinstance(item, list):
				for i in item:
					text_tmp.extractor.main(i)
			elif isinstance(item, dict):
				for k, v in item.items():
					for v_ in v:
						text_tmp.extractor.main(v_)

	return


# **************************************************
# ----- Process Main
# **************************************************
if __name__ == "__main__":
	main()


# **************************************************
# ----- End
# **************************************************
