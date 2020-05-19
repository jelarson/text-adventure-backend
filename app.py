from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from environs import Env
import os

app = Flask(__name__)
CORS(app)
heroku = Heroku(app)

env = Env()
env.read_env()
DATABASE_URL = env("DATABASE_URL")
 
basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
#     os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Adventures Table

class Adventure(db.Model):
    __tablename__ = "adventure"
    id = db.Column(db.Integer, primary_key=True)
    # health = db.Column(db.String(10), nullable=False)
    # family = db.Column(db.String(10), nullable=False)
    # points = db.Column(db.String(10), nullable=False)
    # security = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(2500), nullable=False)
    buttonOneName = db.Column(db.String(100), nullable=False)
    buttonTwoName = db.Column(db.String(100), nullable=False)
    buttonOnePath = db.Column(db.String(100), nullable=False)
    buttonTwoPath = db.Column(db.String(100), nullable=False)
    # resultOne = db.Column(db.String(2500), nullable=False)
    # resultTwo = db.Column(db.String(2500), nullable=False)
    # resultPath = db.Column(db.String(10), nullable=False)
    # adventurePath = db.Column(db.String(10), nullable=False)

    def __init__(self, description, buttonOneName, buttonTwoName, buttonOnePath, buttonTwoPath):
        # self.health = health
        # self.family = family
        # self.points = points
        # self.security = security
        self.description = description
        self.buttonOneName = buttonOneName
        self.buttonTwoName = buttonTwoName
        self.buttonOnePath = buttonOnePath
        self.buttonTwoPath = buttonTwoPath
        # self.resultOne = resultOne
        # self.resultTwo = resultTwo
        # self.resultPath = resultPath
        # self.adventurePath = adventurePath

class AdventureSchema(ma.Schema):
    class Meta:
        fields = ('id', 'description', 'buttonOneName', 'buttonTwoName', 'buttonOnePath', 'buttonTwoPath')


adventure_schema = AdventureSchema()
adventures_schema = AdventureSchema(many=True)

# Results Table

class Result(db.Model):
    __tablename__ = "result"
    id = db.Column(db.Integer, primary_key=True)
    health = db.Column(db.String(10), nullable=False)
    family = db.Column(db.String(10), nullable=False)
    points = db.Column(db.String(10), nullable=False)
    security = db.Column(db.String(10), nullable=False)
    resultDesc = db.Column(db.String(2500), nullable=False)
    resultPath = db.Column(db.String(10), nullable=False)

    def __init__(self, health, family, points, security, resultDesc, resultPath):
        self.health = health
        self.family = family
        self.points = points
        self.security = security
        self.resultDesc = resultDesc
        self.resultPath = resultPath

class ResultSchema(ma.Schema):
    class Meta:
        fields = ('id', 'health', 'family', 'points', 'security', 'resultDesc', 'resultPath')


result_schema = ResultSchema()
results_schema = ResultSchema(many=True)

# Routes

@app.route('/', methods=["GET"])
def home():
    return "<h1>Text Adventure API</h1>"

# Adventure Routes

@app.route('/adventure', methods=['POST'])
def add_adventure():
    # health = request.json['health']
    # family = request.json['family']
    # points = request.json['points']
    # security = request.json['security']
    description = request.json['description']
    buttonOneName = request.json['buttonOneName']
    buttonTwoName = request.json['buttonTwoName']
    buttonOnePath = request.json['buttonOnePath']
    buttonTwoPath = request.json['buttonTwoPath']
    # resultOne = request.json['resultOne']
    # resultTwo = request.json['resultTwo']
    # resultPath = request.json['resultPath']
    # adventurePath = request.json['adventurePath']


    new_adventure = Adventure(description, buttonOneName, buttonTwoName, buttonOnePath, buttonTwoPath)

    db.session.add(new_adventure)
    db.session.commit()

    adventure = Adventure.query.get(new_adventure.id)
    return adventure_schema.jsonify(adventure)

@app.route('/adventures', methods=["GET"])
def get_adventures():
    all_adventures = Adventure.query.all()
    result = adventures_schema.dump(all_adventures)

    return jsonify(result)

@app.route('/adventure/<id>', methods=['GET'])
def get_adventure(id):
    adventure = Adventure.query.get(id)

    result = adventure_schema.dump(adventure)
    return jsonify(result)

@app.route('/product/<id>', methods=['PATCH'])
def update_category(id):
    adventure = Adventure.query.get(id)

    # new_health = request.json['inventory']
    # new_family = request.json['family']
    # new_points = request.json['points']
    # new_security = request.json['security']
    new_description = request.json['description']
    new_buttonOneName = request.json['buttonOneName']
    new_buttonTwoName = request.json['buttonTwoName']
    new_buttonOnePath = request.json['buttonOnePath']
    new_buttonTwoPath = request.json['buttonTwoPath']
    # new_resultOne = request.json['resultOne']
    # new_resultTwo = request.json['resultTwo']
    # new_resultPath = request.json['resultPath']

    # adventure.health = new_health
    # adventure.family = new_family
    # adventure.points = new_points
    # adventure.security = new_security
    adventure.description = new_description
    adventure.buttonOneName = new_buttonOneName
    adventure.buttonTwoName = new_buttonTwoName
    adventure.buttonOnePath = new_buttonOnePath
    adventure.buttonTwoPath = new_buttonTwoPath
    # adventure.resultOne = new_resultOne
    # adventure.resultTwo = new_resultTwo
    # adventure.resultPath = new_resultPath


    db.session.commit()
    return adventure_schema.jsonify(adventure)

@app.route('/adventure/<id>', methods=['DELETE'])
def delete_adventure(id):
    record = Adventure.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify('Item deleted')

# Result Routes

@app.route('/result', methods=['POST'])
def add_result():
    health = request.json['health']
    family = request.json['family']
    points = request.json['points']
    security = request.json['security']
    resultDesc = request.json['resultDesc']
    resultPath = request.json['resultPath']


    new_result = Result(health, family, points, security, resultDesc, resultPath)

    db.session.add(new_result)
    db.session.commit()

    result1 = Result.query.get(new_result.id)
    return result_schema.jsonify(result1)

@app.route('/results', methods=["GET"])
def get_results():
    all_results = Result.query.all()
    result = results_schema.dump(all_results)

    return jsonify(result)

@app.route('/result/<id>', methods=['GET'])
def get_result(id):
    result = Result.query.get(id)

    result1 = result_schema.dump(result)
    return jsonify(result1)

@app.route('/result/<id>', methods=['PATCH'])
def update_result(id):
    result = Result.query.get(id)

    new_health = request.json['inventory']
    new_family = request.json['family']
    new_points = request.json['points']
    new_security = request.json['security']
    new_resultDesc = request.json['resultDesc']
    new_resultPath = request.json['resultPath']

    result.health = new_health
    result.family = new_family
    result.points = new_points
    result.security = new_security
    result.resultDesc = new_resultDesc
    result.resultPath = new_resultPath


    db.session.commit()
    return result_schema.jsonify(result)

@app.route('/result/<id>', methods=['DELETE'])
def delete_result(id):
    record = Result.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify('Item deleted')