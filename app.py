import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User
#from flask_script import Manager
from flask_migrate import Migrate

BASEDIR = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(BASEDIR, "test.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV']= 'development'
app.config['DEBUG']= True

#manager = Manager(app)
db.init_app(app)
Migrate(app, db)


@app.route('/')
def home():
    return jsonify("Hola Mundo")

@app.route("/user", methods=["POST", "GET"])
def user():
    if request.method == "GET":
        user = User.query(1)
        if user is not None:
            return jsonify(user.serialize_just_username)
    else:
        user = User()
        data = request.json.get("name")
        user.name = request.json.get("name")
        user.password = request.json.get("password")
        user.email = request.json.get("email")
        user.isActive = request.json.get("isActive")
        print(user)


        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize()), 200


if __name__ == "__main__":
        app.run(host='localhost', port=8080)