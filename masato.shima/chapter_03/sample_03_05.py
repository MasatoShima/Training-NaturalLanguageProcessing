"""
Name: sample_03_05
Description: sample script from chapter 3
Created by: Masato Shima
Created on: 2019/07/17
"""

# **************************************************
# ----- Import Library
# **************************************************
import os

from mylib import sqlitedatastore as datastore


# **************************************************
# ----- Main Function
# **************************************************
def main():
	datastore.connect()

	for doc_id in datastore.get_all_ids(limit=10):
		row = datastore.get(doc_id, ["id", "content", "meta_info"])

		print(
			f"{row['id']}\n"
			f"{row['meta_info']}\n"
			f"{row['content']}\n"
			f"********"
		)

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
