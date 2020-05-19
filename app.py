from flask import Flask, jsonify
from flask import request
from flask import after_this_request
from src.Service import Service
from flask_cors import CORS, cross_origin
from mysql.connector import Error

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources=r'/*', headers='Content-Type')
service = Service()


# @app.after_request
# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   response.headers.add('Access-Control-Allow-Credentials', 'true')
#   return response


@app.before_request
def oauth_verify(*args, **kwargs):
    """Ensure the oauth authorization header is set"""
    if request.method in ['OPTIONS', ]:
        return


@app.route('/query', methods=['POST'])
@cross_origin()
def generateQuery():
    request_json = request.get_json()
    Data = request_json['Data']
    database = Data['database']
    query = Data['query']
    try:
        result = service.getQueryAlternativeConditions(query, database)
        response = jsonify(result)
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


# @app.errorhandler(500)
# @cross_origin()
# def internal_error(error):
#     print(error)
#     return jsonify(error), 201


if __name__ == '__main__':
    app.run()
