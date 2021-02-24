import time, os
from flask import Flask, render_template, request, _app_ctx_stack, session, url_for, redirect
from flask_restful import Api, reqparse, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import select

from models import db
from models import UserInfo
import sqlite3

app = Flask('My First App')
api = Api(app)

#현재있는 파일의 디렉토리 절대경로
basdir = os.path.abspath(os.path.dirname(__file__))
# basdir 경로안에 DB파일 만들기
dbfile = os.path.join(basdir, 'db.sqlite')
#SQLAlchemy 설정
#내가 사용할 DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
# 비지니스 로직이 끝날때 Commit 실행(DB반영)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#수정사항에 대한 TRACK
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# #SECRET_KEY
# app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'


# basedir = os.path.abspath(os.path.dirname(__file__))  # database 경로를 절대경로로 설정함
# dbfile = os.path.join(basedir, 'db.sqlite')  # 데이터베이스 이름과 경로
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 사용자에게 원하는 정보를 전달완료했을때가 TEARDOWN, 그 순간마다 COMMIT을 하도록 한다.라는 설정
# # 여러가지 쌓아져있던 동작들을 Commit을 해주어야 데이터베이스에 반영됨. 이러한 단위들은 트렌젝션이라고함.
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # True하면 warrnig메시지 유발,


db.init_app(app) #초기화 후 db.app에 app으로 명시적으로 넣어줌
db.app = app
db.create_all() # 이 명령이 있어야 db가 생성됨


# @app.route('/', methods=['GET', 'POST'])
# def home():
# 	""" Session control"""
# 	if not session.get('logged_in'):
# 		return {'result': 'nok'}
# 	else:
# 		if request.method == 'POST':
# 			username = getname(request.form['username'])
# 			return render_template('index.html', data=getfollowedby(username))
# 		return render_template('index.html')




class User(Resource):
    def post(self):
        try:
            print('start')
            parser = reqparse.RequestParser()
            parser.add_argument('id', required=True)
            parser.add_argument('name', required=True)
            parser.add_argument('password', required=True)
            parser.add_argument('phonenumber', required=True)
            parser.add_argument('address', required=True)
            parser.add_argument('rrn', required=True)

            args = parser.parse_args()
            userid = args['id']
            name = args['name']
            password = args['password']
            phoneNumber = args['phonenumber']
            address = args['address']
            rrn = args['rrn']

            print(id)
            fcuser = UserInfo()
            fcuser.id = userid
            fcuser.name = name
            fcuser.password = password
            fcuser.phoneNumber = phoneNumber
            fcuser.address = address
            fcuser.rrn = rrn

            print(id)
            db.session.add(fcuser)
            print(id)
            db.session.commit()
            print('end')
            return {'result' : 'ok'}
        except Exception as e:
            return {'error': str(e)}

    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', required=True)
            parser.add_argument('id', required=True)
            parser.add_argument('password', required=True)
            parser.add_argument('newpassword', required=True)
            args = parser.parse_args()
            name = args['name']
            user_id = args['id']
            password = args['password']
            new_password = args['newpassword']

            query_user = UserInfo.query.filter_by(id=user_id).first()
            if query_user == None:
                return {'result': 'Nok', 'reason': '미등록id입니다.'}
            if name != query_user.name:
                return {'result': 'Nok', 'reason': '이름이 id와 일치하지않습니다.'}
            if password == query_user.password:
                query_user.password = new_password
                db.session.commit()
                return {'result': 'ok'}
            else:
                return {'result': 'Nok', 'reason': 'password가 불일치 합니다.'}
        except Exception as e:
            return {'error': str(e)}

    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', required=True)
            parser.add_argument('password', required=True)
            args = parser.parse_args()
            id = args['id']
            password = args['password']

            query_user = UserInfo.query.filter_by(id=id).first()

            if query_user == None:
                return {'result' : 'Nok', 'reason' : '미등록 id입니다.' }
            if password == query_user.password:
                db.session.delete(query_user)
                db.session.commit()
                return {'result': 'ok'}
            else:
                return {'result' : 'Nok', 'reason' : 'password가 불일치 합니다.'}
        except Exception as e:
            return {'error' : str(e)}

class SearchId(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', required=True)
            parser.add_argument('rrn', required=True)
            args = parser.parse_args()
            input_name = args['name']
            input_rrn = args['rrn']

            query_user = UserInfo.query.filter_by(rrn=input_rrn).first()

            if query_user == None:
                return {'result' : 'Nok', 'reason': '미등록 사용자 입니다.'}
            if input_name == query_user.name:
                return {'result': 'ok', 'id': query_user.id}
            else:
                return {'result': 'Nok', 'reason': '주민번호와 이름이 일치하지않음'}
        except Exception as e:
            return {'error': str(e)}

class SearchPassword(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', required=True)
            parser.add_argument('rrn', required=True)
            args = parser.parse_args()
            input_id = args['id']
            input_rrn = args['rrn']

            query_user = UserInfo.query.filter_by(rrn=input_rrn).first()

            if query_user == None:
                return {'result' : 'Nok', 'reason': '미등록 사용자 입니다.'}
            if input_id == query_user.id:
                return {'result': 'ok', 'id': query_user.password}
            else:
                return {'result': 'Nok', 'reason': '주민번호와 이름이 일치하지않음'}
        except Exception as e:
            return {'error': str(e)}

# class UserAllList(Resource):
#     def get(self):
#         try:
#             print('start')
#             print(UserInfo)
#             query_user = UserInfo.query.filter_by(id=id).first()
#             print('mid')
#
#             return {'UserInfo' : query_user.query.all()}
#             print('end')
#         except Exception as e:
#             return {'error': str(e)}

# class login(Resource):
#     def get(self):
#         try:
#             print('1')
#             parser = reqparse.RequestParser()
#             parser.add_argument('id', required=True)
#             parser.add_argument('password', required=True)
#             args = parser.parse_args()
#             id = args['id']
#             password = args['password']
#             print('2')
#             data = UserInfo.query.filter_by(id=id, password=password).first()
#             print('3')
#             if data is not None:
#                 db.session['logged_in'] = True
#                 print('4')
#                 return {'ok'}
#
#
#         except Exception as e:
#             return {'error' : str(e)}

class login(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', required=True)
            parser.add_argument('password', required=True)
            args = parser.parse_args()
            id = args['id']
            password = args['password']

            query_user = UserInfo.query.filter_by(id=id).first()

            if query_user == None:
                return {'result' : 'Nok', 'reason' : '미등록 id입니다.' }
            if password == query_user.password:
                query_user.login = 'True'
                db.session.commit()
                return {'result': 'ok', 'login' : query_user.login}
            else:
                return {'result' : 'Nok', 'reason' : 'password가 불일치 합니다.'}
        except Exception as e:
            return {'error' : str(e)}

class logout(Resource):
    def get(self):
        try:
            # query_user = UserInfo.query.filter_by(id=id).first()
            UserInfo.login = 'False'
            db.session.commit()
            return {'result': 'ok', 'login' : UserInfo.login}
        except Exception as e:
            return {'error' : str(e)}


@app.route('/')
def hello_pybo():
    return render_template('main.html')





api.add_resource(User, '/user')
# api.add_resource(UserAllList, '/useralllist')
api.add_resource(SearchId, '/searchid')
api.add_resource(SearchPassword, '/searchpassword')
api.add_resource(login, '/login')
api.add_resource(logout, '/logout')

app.secret_key = "super secret key"
app.config['SESSION_TYPE'] = 'filesystem'


if __name__ == "__main__":
    app.run(debug=True)



