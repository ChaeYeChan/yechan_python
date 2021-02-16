import time, os
from flask import Flask, render_template, request, _app_ctx_stack
from flask_restful import Api, reqparse, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import select
from models import db
from models import UserInfo
import sqlite3
# 수정수정

app = Flask('My First App')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1591@localhost/pythonlogin'

api = Api(app)

basedir = os.path.abspath(os.path.dirname(__file__))  # database 경로를 절대경로로 설정함
dbfile = os.path.join(basedir, 'db.sqlite')  # 데이터베이스 이름과 경로
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 사용자에게 원하는 정보를 전달완료했을때가 TEARDOWN, 그 순간마다 COMMIT을 하도록 한다.라는 설정
# 여러가지 쌓아져있던 동작들을 Commit을 해주어야 데이터베이스에 반영됨. 이러한 단위들은 트렌젝션이라고함.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # True하면 warrnig메시지 유발,




db.init_app(app)  # 초기화 후 db.app에 app으로 명시적으로 넣어줌
db.app = app
db.create_all()  # 이 명령이 있어야 생성됨. DB가


# 2차 수정입니다.


# https://net-study.club/entry/AWS-%EC%95%84%EB%A7%88%EC%A1%B4-%EC%9B%B9-%EC%84%9C%EB%B9%84%EC%8A%A4Amazon-Web-Service-%EA%B0%80%EC%9E%85-%EC%9D%B8%EC%A6%9D

# DATABASE = '/path/to/sqlite.db'
#
# def get_db():
#     top = _app_ctx_stack.top
#     if not hasattr(top, 'sqlite_db'):
#         top.sqlite_db = sqlite3.connect(DATABASE)
#     return top.sqlite_db


class User(Resource):
    def post(self):
        # 등록
        try:
            # global user
            parser = reqparse.RequestParser()
            parser.add_argument('id', required=True)
            parser.add_argument('name', required=True)
            parser.add_argument('password', required=True)

            args = parser.parse_args()
            userid = args['id']
            name = args['name']
            password = args['password']

            # no = request.form.get('no')
            # name = request.form.get('name')
            # password = request.form.get('password')
            fcuser = UserInfo()
            fcuser.id = userid
            fcuser.name = name
            fcuser.password = password  # models의 FCuser 클래스를 이용해 db에 입력한다.

            db.session.add(fcuser)
            db.session.commit()
            return {'result': 'ok'}


            # if user.get(id) == None:
            #     user[id] = {'name': name,
            #                   'password': password}
            #     fcuser = UserInfo()
            #     fcuser.password = password  # models의 FCuser 클래스를 이용해 db에 입력한다.
            #     fcuser.id = id
            #     fcuser.name = name
            #     db.session.add(fcuser)
            #     db.session.commit()
            #     return {'result' : 'ok'}
            # else:
            #     return {'result': 'Nok'}
        except Exception as e:
            return {'error': str(e)}


    def get(self):
        try:
            global user
            parser = reqparse.RequestParser()
            parser.add_argument('name', required=True)
            args = parser.parse_args()
            name =args['name']
            return_list = []
            for i in user:
                if name == user[i]['name']:
                    return_list.append({'id' : i})
            if len(return_list) > 0:
                return {'result' : 'ok', 'userids' : return_list}
            else:
                return {'result': 'Nok', 'reason': '등록된 사용자가 없습니다.'}
        except Exception as e:
            return {'error': str(e)}
    # def get(self):
    #         # 검색 찾기
    #     try:
    #        global user
    #        parser = reqparse.RequestParser()
    #        parser.add_argument('id', required=True)
    #        args = parser.parse_args()
    #
    #        id = args['id']
    #
    #        if user.get(id) == None:
    #            return {'result': 'Nok'}
    #        else:
    #
    #            return {'result': 'ok', 'userinfo' : user[id]}







    # def get(self):
    #         # 검색 찾기
    #     try:
    #        global user
    #        parser = reqparse.RequestParser()
    #        parser.add_argument('name', required=True)
    #        args = parser.parse_args()
    #
    #        name = args['name']
    #
    #
    #        return_list = []
    #        for i in user:
    #            if name == user[i]['name']:
    #                return_list.append(i)
    #        if len(return_list) > 0:
    #            return {'result' : 'ok', 'userids' : return_list}
    #        else:
    #            return {'result': 'Nok', 'reason': '등록된 사용자가 없습니다.'}
           #
           #
           # if user.get(name) == None:
           #     return {'result': 'Nok', 'reason' : '등록된 사용자가 없습니다.'}
           # else:
           #     return {'result': 'ok', 'user': user[id]}
           # else:
           #     name = args['name']
           #     # name = args.get('name')
           #     # get은 함수라 ()
           #     if user.get(name) == None:
           #         return {'result' : 'Nok', 'reason' : '해당 사용자가 없습니다.'}
           #     else:
           #        return {'result' : 'ok', 'userids' : user[name]}
        # except Exception as e:
        #     return {'error': str(e)}

    def put(self):
            # 수정
        global user
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', required=True)
            parser.add_argument('id', required=True)
            parser.add_argument('password', required=True)
            args = parser.parse_args()

            name = args['name']
            id = args['id']
            password = args['password']

            if user.get(id) == None:
                return {'result': 'Nok!'}
            else:
                user[id] = { 'name' : name,
                             'password' : password}
                return {'result': 'ok'}
        except Exception as e:
            return {'error': str(e)}

    def delete(self):
        global user
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', required=True)
            args = parser.parse_args()

            id = args['id']

            if user.get(id) == None:
                return {'result' : 'Nok'}
            else:
                del user[id]
                return {'result' : 'DELETE'}
        except Exception as e:
            return {'eroor': str(e)}

