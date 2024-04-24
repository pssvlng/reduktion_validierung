
import os
from urllib.parse import unquote

from flask import Flask
from flask import Response
from flask import request, jsonify
from flask_cors import CORS, cross_origin

from passivlingo_dictionary.Dictionary import Dictionary
from passivlingo_dictionary.models.SearchParam import SearchParam

import nltk
from encoders.WordEncoder import WordEncoder

from bs4 import BeautifulSoup
import requests
import re
from rdflib.namespace import _SKOS, _RDFS
from config import cors_dev_config, cors_prod_config
from spacy_config import create_pipeline_de, create_pipeline_en

from langdetect import detect

app = Flask(__name__)

# if os.environ.get("FLASK_ENV") == "production":    
#     CORS(app, resources={r"/api/*": cors_prod_config})
# else:    
#     CORS(app, resources={r"/api/*": cors_dev_config})        

# dictionary endpoints

nlp = {}
nlp['en'] = create_pipeline_en()
nlp['de'] = create_pipeline_de()

@app.route('/api/validate/description', methods=['POST'])
@cross_origin()
def weightedWords():            
	text = request.json['text']
	lang = request.json['lang'] 
	
	try:
		model = nlp[lang]
		words = model(text)
		
		if len(words) < 5:			
			response = {
					"status": "ERROR",
					"message": "Beschreibung zu kurz"
			}
			return jsonify(response)	

		nouns_and_named_entities = [token.text for token in words if token.pos_ == "NOUN" or token.ent_type_ != ""]
		if len(nouns_and_named_entities) == 0:
			response = {
					"status": "ERROR",
					"message": "mindestens ein Substantiv im Beschreibungstext erforderlich"
			}
			return jsonify(response)				

		verbs = [token.text for token in words if token.pos_ in ["VERB", "AUX"]]
		if len(verbs) == 0:
			response = {
					"status": "WARNING",
					"message": "Der Text enthält keine Verben"
			}
			return jsonify(response)				

		response = {
					"status": "OK",
					"message": ""
			}
		return jsonify(response)				
		
		#return Response(response=jsonify(response), status=200, mimetype="application/json")    

	except ValueError as err:
		return Response(response='{"message":"' + format(err) + '"}', status=404, mimetype="application/json")    


    



