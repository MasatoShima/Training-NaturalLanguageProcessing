"""
Name: ruleclassifier.py
Description: 
Created by: Masato Shima
Created on: 2019/10/09
"""

# **************************************************
# ----- Import Library
# **************************************************
from typing import *


# **************************************************
# ----- Variables
# **************************************************


# **************************************************
# ----- Data Model
# **************************************************


# **************************************************
# ----- Function contain_yumei
# **************************************************
def contain_yumei(tokens):
	for token in tokens:
		if token["lemma"] == "有名":
			return True

	return False


# **************************************************
# ----- Function contain_location
# **************************************************
def contain_location(tokens):
	for token in tokens:
		if token.get("NE", "").endswith("LOCATION"):
			return True

	return False


# **************************************************
# ----- Function contain_oishii
# **************************************************
def contain_oishii(tokens):
	for token in tokens:
		if token["lemma"] == "おいしい":
			return True

	return False


# **************************************************
# ----- Function meibutsu_rule
# **************************************************
def meibutsu_rule(feature):
	if feature["contain_yumei"] and feature["contain_location"]:
		return 1
	if feature["contain_oishii"]:
		return 1

	return


# **************************************************
# ----- Function get_rule
# **************************************************
def get_rule():
	value = {
		"partial": {
			"contain_yumei": contain_yumei,
			"contain_location": contain_location,
			"contain_oishii": contain_oishii
		},
		"compound": meibutsu_rule
	}

	return value


# **************************************************
# ----- Function convert_into_feature_using_rules
# **************************************************
def convert_into_feature_using_rules(sentences, rule):
	features = []

	for doc_id, sent, tokens, in sentences:
		feature = {}

		for name, func in rule["partial"].items():
			feature[name] = func(tokens)

		features.append(feature)

	return features


# **************************************************
# ----- Function classify
# **************************************************
def classify(features, rule):
	value = [
		rule["compound"](feature)
		for feature in features
	]

	return value


# **************************************************
# ----- End
# **************************************************
