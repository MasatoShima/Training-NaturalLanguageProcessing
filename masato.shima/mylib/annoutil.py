"""
Name: annoutil
Description: 
Created by: Masato Shima
Created on: 2019/09/11
"""

# **************************************************
# ----- Import Library
# **************************************************
from typing import *


# **************************************************
# ----- Function find_xs_in_y
# **************************************************
def find_xs_in_y(
		xs: List[Dict[str, Any]],
		y: Dict[str, Any]
) -> List[Dict[str, Any]]:
	"""
	token （単語の一覧）と sentence （文）を引数で受け取る
	token のうち, sentence に含まれているもののみを抽出し, それらを戻り値として返す
	:param xs: token の一覧が格納されている（単語と, その単語の出現位置などが格納されている）
	:param y: sentence が格納されている（文と, その文の出現位置などが格納されている）
	:return: sentence に含まれている token の一覧
	"""
	response = [
		x for x in xs
		if y["begin"] <= x["begin"]
		and x["end"] <= y["end"]
	]

	return response


# **************************************************
# ----- End
# **************************************************