class UserAllList(Resource):
    def get(self):
        # 전체목록 출력
        global user
        try:
            # parser = reqparse.RequestParser()
            # parser.add_argument('name', required=True)
            # args = parser.parse_args()
            # userid = args['userid']
            # if memo_map.get(userid) == None:
            #     return {'result': 'Nok'}
            # else:

            return {'userlist' : user}
        except Exception as e:
            return {'error': str(e)}

class UserAllid(Resource):
    def get(self):
        # 전체ID 출력
        global user
        try:
            # parser = reqparse.RequestParser()
            # parser.add_argument('id', required=True)
            # args = parser.parse_args()
            # id = args['id']
            # name = args['name']
            #         return_list = []
            #         for i in user:
            #             if name == user[i]['name']:
            #                 return_list.append(i)
            #         if len(return_list) > 0:
            #             return {'result' : 'ok', 'userids' : return_list}
            #         else:
            #             return {'result': 'Nok', 'reason': '등록된 사용자가 없습니다.'}
            return_list = []
            for i in user:
                return_list.append({'id' : i})
            if len(return_list) > 0:
                return {'result' : 'ok', 'userid' : return_list}
            # return {'userid' : user[id]}
        except Exception as e:
            return {'error': str(e)}



class Userlist(Resource):
    def get(self):
            # 찾기
        try:
           global user_map
           parser = reqparse.RequestParser()
           parser.add_argument('name', required=False)
           args = parser.parse_args()
           if args.get('name') == None:
              if user_map == {}:
                  return {'result': 'Nok', 'reason' : '등록된 사용자가 없습니다.'}
              else:
                  return {'result': 'ok', 'userlist': user_map}
           else:
               name = args['name']
               # name = args.get('name')

               # get은 함수라 ()
               if user_map.get(name) == None:
                   return {'result' : 'Nok', 'reason' : '해당 사용자가 없습니다.'}
               else:
                  return {'result' : 'ok', 'userids' : user_map[name]}
        except Exception as e:
            return {'error': str(e)}


