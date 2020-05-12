from flask import Flask, jsonify
from flask import request
from flask import after_this_request
from src.Service import Service
from flask_cors import CORS, cross_origin

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
    result = service.getQueryAlternativeConditions(query, database)
    response = jsonify(result)
    return response

@app.route('/execute', methods=['POST'])
@cross_origin()
def executeQuery():

    request_json = request.get_json()
    Data = request_json['Data']
    database = Data['database']
    query = Data['query']
    result, columns = service.executeQuery(query, database)
    dataToSend = {'results': result, 'columns': columns}
    response = jsonify(dataToSend)
    return response

if __name__ == '__main__':
    app.run()
