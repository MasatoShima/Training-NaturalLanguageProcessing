"""
Name: extract_annotation.py
Created by: Masato Shima
Created on: 2020/11/11
Description: Extract annotation.
"""

# **************************************************
# ----- Import Library
# **************************************************
import hsde


# **************************************************
# ----- Function main
# **************************************************
def main():
	h = hsde.Hsde()

	# For example
	# rules = h.compile(name="template1", rules=["data/rules.lisp"], dicts=[])

	# For debug
	rules = h.compile(name="template1", rules=["./../app/config/rules.lisp"], dicts=[])

	sample_text = [
		"主な事業領域ごとの特性として、"
		"プラント・自動車・建設機械等の機械関連取引、金属資源・エネルギー・化学品等のトレード並びに"
		"開発投資については世界経済の動向に大きく影響を受ける一方、"
		"繊維・食料等の生活消費分野は相対的に国内景気の影響を受けやすいと言えます。"
	]

	rules_parsed = h.parse_sentences(sample_text)

	matches = h.match(rules_parsed, [rules])

	results = h.extract_annotation(matches, ["text"])
	print(results)

	return


# **************************************************
# ----- Process Main
# **************************************************
if __name__ == "__main__":
	main()


# **************************************************
# ----- End
# **************************************************
