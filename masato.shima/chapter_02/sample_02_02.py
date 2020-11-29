"""
Name: sample_02_02
Description: sample script from chapter 2
Created by: Masato Shima
Created on: 2019/06/19
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import urllib.request
import cchardet


# **************************************************
# ----- Variables
# **************************************************
url = "https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC"


# **************************************************
# ----- Main Function
# **************************************************
def main():
	with urllib.request.urlopen(url) as response:
		data_bytes = response.read()
		data_string = data_bytes.decode(cchardet.detect(data_bytes)["encoding"])

	print(data_string)

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
