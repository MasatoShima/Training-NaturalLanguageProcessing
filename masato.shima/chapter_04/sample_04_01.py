"""
Name: sample_04_01.py
Description: sample script from chapter 4
Created by: Masato Shima
Created on: 2019/11/04
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import CaboCha

cabocha = CaboCha.Parser("-n1")


# **************************************************
# ----- Main Function
# **************************************************
def main(sentence_str):
	# CaboCha を用いて, 係り受け構造を解析
	tree = cabocha.parse(sentence_str)

	text = sentence_str

	# chunk ( == 文節 ) を 1つずつ取得し, 処理を進める
	sentence_begin = 0

	for i in range(tree.chunk_size()):
		chunk = tree.chunk(i)
		chunk_begin = None

		print("chunk:")

		# token ( == 単語 ) を 1つずつ取得し, 処理を進める
		token_end = 0

		for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
			token = tree.token(j)

			# token.feature の中に抽出した単語の原形, 品詞, 固有表現の有無などの情報が
			# カンマ区切りの文字列で格納されている
			features = token.feature.split(",")

			# 単語の出現位置を決定
			token_begin = text.find(token.surface) + sentence_begin
			token_end = token_begin + len(token.surface)

			if chunk_begin is None:
				chunk_begin = token_begin

			print(f"    token_begin: {token_begin}")
			print(f"    token_end  : {token_end}")
			print(f"    features   : {features}")
			print(f"    lemma      : {features[-3]}")
			print(f"    POS        : {features[0]}")
			print(f"    POS2       : {features[1]}")
			print(f"    NE         : {token.ne}")
			print(f"")

			# 処理済みの chunk を text から削除
			text = text[token_end - sentence_begin:]

			sentence_begin = token_end

		chunk_end = token_end

		print(f"    chunk_link : {chunk.link}")
		print(f"    chunk_begin: {chunk_begin}")
		print(f"    chunk_end  : {chunk_end}")
		print(f"")

	return


# **************************************************
# ----- Main Process
# **************************************************
if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	sample = (
		"Amazon 社内のビジネス課題を解決するために生まれた IT インフラストラクチャのノウハウをもとに、"
		"2006 年、アマゾン ウェブ サービス（AWS）はウェブサービスという形態で、"
		"企業を対象に IT インフラストラクチャサービスの提供を開始しました。"
	)

	main(sample)


# **************************************************
# ----- End
# **************************************************
