"""
Name: sample_08_09.py
Description: wordnet を用いて, 単語同士の類似度を取得する
Created by: Masato Shima
Created on: 2020/01/12
"""

# **************************************************
# ----- Import Library
# **************************************************
import os

from mylib import wordnetknowledge


# **************************************************
# ----- Function main
# **************************************************
def main():
	text1 = "アメリカ合衆国"
	text2 = "米国"

	similarity = wordnetknowledge.calc_similarity(text1, text2)

	print(text1, text2, similarity)

	text1 = "アメリカ合衆国"
	text2 = "日本"

	similarity = wordnetknowledge.calc_similarity(text1, text2)

	print(text1, text2, similarity)

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
