"""
Name: sample_08_06.py
Description: DBpedia より人口に関するデータを取得する
Created by: Masato Shima
Created on: 2020/01/12
"""

# **************************************************
# ----- Import Library
# **************************************************
import os

from mylib import dbpediaknowledge


# **************************************************
# ----- Function Main
# **************************************************
def main():
	text = "アメリカ合衆国"

	population = dbpediaknowledge.get_population(text)

	print(population)

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
