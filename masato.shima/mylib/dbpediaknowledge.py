"""
Name: dbpediaknowledge.py
Description: DBpedia を問い合わせを行い, データを取得する
Created by: Masato Shima
Created on: 2019/09/25
"""

# **************************************************
# ----- Import Library
# **************************************************
from typing import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from SPARQLWrapper import JSON, SPARQLWrapper

from mylib import cabochaparser as parser


# **************************************************
# ----- Function get_synonyms
# **************************************************
def get_synonyms(text: str) -> List[Dict[str, str]]:
	uri = f"<http://ja.dbpedia.org/resource/{text}>"

	sparql = SPARQLWrapper("http://ja.dbpedia.org/sparql")
	sparql.setReturnFormat(JSON)
	sparql.setQuery(
		f"""
		SELECT DISTINCT *
		WHERE {{
			{{ ?redirect <http://dbpedia.org/ontology/wikiPageRedirects> {uri} }}
			UNION
			{{ {uri} <http://dbpedia.org/ontology/wikiPageRedirects> ?redirect }} .
			?redirect <http://www.w3.org/2000/01/rdf-schema#label> ?synonym
		}}
		"""
	)

	results = []

	for x in sparql.query().convert()["results"]["bindings"]:
		word = x["synonym"]["value"]

		results.append(
			{
				"term": word
			}
		)

	return results


# **************************************************
# ----- Function calc_similarity
# **************************************************
def calc_similarity(text1: str, text2: str) -> float:
	summary1 = retrieve_abstract(text1)
	summary2 = retrieve_abstract(text2)

	if summary1 is None or summary2 is None:
		return 0

	sentences1, chunks1, tokens1 = parser.parse(summary1)
	doc1 = " ".join([token["lemma"] for token in tokens1])

	sentences2, chunks2, tokens2 = parser.parse(summary2)
	doc2 = " ".join([token["lemma"] for token in tokens2])

	vectorizer = CountVectorizer(analyzer="word")

	vectors = vectorizer.fit_transform([doc1, doc2])

	sim = cosine_similarity(vectors)

	return sim[0][1]


# **************************************************
# ----- Function retrieve_abstract
# **************************************************
def retrieve_abstract(text: str) -> str or None:
	uri = f"<http://ja.dbpedia.org/resource/{text}>"

	sparql = SPARQLWrapper("http://ja.dbpedia.org/sparql")
	sparql.setReturnFormat(JSON)
	sparql.setQuery(
		f"""
		SELECT DISTINCT *
		WHERE {{
			{{ {uri} <http://dbpedia.org/ontology/abstract> ?summary }}
		}}
		"""
	)

	results = sparql.query().convert()["results"]["bindings"]

	if len(results) > 0:
		return results[0]["summary"]["value"]
	else:
		return None


# **************************************************
# ----- Function get_population
# **************************************************
def get_population(text: str) -> int:
	uri = f"<http://ja.dbpedia.org/resource/{text}>"

	sparql = SPARQLWrapper("http://ja.dbpedia.org/sparql")
	sparql.setReturnFormat(JSON)
	sparql.setQuery(
		f"""
		SELECT DISTINCT *
		WHERE {{
			{{ {uri} <http://ja.dbpedia.org/property/人口値> ?population }}
		}}
		"""
	)

	results = sparql.query().convert()["results"]["bindings"]

	if len(results) > 0:
		population = results[0]["population"]["value"]
		return int(population)
	else:
		return -1


# **************************************************
# ----- End
# **************************************************