class MemoInfo(Resource):
    # def get(self):
    #     # 찾기
    #     global memo_map
    #     try:
    #         parser = reqparse.RequestParser()
    #         parser.add_argument('name', required=True)
    #         args = parser.parse_args()
    #         name = args['name']
    #         if memo_map.get(name) == None:
    #             return {'result' : 'Nok'}
    #         else:
    #             return {'result' : 'ok', 'content' : memo_map[name]}
    #     except Exception as e:
    #         return {'error': str(e)}

    def get(self):
            # 찾기
        global memo_map, user

        try:
              parser = reqparse.RequestParser()
              parser.add_argument('userid', required=True)
              parser.add_argument('memoid', required=True)
              args = parser.parse_args()
              userid = args['userid']
              memoid = args['memoid']

              if user.get(userid) == None:
                  return {'result': 'Nok', 'reason': '등록되지않은 사용자입니다.'}

              if memo_map.get(userid) == None:
                  return {'result': 'Nok'}
              else:
                  if (memo_map.get(userid)).get(memoid) == None:
                      return {'result': 'Nok'}
                  else:
                      return {'result': 'ok', 'memo': memo_map[userid][memoid]}
        except Exception as e:
            return {'error': str(e)}

    # def get(self):
    #     # 찾기
    #     global memo_map
    #     try:
    #         parser = reqparse.RequestParser()
    #         parser.add_argument('id', required=True)
    #         args = parser.parse_args()
    #         id = args['id']
    #         print("id :", id)
    #         if memo_map.get(id) == None:
    #             return {'result': 'Nok'}
    #         else:
    #             return {'result': 'ok', 'content': memo_map[id]}
    #     except Exception as e:
    #         return {'error': str(e)}

    def post(self):
        # 저장
        global memo_map, user
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('userid', required=True)
            parser.add_argument('memo', required=True)
            args = parser.parse_args()
            userid = args['userid']
            memo = args['memo']
            if user.get(userid) == None:
                return {'result': 'Nok', 'reason': '등록되지않은 사용자입니다.'}

            memoid = str(time.time())
            if memo_map.get(userid) == None:
                memo_map[userid] = {memoid : memo}
            else:
                memo_map[userid].update({memoid : memo})
            return {'result': 'ok', 'memoid' : memoid}
        except Exception as e:
            return {'error': str(e)}

    def put(self):
            # 수정
        global memo_map, user
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('userid', required=True)
            parser.add_argument('memoid', required=True)
            parser.add_argument('memo', required=True)
            args = parser.parse_args()

            userid = args['userid']
            memoid = args['memoid']
            memo = args['memo']

            if user.get(userid) == None:
                return {'result': 'Nok', 'reason': '등록되지않은 사용자입니다.'}

            if memo_map.get(userid) == None:
                return {'result': 'Nok!'}
            else:
                if (memo_map.get(userid)).get(memoid) == None:
                    return {'result': 'Nok'}
                else:
                    (memo_map[userid])[memoid] = memo
                    return {'result': 'ok'}
        except Exception as e:
            return {'error': str(e)}

        # def post(self):
        #     # 저장
        #     global memo_map
        #     try:
        #         parser = reqparse.RequestParser()
        #         parser.add_argument('name', required=True)
        #         parser.add_argument('memo', required=True)
        #         args = parser.parse_args()
        #         name = args['name']
        #         memo = args['memo']
        #
        #         memo_map[str(time.time())] = {name: memo}
        #         return {'result': 'ok'}
        #     except Exception as e:
        #         return {'error': str(e)}
    def put(self):
        # 수정
        global memo_map, user
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('userid', required=True)
            parser.add_argument('memoid', required=True)
            parser.add_argument('memo', required=True)
            args = parser.parse_args()

            userid = args['userid']
            memoid = args['memoid']
            memo = args['memo']

            if memo_map.get(userid) == None:
                return {'result' : 'Nok!'}
            else:
                if (memo_map.get(userid)).get(memoid) == None:
                    return {'result': 'Nok'}
                else:
                    (memo_map[userid])[memoid] = memo
                return {'result' : 'ok'}
        except Exception as e:
            return {'error': str(e)}

        # def put(self):
        #     # 수정
        #     global memo_map
        #     try:
        #         parser = reqparse.RequestParser()
        #         parser.add_argument('name', required=True)
        #         parser.add_argument('memo', required=True)
        #         parser.add_argument('id', required=True)
        #         args = parser.parse_args()
        #
        #         id = args['id']
        #         name = args['name']
        #         memo = args['memo']
        #
        #         if memo_map.get(id) == None:
        #             return {'result': 'Nok'}
        #         else:
        #             memo_map[id] = {name: memo}
        #             return {'result': 'ok'}
        #     except Exception as e:
        #         return {'error': str(e)}
    def delete(self):
        global memo_map
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', required=True)
            args = parser.parse_args()
            name = args['name']
            if memo_map.get(name) == None:
                return {'result' : 'Nok'}
            else:
                del memo_map[name]
                return {'result' : 'ok'}
        except Exception as e:
            return {'error': str(e)}

