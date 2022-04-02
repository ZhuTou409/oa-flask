from flask import Flask
from flask import jsonify
from flask import request, jsonify, session, Blueprint
# from router import app, cors
from flask_cors import CORS, cross_origin
from flask_login import LoginManager
from app import ServerInstance

FlaskApp = Flask(__name__)
FlaskApp.secret_key = "FlaskOaSystem"
cors = CORS(FlaskApp)

ServerInstance.login_manager = LoginManager()
ServerInstance.login_manager.login_view = 'auth_flask_login.login'
ServerInstance.login_manager.login_message_category = 'info'
ServerInstance.login_manager.login_message = '请登录'
ServerInstance.login_manager.init_app(FlaskApp)
ServerInstance.App = FlaskApp

# app = Flask(__name__)
# cors = CORS(app)

# Get Blueprint Apps
from LoginModule.oa_login import auth_flask_login
FlaskApp.register_blueprint(auth_flask_login)

# Register Blueprints
# app.register_blueprint(auth_flask_login)


@FlaskApp.route('/test', methods=['GET', 'POST'])
def hello_world():
    data = request.get_json(silent=True)
    print("register in ：{}".format(str(data)))
    return 'Hello World!'


@FlaskApp.route('/getMsg', methods=['GET', 'POST'])
def home():
    response = {
        'msg': 'Hello, Python !'
    }
    return jsonify(response)


# 启动运行
if __name__ == '__main__':
    FlaskApp.run(debug=True)
# app.run(host='your_ip_address') # 这里可通过 host 指定在公网IP上运行

