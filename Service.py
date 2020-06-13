from flask import Flask, jsonify
from flask import request
from src.Controller import Controller
from flask_cors import CORS, cross_origin
from mysql.connector import Error
import time

from src.QueryValidator import QueryValidator

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources=r'/*', headers='Content-Type')
service = Controller()
validator = QueryValidator()

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
    rate = Data['rate']
    try:
        isValidated, message = validator.checkIntegralQuery(query)
        if not isValidated:
            return message, 209
        start_time = time.time()
        result, positive_ids= service.getQueryAlternativeConditions(query, database, negation, rate)
        dataToSend = {'results': result, 'pos_ids': positive_ids}
        print("--- %s seconds ---" % (time.time() - start_time))
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
        isValidated, message = validator.checkExecuteQuery(query)
        if not isValidated:
            return message, 209
        result, columns = service.executeQuery(query, database)
        print("Result size" + str(len(result)))
        dataToSend = {'results': result, 'columns': columns}
        response = jsonify(dataToSend)
        return response
    except Error as n:
        return n.msg, 209

@app.route('/executeId', methods=['POST'])
@cross_origin()
def executeQueryId():
    request_json = request.get_json()
    Data = request_json['Data']
    database = Data['database']
    query = Data['query']
    try:
        result = service.executeQueryId(query, database)
        dataToSend = {'results': result}
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

@app.route('/maxMin', methods=['GET', 'POST'])
@cross_origin()
def getMinMax():
    request_json = request.get_json()
    Data = request_json['Data']
    table = Data['table']
    database = Data['database']
    column = Data['column']
    try:
        result = service.getMinMaxColumn(database, table, column)
        response = jsonify(result)
        return response
    except Error as n:
        return n.msg, 209


if __name__ == '__main__':
    app.run()
