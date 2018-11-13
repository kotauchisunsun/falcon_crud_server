import tornado.wsgi
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

"""
初期化
from main import db
db.create_all()
"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


#curl -H 'Content-Type:application/json' -d '{"username":"ryo","email":"ryo@email.com"}' -X POST localhost:8888/users

#Create
@app.route("/users", methods=['POST'])
def create():
    data = request.json
    username = data["username"]
    email = data["email"]
    user = User(username=username, email=email)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })

#Read
@app.route("/users/<user_id>")
def read(user_id):
    user = User.query.filter_by(id=user_id).first()
    return jsonify(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }        
    )

#curl -H 'Content-Type:application/json' -d '{"username":"ryo2","email":"ryo@email.com"}' -X PUT localhost:8888/users/3

#Update
@app.route("/users/<user_id>", methods=['PUT'])
def update(user_id):
    print(user_id)
    data = request.json
    username = data["username"]
    email = data["email"]
    user = User.query.filter_by(id=user_id).first()

    user.username = username
    user.email = email

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })

#curl -H 'Content-Type:application/json' -X DELETE localhost:8888/users/3

#Delete
@app.route("/users/<user_id>", methods=['DELETE'])
def delete(user_id):
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return None

@app.route("/")
def hello():
    return "Hello World!"

def run():
    container = tornado.wsgi.WSGIContainer(app)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__=="__main__":
    run()
