"""Ewondo Transcription Tansform API (ETTA)

Authors
 * St Germes Bengono Obiang 2023
"""

from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
import json
import argparse


import Utils
import numpy as np
from Syllabification import SyllabificationEwonodo
import string

app = Flask(__name__)
CORS(app)
import unidecode
# This is a sample Python script.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))

@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"


@app.route('/syll-word/<string:message>/')
def syllabationWord(message):
    print(message)
    core = SyllabificationEwonodo(message)
    syllabes = core.generate()
    print(syllabes)
    return {
        "error": False,
        "data": syllabes
    }


@app.route('/syll-sent/<string:sentence>/')
def syllabationSentense(sentence):
    print(sentence)
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    words = sentence.split(" ")
    result = []
    for word in words:
        core = SyllabificationEwonodo(word)
        result.append(core.generate())
    return {
        "error": False,
        "data": result
    }

@app.route("/docs")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Ewondo Transcription Transfrorm API (ETTA)"
    return jsonify(swag)


def configSwagger(port):
    SWAGGER_URL = '/api/docs'
    API_URL = f'http://127.0.0.1:{port}/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Ewondo Transcription Transform (ETTA)"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Ewondo Utils")
    parser.add_argument("-p", dest="port", help="The server starts on the selected port", type=int, default=2045)
    args = parser.parse_args()
    configSwagger(args.port)
    app.run(host='0.0.0.0', port=args.port)

