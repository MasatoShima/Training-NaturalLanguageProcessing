"""
Name: sample_02_04
Description: sample script from chapter 2
Created by: Masato Shima
Created on: 2019/07/03
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import re
import unicodedata


# **************************************************
# ----- Main Function
# **************************************************
def main():
	text = "    C　L　E　A　N　S　ing  によりﾃｷｽﾄﾃﾞｰﾀを変換すると　トラブルが少なくなります。　"
	print(f"Before: {text}")

	translation_table = str.maketrans(dict(zip("()!", "（）！")))

	# 半角全角で不統一となっている文字列を正規化
	text = unicodedata.normalize("NFKC", text)

	# translation_table にもとづき, 全角にしたい文字列を半角から変換
	text = text.translate(translation_table)

	# 2連続以上のスペースは 1つのスペースに変換
	text = re.sub(r"\s+", " ", text)

	print(f"After : {text}")

	return


# **************************************************
# ----- Main Process
# **************************************************
if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	main()

# **************************************************
# ----- End
# **************************************************
