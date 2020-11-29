"""
Name: sample_08_02.py
Description: DBpedia より同義語の一覧を取得する
Created by: Masato Shima
Created on: 2020/01/05
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import json

from mylib import dbpediaknowledge


# **************************************************
# ----- Function Main
# **************************************************
def main() -> None:
	synonyms = dbpediaknowledge.get_synonyms("アメリカ合衆国")

	print(json.dumps(synonyms, ensure_ascii=False, indent=4))

	return


# **************************************************
# ----- Main
# **************************************************
if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	main()


# **************************************************
# ----- End
# **************************************************
