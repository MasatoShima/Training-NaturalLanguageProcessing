"""
Name: cabochaparser
Description: text split to sentences and parse at "CaboCha"
Created by: Masato Shima
Created on: 2019/07/17
"""

# **************************************************
# ----- Import Library
# **************************************************
import re
import CaboCha


# **************************************************
# ----- Constants & Variables
# **************************************************
ptn_sentence = re.compile(
	r"(^|。|！|<__EOS__>)\s*(.+?)(?=(。|！|<__EOS__>))",
	re.M
)


# **************************************************
# ----- Function parse
# **************************************************
def parse(text):
	sentences = []
	chunks = []
	tokens = []

	sentence_begin = 0

	for sentence_str, sentence_begin in split_into_sentences(text):
		parse_sentences(sentence_str, sentence_begin, chunks, tokens)

		sentence_end = chunks[-1]["end"]

		sentences.append(
			{
				"begin": sentence_begin,
				"end": sentence_end
			}
		)

	return sentences, chunks, tokens


# **************************************************
# ----- Function split_into_sentences
# **************************************************
def split_into_sentences(text):
	# 正規表現のパターンにもとづき, text を文単位に分割し, list に格納
	sentences = []

	for m in ptn_sentence.finditer(text):
		sentences.append((m.group(2), m.start(2)))

	return sentences


# **************************************************
# ----- Function parse_sentences
# **************************************************
def parse_sentences(sentence_str, sentence_begin, chunks, tokens):
	# 引数で渡された文の係り受け構造を CaboCha で解析し,
	# 抽出した文節 ( == chunk ), 単語 ( == token )を
	# 引数で渡された chunks, tokens にそれぞれ格納する
	cabocha = CaboCha.Parser("-n1")

	tree = cabocha.parse(sentence_str)

	offset = sentence_begin

	chunk_id_offset = len(chunks)

	text = sentence_str

	# chunk ( == 文節 ) を 1つずつ取得し, 処理を進める
	for i in range(tree.chunk_size()):
		chunk = tree.chunk(i)

		chunk_begin = None

		token_end = None

		# token ( == 単語 ) を 1つずつ取得し, 処理を進める
		for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
			token = tree.token(j)

			# token.feature の中に抽出した単語の原形, 品詞, 固有表現の有無などの情報が
			# カンマ区切りの文字列で格納されている
			features = token.feature.split(",")

			# 単語の出現位置を決定
			token_begin = text.find(token.surface) + offset
			token_end = token_begin + len(token.surface)

			if chunk_begin is None:
				chunk_begin = token_begin

			tokens.append(
				{
					"begin": token_begin,
					"end": token_end,
					"lemma": features[-3],
					"POS": features[0],
					"POS2": features[1],
					"NE": token.ne
				}
			)

			text = text[token_end - offset:]

			offset = token_end

		chunk_end = token_end

		# chunk ID を手前に出現した chunk ID の数だけずらす
		if chunk.link == -1:
			link = -1
		else:
			link = chunk.link + chunk_id_offset

		chunks.append(
			{
				"begin": chunk_begin,
				"end": chunk_end,
				"link": ("chunk", link)
			}
		)

	return


# **************************************************
# ----- End
# **************************************************
