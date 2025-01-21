from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
from datetime import datetime
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change to this!
# app.config['SECRET KEY'] = 'SUPER-SECRET-KEY'# wrong
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
jwt = JWTManager(app)
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=True)
    with app.app_context():
        db.create_all()

    def register_student(self, username, password):
        if not username or not password:
            return 'Missing username or password'
        if Users.query.filter_by(username=username).first():
            return "Name already taken"
        new_user = Users(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return 'User created successfully'

    def login(self, username, password):
        user = Users.query.filter_by(username=username).first()
        if user and user.password == password:
            access_token = create_access_token(identity=user.id)
            return {'access token': access_token}
        return 'invalid credential '

    def data(self):
        current_user_id = get_jwt_identity()
        user = Users.query.filter_by(id=current_user_id).first()
        return f"Hello {user.username}, you are accessed to protected data "


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    data = request.get_json()
    username = data['username']
    password = data['password']
    dat = Users()
    responses = dat.register_student(username, password)

    return jsonify(responses)


@app.route('/log', methods=['POST', 'GET'])
def log():
    data = request.get_json()
    username = data['username']
    password = data['password']
    dat = Users()
    response = dat.login(username, password)
    return jsonify(response)


@app.route('/fetchdata', methods=['POST', 'GET'])
@jwt_required()
def fetchdata():
    dat = Users()
    response = dat.data()
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_restful import Resource, Api
# from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
# app = Flask(__name__)
# app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
# # app.config['SECRET KEY'] = 'SUPER-SECRET-KEY' #wrong
# # app.config["JWT_ALGORITHM"] = "SHA256"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# jwt = JWTManager(app)
# db = SQLAlchemy(app)
# api = Api(app)
#
#
# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), nullable=False)
#     password = db.Column(db.String(120), nullable=True)
#
#
# with app.app_context():
#     db.create_all()
#
#
# class RegisterUser(Resource):
#     def post(self):
#         data = request.get_json()
#         username = data['username']
#         password = data['password']
#
#         if not username or not password:
#             return 'Missing username or password'
#         if Users.query.filter_by(username=username).first():
#             return "Name already taken"
#         new_user = Users(username=username, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#         return 'User created successfully'
#
#
# class LoginUser(Resource):
#     def post(self):
#         data = request.get_json()
#         username = data['username']
#         password = data['password']
#         user = Users.query.filter_by(username=username).first()
#         if user and user.password == password:
#             access_token = create_access_token(identity=user.id)
#             return {'access token': access_token}
#         return 'invalid credential '
#
#
# class Data(Resource):
#     @jwt_required()
#     def get(self):
#         current_user_id = get_jwt_identity()
#         user = Users.query.filter_by(id=current_user_id).first()
#         return f"Hello {user.username}, you are accessed to protected data "
#
#
# api.add_resource(RegisterUser, '/register')
# api.add_resource(LoginUser, '/login')
# api.add_resource(Data, '/getdata')
#
# if __name__ == '__main__':
#     app.run(debug=True)






