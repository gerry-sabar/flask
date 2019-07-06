from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, reqparse, fields
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, pprint

# Customisasi Flask
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/my_project'

# Flask Restplus
api = Api(app)
name_space = api.namespace('main', description='Main APIs')

# SQLAlchemy
db = SQLAlchemy(app)

my_fields = api.model('MyModel', {
    'detail': fields.String,
})

class LogSchema(Schema):
    id = fields.Int()
    detail = fields.Str()

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    detail = db.Column(db.Text)


@name_space.route("/<int:id>")
class LogDetail(Resource):
    @api.doc(
        responses=
        {
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error'
        },
        params=
        {
            'id': 'Specify the Id associated with the person'
        })
    def get(self, id):
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
    @api.doc(
        responses=
        {
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error'
        },
        params=
        {
            'detail': 'Log detail text'
        })
    def get(self):
        logs = Log.query.all()
        result = []
        resultSchema = []
        schema = LogSchema()
        for log in logs:
            result.append({
                'id': log.id,
                'detail': log.detail,
            })
            resultSchema.append(schema.dump(log))
        return {
            "data": result,
            "dataSchema": resultSchema
        }

    @api.doc(model='MyModel', body=my_fields)
    def post(self):
        payload = request.get_json()
        log = Log()
        log.detail = payload['detail']
        db.session.add(log)
        db.session.commit()

        return {
            "data": log
        }
