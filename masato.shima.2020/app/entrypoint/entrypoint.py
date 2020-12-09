"""
Name: entrypoint.py
Created by: Masato Shima
Created on: 2020/12/09
Description:
"""

# **************************************************
# ----- Import Library
# **************************************************
import hsde


# **************************************************
# ----- Constants & Variables
# **************************************************
DIR_CONFIG = "config/"


# **************************************************
# ----- Function main
# **************************************************
def main(text: str):
	h = hsde.Hsde()

	rules = h.compile(name="template1", rules=[f"{DIR_CONFIG}rules.lisp"], dicts=[])

	rules_parsed = h.parse_sentences([text])

	matches = h.match(rules_parsed, [rules])

	results = h.extract_annotation(matches, ["text"])

	print(results)

	return


# **************************************************
# ----- Process Main
# **************************************************
if __name__ == "__main__":
	sample = (
		"主な事業領域ごとの特性として、"
		"プラント・自動車・建設機械等の機械関連取引、金属資源・エネルギー・化学品等のトレード並びに"
		"開発投資については世界経済の動向に大きく影響を受ける一方、"
		"繊維・食料等の生活消費分野は相対的に国内景気の影響を受けやすいと言えます。"
	)

	main(sample)


# **************************************************
# ----- End
# **************************************************
