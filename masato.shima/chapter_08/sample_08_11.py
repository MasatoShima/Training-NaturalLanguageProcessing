"""
Name: sample_08_11.py
Description: wordnet を用いて, 単語の上位語・下位語を取得する
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
	text = "幸福"

	results = wordnetknowledge.get_hypernym(text)
	print("**** 上位語 ****")
	print(json.dumps(results, ensure_ascii=False, indent=4))

	results = wordnetknowledge.get_hyponym(text)
	print("**** 下位語 ****")
	print(json.dumps(results, ensure_ascii=False, indent=4))

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
