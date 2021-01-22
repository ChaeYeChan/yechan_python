from flask import Flask, render_template, request
from flask_restful import Resource, reqparse, Api

# 안녕하세요 테스트용입니다.
# ㅎㅎㅎㅎㅎ

# https://net-study.club/entry/AWS-%EC%95%84%EB%A7%88%EC%A1%B4-%EC%9B%B9-%EC%84%9C%EB%B9%84%EC%8A%A4Amazon-Web-Service-%EA%B0%80%EC%9E%85-%EC%9D%B8%EC%A6%9D

# tvOnFlag = False

# class TvOn(Resource):
#     def get(self):
#         try:
#             global tvOnFlag
#             tvOnFlag = True
#             return {'result': 'tv in on now'}
#         except Exception as e:
#             return {'error': str(e)}
#
# class TvOff(Resource):
#     def get(self):
#         try:
#             global tvOnFlag
#             tvOnFlag = False
#             return {'result': 'tv os off now'}
#         except Exception as e:
#             return {'error': str(e)}










app = Flask('My First App')
api = Api(app)

# api.add_resource(TvOn, '/tv/on')
# api.add_resource(TvOff, '/tv/off')

a = []
b = {}

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


    # @app.route('/delphoneinfo', methods=['POST'])
    # def delphoneinfo_pybo():
    #     phone_number = request.form['number']
    #     if b.get(phone_number) == None:
    #         return '없는 번호 입니다..'
    #     else:
    #         del b[phone_number]
    #         return '삭제 성공!.'

# return b[phone_number]


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





app.run(debug=True)