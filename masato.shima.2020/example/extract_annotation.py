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

	rules = h.compile(name="template1", rules=["data/rules.lisp"], dicts=[])

	sample_text = ["私は上司に書類を提出した"]

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
