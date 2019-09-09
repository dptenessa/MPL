from flask import Flask
from flask_restful import request, Resource, Api
from Main import *


app = Flask(__name__)
api = Api(app)

class search(Resource):
    def get(self):
        args = request.args
        phone_name, memory, tariff, channel, transaction, finance, commitment = args.get("param1", ""), args.get("param2", ""), \
                                                                           args.get("param3", ""), args.get("param4", ""), \
                                                                           args.get("param5", ""), args.get("param6", ""), \
                                                                           args.get("param7", "")
        json = return_phome_info(phone_name, memory, tariff, channel, transaction, finance, commitment)
        return json

api.add_resource(search,'/events')
app.run(debug=True)