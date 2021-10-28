import datetime
import requests
import json
import pymongo
import argparse
from flask import Flask, request, jsonify, render_template
from database import get_key


app = Flask(__name__)

@app.route('/champions', methods=['GET'])
def getAllChampions():
    """
    Function for an API Get Request
    """
    client = pymongo.MongoClient(get_key())
    data_base = client['Collection']
    champions = data_base["Champions"]
    output = []
    if champions.find() is None:
        output.append({'time' : datetime.datetime.now(), 'status' : 400,
                       'message' : 'Get Failed.'})
        return jsonify(output)
    for champ in champions.find():
        output.append({"name" : champ['name'],
        'win_rate' :  champ['win_rate'],
        'pick_rate' : champ['pick_rate'],
        'counter_champs' : champ['counter_champs'],
        'strong_against' : champ['strong_against']})
    return jsonify(output)