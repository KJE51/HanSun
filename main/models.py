from main import db

#유저 : 아이디(이메일)/비밀번호/남은 무료/남은 유료

class User(db.Model):
    email = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)
    freeNum = db.Column(db.Integer, default = 3)
    payNum = db.Column(db.Integer, default = 0)

