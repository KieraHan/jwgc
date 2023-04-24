# models.py
from pybo import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

class User(db.Model):
    #데이터의 고유번호
    id = db.Column(db.Integer, primary_key=True)
    #회원이름
    name = db.Column(db.String(5), nullable=False)
    
class Overseer(db.Model):
    #데이터의 고유번호
    id = db.Column(db.Integer, primary_key=True)
    #회원이름
    name = db.Column(db.String(5), nullable=False)


# 요일별신청자데이터
class TueBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.String(5), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user_name = db.Column(db.String(50), nullable=False)  # user_name 필드 추가
    user = relationship("User", backref=db.backref('tue_board', lazy=True))
class ThuBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.String(5), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user_name = db.Column(db.String(50), nullable=False)  # user_name 필드 추가
    user = relationship("User", backref=db.backref('thu_board', lazy=True))
class SatBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.String(5), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user_name = db.Column(db.String(50), nullable=False)  # user_name 필드 추가
    user = relationship("User", backref=db.backref('sat_board', lazy=True))
class SunBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.String(5), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user_name = db.Column(db.String(50), nullable=False)  # user_name 필드 추가
    user = relationship("User", backref=db.backref('sun_board', lazy=True))

#슬롯비활성화
class DisabledSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot_id = db.Column(db.String(20), nullable=False, unique=True)
    is_disabled = db.Column(db.Boolean, nullable=False, default=False)

#공지
class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    slot = db.Column(db.String(20), nullable=False)

