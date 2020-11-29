"""
Name: sample_03_02
Description: sample script from chapter 3
Created by: Masato Shima
Created on: 2019/07/03
"""

# **************************************************
# ----- Import Library
# **************************************************
import os

from mylib import sqlitedatastore as datastore


# **************************************************
# ----- Config
# **************************************************


# **************************************************
# ----- Main Function
# **************************************************
def main():
	datastore.connect()
	datastore.create_table()
	datastore.close()

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
