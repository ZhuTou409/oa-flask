from flask import Flask
from flask import jsonify
from flask_cors import CORS
from router import app, cors

# app = Flask(__name__)
# cors = CORS(app, resources={r"/getMsg": {"origins": "*"}})


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


# 启动运行
# if __name__ == '__main__':
#     app.run(debug=True)
# app.run(host='your_ip_address') # 这里可通过 host 指定在公网IP上运行
