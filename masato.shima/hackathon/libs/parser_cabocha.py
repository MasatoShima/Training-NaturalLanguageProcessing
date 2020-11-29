"""
Name: parser_cabocha.py
Description: Cabocha を用いて, 文の係り受け構造を解析する
Created by: Masato Shima
Created on: 2019/12/22
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import re
from typing import *

import CaboCha


# **************************************************
# ----- Constants & Variables
# **************************************************
cabocha = CaboCha.Parser("-n1")

pattern = [
	("（出典）", "FRONT"),
	("（出所）", "FRONT"),
	("（引用）", "FRONT"),
	("出典", "FRONT"),
	("出所", "FRONT"),
	("引用", "FRONT"),
	("より", "BACK"),
	("よると", "BACK"),
	("よれば", "BACK")
]

ignores = [
	"[!\"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]"
]


# **************************************************
# ----- Main Function
# **************************************************
def main(sentence: str) -> str:
	chunks = _parse_sentence(sentence)
	chunks = _extract_chunks(chunks)
	chunks = _ignore_character(chunks)

	return chunks


# **************************************************
# ----- Function parse_sentence
# **************************************************
def _parse_sentence(sentence: str) -> List[Dict[str, Any]]:
	chunks = []

	# CaboCha を用いて, 係り受け構造を解析
	tree = cabocha.parse(sentence)

	text = sentence
	text_stdout = sentence

	# chunk ( == 文節 ) を 1つずつ取得し, 処理を進める
	sentence_begin = 0

	for i in range(tree.chunk_size()):
		# sentence 内の i 番目の chunk を取得
		chunk = tree.chunk(i)

		chunk_begin = None

		token_end = 0

		# token ( == 単語 ) を 1つずつ取得し, 処理を進める
		# token_pos: chunk 内の token の出現位置 （ 出現位置の数え方は sentence 全体で見たときの値 ）
		# token_size: chunk 内における token の数
		for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
			# sentence 内の j 番目の token を取得
			token = tree.token(j)

			# 単語の出現位置 （ 開始 / 終了 の位置 ） を決定
			token_begin = text.find(token.surface) + sentence_begin
			token_end = token_begin + len(token.surface)

			if chunk_begin is None:
				chunk_begin = token_begin

			# 処理済みの chunk を text から削除
			text = text[token_end - sentence_begin:]

			sentence_begin = token_end

		chunk_end = token_end

		chunks.append(
			{
				"chunk": text_stdout[chunk_begin: chunk_end],
				"chunk_link": chunk.link,
				"chunk_begin": chunk_begin,
				"chunk_end": chunk_end
			}
		)

	# For check
	# import json
	# print(json.dumps(chunks, ensure_ascii=False, indent=4))

	return chunks


# **************************************************
# ----- Function extract_chunks
# **************************************************
def _extract_chunks(chunks: List[Dict[str, Any]]):
	# pattern から正規表現にもとづく検索条件を作成
	pattern_reg = [p[0] for p in pattern]
	pattern_reg = fr"({'|'.join(pattern_reg)})"
	ignores_reg = fr"({'|'.join(ignores)})"

	# 正規表現の検索条件に合致する chunk および, その chunk の出現位置を取得
	# 合致する chunk が複数あった場合は, sentence の中で最も後ろに出現したものを取得する
	chunks_extracted = [
		chunk for chunk in chunks
		if re.search(pattern_reg, re.sub(ignores_reg, "", chunk["chunk"]))
	]

	if chunks_extracted:
		chunks_modified = chunks_extracted[-1]["chunk"]
		chunks_position = chunks.index(chunks_extracted[-1])

		# chunks_modified を修飾する chunk を取得し,
		# chunks_modified の先頭に結合していく
		for chunk in reversed(chunks):
			if chunk["chunk_link"] == chunks_position:
				chunks_modified = chunk["chunk"] + chunks_modified

				# chunks_modified を修飾する chunk を修飾する chunk を再帰的に取得し,
				# chunks_modified の先頭に結合していく
				for c in _extract_tree(chunks, chunk):
					chunks_modified = c["chunk"] + chunks_modified
	else:
		chunks_modified = "Not Found"

	return chunks_modified


# **************************************************
# ----- Function extract_tree
# **************************************************
def _extract_tree(chunks: List[Dict[str, Any]], chunk: Dict[str, Any]) -> Generator:
	chunk_position = chunks.index(chunk)

	for c in reversed(chunks):
		if c["chunk_link"] == chunk_position:
			yield c

			c_position = chunks.index(c)

			check = [
				cc for cc in chunks
				if cc["chunk_link"] == c_position
			]

			for ccc in check:
				yield ccc

	return


# **************************************************
# ----- Function ignore_character
# **************************************************
def _ignore_character(chunk: str) -> str:
	for p in pattern:
		match_object = re.search(re.compile(p[0]), chunk)

		if match_object:
			match_word = match_object.group()
			span_from, span_to = match_object.span()

			if p[0] == match_word:
				if p[1] == "FRONT":
					chunk = chunk[span_to:]
				elif p[1] == "BACK":
					chunk = chunk[:span_from]

	return chunk


# **************************************************
# ----- Main Process
# **************************************************
if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	with open("./../test/test.txt", "r", encoding="utf-8") as file:
		samples = file.readlines()

	for sample in samples:
		print(
			f"text: {sample.strip()}\n"
			f"=> {main(sample.strip())}\n"
		)


# **************************************************
# ----- End
# **************************************************
