"""
Name: sample_08_08.py
Description: wordnet を用いて, 単語に対する類似語を取得する
Created by: Masato Shima
Created on: 2020/01/12
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import json

from mylib import wordnetknowledge


# **************************************************
# ----- Function main
# **************************************************
def main():
	synonyms = wordnetknowledge.get_synonyms("アメリカ合衆国")

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
