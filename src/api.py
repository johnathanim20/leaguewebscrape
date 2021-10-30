'''
set FLASK_APP=src/api
flask run
api for our champions application
'''

import datetime
import requests
import json
import pymongo
import argparse
from flask import Flask, request, jsonify, render_template
from database import get_key, get_collection


app = Flask(__name__)

@app.route('/champions', methods=['GET'])
def getAllChampions():
    """
    Function for an API Get Request
    """
    
    champions = get_collection()
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
    return jsonify({'result' : output})

@app.route('/champion', methods=['GET'])
def getChampion():
    """
    Function for an API GET Request by name 
    """
    champ_name = request.args.get("name")
    champions = get_collection()
    output = []
    champ = champions.find_one({'name' : champ_name})
    if champ:
        output.append({"name" : champ['name'],
        'win_rate' :  champ['win_rate'],
        'pick_rate' : champ['pick_rate'],
        'counter_champs' : champ['counter_champs'],
        'strong_against' : champ['strong_against']})
        return jsonify(output)
    output.append({'time' : datetime.datetime.now(), 'status' : 400,
                       'message' : 'Get Failed.'})
    return jsonify({'result' : output})

"""PUT request for champion."""
@app.route('/champion', methods=['PUT'])
def put_champion():
    id_ = request.args.get("name") # @UndefinedVariable
    update_values = request.get_json()
    if id_ is None or update_values is None or len(request.args) > 1:
        bad_input_error = {
                "status": 400,
                "error":"Bad Request"
                }
        
        return bad_input_error
    
    result = get_collection().update({'name' : id_}, {"$set": update_values})
    
    if not result["updatedExisting"]:
        error = {
                "status": 500,
                "error":"Internal Server Error",
                "message":"No champions found with given name"
                }
        
        return error
    
    return "updated champion entry: " + id_

"""POST request for champion."""
@app.route('/champion', methods=['POST'])
def make_new_champion():
    update_values = request.get_json()
    
    if update_values is None or len(request.args) > 0 or not send.valid_book(request.get_json()):
        bad_input_error = {
                "status": 400,
                "error":"Bad Request"
                }
        
        return bad_input_error
    
    r = get_collection().update({'name' : update_values['name']}, {"$setOnInsert":update_values}, upsert=True)
    
    if r["updatedExisting"]:
        error = {
                "status": 500,
                "error":"Internal Server Error",
                "message":"Champion entry already exists"
                }
        
        return error
    
    return jsonify({'result' : update_values})

"""DELETE a champion."""
@app.route('/champion', methods=['DELETE'])
def delete_champion():
    _id = request.args.get("name") # @UndefinedVariable
    
    if _id is None or len(request.args) > 1:
        bad_input_error = {
                "status": 400,
                "error":"Bad Request"
                }
        
        return bad_input_error
    
    get_collection().remove({"name" : _id})
    
    return "deleted champion with name " + _id

