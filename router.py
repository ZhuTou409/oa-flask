from flask import Flask
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)

app.config["SECRET_KEY"] = "FlaskOASystem"

cors = CORS(app, resources={r"/getMsg": {"origins": "*"}})


# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# @app.route('/getMsg', methods=['GET', 'POST'])
# def home():
#     response = {
#         'msg': 'Hello, Python !'
#     }
#     return jsonify(response)