class MemoList(Resource):
    def get(self):
        global memo_map
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('userid', required=True)
            args = parser.parse_args()
            userid = args['userid']
            if memo_map.get(userid) == None:
                return {'result': 'Nok'}
            else:
                return {'result': 'ok', 'memolist' : memo_map.get(userid)}
        except Exception as e:
            return {'error': str(e)}



api.add_resource(MemoInfo, '/memo')
api.add_resource(MemoList, '/memolist')
api.add_resource(Userlist, '/userlist')
api.add_resource(User, '/user')
api.add_resource(UserAllList, '/useralllist')
api.add_resource(UserAllid, '/useridlist')

a = []
b = {}

memo_map = {
             'userid1' : {'memoid1' : 'MemoContent1',
                           'memoid2' : 'MemoContent2',
                           'memoid3' : 'MemoContent3'},
             'userid2' : {'memoid4' : 'MemoContent4'},
             'userid3' : {'memoid5' : 'MemoContent5',
                           'memoid6' : 'MemoContent6'},
           }

user_map = {
             'name#1' : [ 'userid1', 'userid2' ],
             'name#2' : [ 'userid3']
           }

user = {
        'chae971012'  : { 'name' : 'yechan',
                      'password' : '1234'},
        'balloo150' : { 'name' : 'yechan',
                      'password' : '4321'},
        'balloony' : { 'name' : 'yechan2',
                      'password' : '1234566'}
       }

# memo_map = {}


@app.route('/')
def hello_pybo():
    return render_template('main.html', phone_length=len(b), phone_list=b)

@app.route('/add')
def add_pybo():
    return render_template('add.html')

@app.route('/addinfo', methods=['POST'])
def addinfo_pybo():
    name = request.form['name']
    phone_number = request.form['number']
    if b.get(phone_number) == None:
        b[phone_number] = name
        return '등록 성공!'
    else:
        return '이미 등록된 번호..'

@app.route('/showinfo')
def showinfo_pybo():
    return render_template('showinfo.html',  phone_length=len(b), phone_list=b)

@app.route('/search')
def search_pybo():
    return render_template('search.html')

@app.route('/searchinfo', methods=['POST'])
def searchinfo_pybo():
    phone_number = request.form['number']
    if b.get(phone_number) == None:
        return '없는 번호야'
    else:
        return b[phone_number]


@app.route('/register')
def register_pybo():
    return render_template('register.html')

@app.route('/delete')
def delete_pybo():
    return render_template('delete.html')

@app.route('/delphoneinfo', methods=['POST'])
def delphoneinfo_pybo():
    phone_number = request.form['number']
    if b.get(phone_number) == None:
        return '없는 번호 입니다..'
    else:
        del b[phone_number]
        return '삭제 성공!.'

@app.route('/update')
def update_pybo():
    return render_template('update.html')

@app.route('/updatephoneinfo', methods=['POST'])
def updatephoneinfo_pybo():
    phone_number = request.form['number']
    name = request.form['name']
    if b.get(phone_number) == None:
        return '없는 번호입니다.'
    else:
        b[phone_number] = name
        return '업데이트 수정 성공!!'

if __name__ == "__main__":

    app.run(debug=True)