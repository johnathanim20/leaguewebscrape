'''
set FLASK_APP=src/api
flask run
api for our champions application
'''
import pprint
import datetime
import requests
import json
import pymongo
import argparse
from query_parser import Query
from flask import Flask, request, jsonify, render_template, send_from_directory
from database import get_key, get_collection, valid_champ
import scrape_exe


app = Flask(__name__, static_folder="static")

@app.route('/')
def home():
    """
    this function serves our html template of our homepage
    """
    #file_template = send_from_directory('client', "index.html")
    #return render_template("index.html")
    return send_from_directory('templates', "index.html")

@app.route('/PRVisual')
def pr_champ_vis():
    """
    this function returns the html template of our bar graph page for pick rate
    """
    #file_template = send_from_directory('client', "index.html")
    #return render_template("index.html")
    return send_from_directory('templates', "pr_champion_visual.html")

@app.route('/WRVisual')
def wr_champ_vis():
    """
    this function returns the html template of our bar graph page for win rate
    """
    #file_template = send_from_directory('client', "index.html")
    #return render_template("index.html")
    return send_from_directory('templates', "wr_champion_visual.html")

@app.route('/CRUD')
def crud_operations():
    """
    this function returns the html templateof our CRUD operations
    """
    #file_template = send_from_directory('client', "index.html")
    #return render_template("index.html")
    return send_from_directory('templates', "CRUD.html")

"""GET request for search and a query."""
@app.route('/search')
def get_search():
    query = request.args.get("q") # @UndefinedVariable
    query_parse = Query()
    
    if query is None or len(request.args) > 1:
        bad_input_error = {
                "status": 400,
                "error":"Bad Request"
                }
        
        return bad_input_error
    
    query_info = query_parse.parse_user_input(query)
    query_result = query_parse.query_handler(query_info[0], query_info[1], query_info[2])
    if not query_result:
        error = {
                "status": 500,
                "error":"Internal Server Error",
                "message":"No entries found with given query"
                }
        
        return error
        
    query_result_cleaned = []
    
    for i in query_result:
        query_result_cleaned.append(i)
    
    return  jsonify({'result' : query_result_cleaned})
@app.route('/champions', methods=['GET'])

def getAllChampions():
    """
    Function for an API Get Request to get all champ docs in database
    """
    if len(request.args) > 0 :
        bad_input_error = {
                'status': 400,
                "error":"Bad Request"
                }
        
        return bad_input_error
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
        'champ_tier' : champ['champ_tier'],
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
        'champ_tier' : champ['champ_tier'],
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
    
    if update_values is None or len(request.args) > 0 or not valid_champ(request.get_json()):
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
    
    result = get_collection().remove({"name" : _id})
    
    if result["n"] == 0:
        error = {
                "status": 500,
                "error":"Internal Server Error",
                "message":"Champion entry already deleted"
                }
        
        return error
    
    return "deleted champion with name " + _id

"""activates scrape function in scrape_exe module"""
@app.route('/scrape', methods=['POST'])
def scrape_new_entries():
    
    if len(request.args) > 0:
        bad_input_error = {
                "status": 400,
                "error":"Bad Request"
                }
        
        return bad_input_error
    
    scrape_exe.main()
    
    
    return "scraping done"


if __name__ == '__main__':
    app.run(debug=False)

