"""
Name: app.py
Description: Simple Web-API. Extract data from PDF file and return it
Created by: Masato Shima
Created on: 2019/12/04
"""

# **************************************************
# ----- Import Library
# **************************************************
import os
import logging
import traceback
import responder


# **************************************************
# ----- Constants & Variables
# **************************************************
DIR_TMP = "./tmp/"


# **************************************************
# ----- Set logger
# **************************************************
logger = logging.getLogger(str(os.path.basename(__file__).split(".")[0]))
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s [%(name)s] %(message)s"))

logger.addHandler(handler)
logger.propagate = False


# **************************************************
# ----- Main
# **************************************************
api = responder.API()


# **************************************************
# ----- Method test
# **************************************************
@api.route("/test")
def hello_world(req, res):
	content = "Hello World !"

	res.text = content

	return


# **************************************************
# ----- Method extract-pdf
# **************************************************
@api.route("/extract-pdf")
async def extract_pdf(req, res):
	@api.background.task
	def process(d):
		post_data = d["file"]

		with open(f"./{DIR_TMP}test_uploaded.pdf", "wb") as file:
			file.write(post_data)

	try:
		data = await req.media(format="files")

		process(data)

		res.media = {
			"status": "Success",
		}

	except Exception as error_info:
		logger.error(
			f"Failed...\n"
			f"{error_info}\n"
			f"{traceback.format_exc()}"
		)

		res.media = {
			"status": "Failed",
		}

	return


# **************************************************
# ----- Start
# **************************************************
# Change current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create temporary directory
os.makedirs(DIR_TMP, exist_ok=True)

# Run Web-API
api.run(address="0.0.0.0", port=8000)


# **************************************************
# ----- End
# **************************************************
