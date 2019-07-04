from flask import Flask, request
from flask_restplus import Api, Resource
from log import Log
from flask_sqlalchemy import SQLAlchemy

flask_app = Flask(__name__)
app = Api(app=flask_app)

name_space = app.namespace('main', description='Main APIs')
sql = SQLAlchemy()

@name_space.route("/<int:id>")
class Log(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'id': 'Specify the Id associated with the person'})
    def get(self,id):
        return {
            "status": "Got new data " + str(id)
        }

    def put(self, id):
        return {
            "status": "Updated data " + str(id)
        }

    def delete(self):
        return {
            "status": "Deleted data"
        }


@name_space.route("/")
class LogList(Resource):
    def get(self):

        log = Log()
        log.detail = 'xxxx'
        sql.session.add(log)
        sql.session.commit()

        return {
            "status": "List all data"
        }

    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'detail': 'Log detail text'})
    def post(self):
        return {
            "status": "Post new data"
        }