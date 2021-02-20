from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #SQLAIchemy를 사용해 데이터베이스 저장

class UserInfo(db.Model):
    __tablename__ = 'userinfo'
    # no = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    phoneNumber = db.Column(db.String(50))
    address = db.Column(db.String(50))
    rrn = db.Column(db.String(50))

    # def __init__(self, id, name, pass
    #     self.name = name
    #     self.data = data
    #
    # def __repr__(self):
    #     return '<User %r>' % self.username

