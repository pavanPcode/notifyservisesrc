from flask import Flask, jsonify,request,send_from_directory
from flask_cors import CORS
# import requests
# from datetime import datetime
# import logging
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
cors = CORS(app)

@app.route('/swagger/swagger.yml')
def send_swagger():
    return send_from_directory('swagger', 'swagger.yml')

SWAGGER_URL = '/swagger'
API_URL = '/swagger/swagger.yml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "WhatsApp Notification API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/')
def ServiceHealth():
    return jsonify('Service Is Up')


import notify
app.register_blueprint(notify.notifyservice)

##
# from RollCallAPI import myrollcall
# from RollCallAPI import adminrollcall
#app.register_blueprint(myrollcall.rcservice)
# app.register_blueprint(adminrollcall.adminrc)


if __name__ == "__main__":
    app.run()
