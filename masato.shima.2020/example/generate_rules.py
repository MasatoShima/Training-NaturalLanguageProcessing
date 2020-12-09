"""
Name: generate_rules.py
Created by: Masato Shima
Created on: 2020/11/11
Description: Generate rules.
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

	with open(f"data/sample.txt", "r", encoding="utf-8") as file:
		contents = file.readlines()
		contents = [content.strip() for content in contents]

	rules = h.generate_rule_pattern(contents)

	print(rules)

	with open(f"data/rules.lisp", "w", encoding="utf-8") as file:
		file.write(rules)

	return


# **************************************************
# ----- Process Main
# **************************************************
if __name__ == "__main__":
	main()


# **************************************************
# ----- End
# **************************************************
