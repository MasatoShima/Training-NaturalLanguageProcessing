"""
Name: sample_08_04.py
Description: DBpedia より取得した文章について, 類似度を算出する
Created by: Masato Shima
Created on: 2020/01/05
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
from mylib import dbpediaknowledge


# **************************************************
# ----- Function Main
# **************************************************
def main() -> None:
	text1 = "アメリカ合衆国"
	text2 = "イギリス"

	similarity = dbpediaknowledge.calc_similarity(text1, text2)
	print(similarity, text1, text2)

	text1 = "アメリカ合衆国"
	text2 = "日本"

	similarity = dbpediaknowledge.calc_similarity(text1, text2)
	print(similarity, text1, text2)

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
