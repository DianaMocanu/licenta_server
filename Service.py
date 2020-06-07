from flask import Flask, jsonify
from flask import request
from src.Controller import Controller
from flask_cors import CORS, cross_origin
from mysql.connector import Error

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources=r'/*', headers='Content-Type')
service = Controller()


@app.before_request
def oauth_verify(*args, **kwargs):
    if request.method in ['OPTIONS', ]:
        return


@app.route('/generate', methods=['POST'])
@cross_origin()
def generateQuery():
    request_json = request.get_json()
    Data = request_json['Data']
    database = Data['database']
    query = Data['query']
    negation = Data['negation']
    try:
        result, oldSize = service.getQueryAlternativeConditions(query, database, negation)
        dataToSend = {'results': result, 'oldSize': oldSize}
        response = jsonify(dataToSend)
        return response
    except Error as n:
        return n.msg, 209


@app.route('/execute', methods=['POST'])
@cross_origin()
def executeQuery():
    request_json = request.get_json()
    Data = request_json['Data']
    database = Data['database']
    query = Data['query']
    try:
        result, columns = service.executeQuery(query, database)
        print("Result size" + str(len(result)))
        dataToSend = {'results': result, 'columns': columns}
        response = jsonify(dataToSend)
        return response
    except Error as n:
        return n.msg, 209


@app.route('/tables', methods=['GET', 'POST'])
@cross_origin()
def getTables():
    request_json = request.get_json()
    Data = request_json['Data']
    database = Data['database']
    try:
        result = service.getTablesDatabase(database)
        response = jsonify(result)
        return response
    except Error as n:
        return n.msg, 209


@app.route('/columns', methods=['GET', 'POST'])
@cross_origin()
def getColumns():
    request_json = request.get_json()
    Data = request_json['Data']
    table = Data['table']
    database = Data['database']
    try:
        result = service.getColumns(database, table)
        response = jsonify(result)
        return response
    except Error as n:
        return n.msg, 209


if __name__ == '__main__':
    app.run()
