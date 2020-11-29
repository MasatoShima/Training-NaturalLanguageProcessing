"""
Name: sqlitedatastore
Description:
Created by: Masato Shima
Created on: 2019/07/03
"""

# **************************************************
# ----- Import Library
# **************************************************
import json
import sqlite3


# **************************************************
# ----- Constants & Variables
# **************************************************
client = None


# **************************************************
# ----- Function connect
# **************************************************
def connect():
	global client

	client = sqlite3.connect("./../data/sample.db")

	return client


# **************************************************
# ----- Function close
# **************************************************
def close():
	client.close()

	return client


# **************************************************
# ----- Function create_table
# **************************************************
def create_table():
	client.execute("DROP TABLE IF EXISTS docs")
	client.execute(
		"""
		CREATE TABLE docs (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		content TEXT,
		meta_info BLOB,
		sentence BLOB,
		chunk BLOB,
		token BLOB
		)
		"""
	)

	return


# **************************************************
# ----- Function put
# **************************************************
def put(values):
	client.executemany(
		"INSERT INTO docs (content, meta_info) VALUES (?,?)",
		values
	)

	client.commit()

	return


# **************************************************
# ----- Function get
# **************************************************
def get(doc_id, fl):
	row_ls = client.execute(
		f"SELECT {','.join(fl)} FROM docs WHERE id = ?",
		(doc_id, )
	)

	row_ls = row_ls.fetchone()

	row_dict = {}

	for key, value in zip(fl, row_ls):
		row_dict[key] = value

	return row_dict


# **************************************************
# ----- Function get_all_ids
# **************************************************
def get_all_ids(limit, offset=0):
	records = client.execute(
		"SELECT id FROM docs LIMIT ? OFFSET ?",
		(limit, offset)
	)

	records = [record[0] for record in records]

	return records


# **************************************************
# ----- Function put_annotation
# **************************************************
def put_annotation(doc_id, name, value):
	client.execute(
		f"UPDATE docs SET {name} = ? WHERE id = ?",
		(json.dumps(value), doc_id)
	)

	client.commit()

	return


# **************************************************
# ----- Function get_annotation
# **************************************************
def get_annotation(doc_id, name):
	row = client.execute(
		f"SELECT {name} FROM docs WHERE id = ?",
		(doc_id, )
	)

	row = row.fetchone()

	if row[0] is not None:
		return json.loads(row[0])

	else:
		return []


# **************************************************
# ----- End
# **************************************************
