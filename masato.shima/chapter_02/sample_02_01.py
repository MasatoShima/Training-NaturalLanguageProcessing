"""
Name: sample_02_01
Description: sample script from chapter 2
Created by: Masato Shima
Created on: 2019/06/19
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import requests


# **************************************************
# ----- Variables
# **************************************************
url = "https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC"


# **************************************************
# ----- Main Function
# **************************************************
def main():
	response = requests.get(url)

	print(response.text)

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
