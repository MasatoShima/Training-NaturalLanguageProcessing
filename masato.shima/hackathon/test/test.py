"""
Name: test.py
Description: PDF ファイルの解析～情報抽出用 Web-API への問い合わせを行う
Created by: Masato Shima
Created on: 2019/12/25
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
from typing import *

import requests


# **************************************************
# ----- Constants & Variables
# **************************************************
URL = "http://52.195.11.63:8080/extract-pdf"


# **************************************************
# ----- Main
# **************************************************
def main():
	sending_pdf()

	return


# **************************************************
# ----- Function
# **************************************************
def sending_pdf() -> None:
	with open("./test.pdf", "rb") as file:
		content = file.read()

	files = {
		"file": (None, content)
	}

	response = requests.post(
		url=URL,
		files=files
	)

	if response.status_code == 200:
		print(f"Success sending news [HTTP STATUS: {response.status_code}]")
	else:
		print(f"Failed sending news [HTTP STATUS: {response.status_code}]")

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
