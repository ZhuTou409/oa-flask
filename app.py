# import os
#
# from flask import Flask, render_template, request, redirect  # etc.
from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS


class ServerApp:
    def __init__(self):
        self.App = None
        self.Cors = None
        self.login_manager = None

    def GetApp(self):
        return self.App

    def GetCors(self):
        return self.Cors

    def GetLoginManager(self):
        return self.login_manager


ServerInstance = ServerApp()

# app = Flask(__name__)
# cors = CORS(app)

# Create and name Flask app
# app = Flask("FlaskLoginApp")
#
# # database connection
# app.config['MONGODB_SETTINGS'] = {'HOST': os.environ.get('MONGOLAB_URI'),'DB': 'FlaskLogin'}
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.debug = os.environ.get('DEBUG', False)

# Associate Flask-Login manager with current app
# login_manager = LoginManager()
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
# login_manager.login_message = '请登录'
# login_manager.init_app(app)

