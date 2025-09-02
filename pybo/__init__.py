from flask import Flask, render_template, request, jsonify, redirect, url_for,Response
from flask_migrate import Migrate
from .models import db,User,Overseer,MonBoard,TueBoard,WedBoard,ThuBoard,FriBoard,SatBoard,SunBoard,Notice,DisabledSlot,DayNotice
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time
import json
import config
migrate = Migrate()


def clear_mon_board(app):
    with app.app_context():
        Notice.query.filter_by(slot="월1012").delete()
        Notice.query.filter_by(slot="월122").delete()
        Notice.query.filter_by(slot="월24").delete()
        db.session.commit()
        MonBoard.query.delete()
        DayNotice.query.delete()
        DisabledSlot.query.update({DisabledSlot.is_disabled: False})
        db.session.commit()

def clear_tue_board(app):
    with app.app_context():
        Notice.query.filter_by(slot="화1012").delete()
        Notice.query.filter_by(slot="화122").delete()
        Notice.query.filter_by(slot="화24").delete()
        Notice.query.filter_by(slot="화79").delete()
        db.session.commit()
        TueBoard.query.delete()
        DayNotice.query.delete()
        DisabledSlot.query.update({DisabledSlot.is_disabled: False})
        db.session.commit()

def clear_wed_board(app):
    with app.app_context():
        Notice.query.filter_by(slot="수1012").delete()
        Notice.query.filter_by(slot="수122").delete()
        Notice.query.filter_by(slot="수24").delete()
        db.session.commit()
        WedBoard.query.delete()
        DayNotice.query.delete()
        DisabledSlot.query.update({DisabledSlot.is_disabled: False})
        db.session.commit()

def clear_thu_board(app):
    with app.app_context():
        Notice.query.filter_by(slot="목1012").delete()
        Notice.query.filter_by(slot="목122").delete()
        Notice.query.filter_by(slot="목13_호별_").delete()
        Notice.query.filter_by(slot="목24").delete()
        Notice.query.filter_by(slot="목79").delete()
        db.session.commit()
        ThuBoard.query.delete()
        DayNotice.query.delete()
        DisabledSlot.query.update({DisabledSlot.is_disabled: False})
        db.session.commit()

def clear_fri_board(app):
    with app.app_context():
        Notice.query.filter_by(slot="금1012").delete()
        Notice.query.filter_by(slot="금122").delete()
        Notice.query.filter_by(slot="금24").delete()
        Notice.query.filter_by(slot="금13_호별_").delete()
        Notice.query.filter_by(slot="금79").delete()
        db.session.commit()
        FriBoard.query.delete()
        DayNotice.query.delete()
        DisabledSlot.query.update({DisabledSlot.is_disabled: False})
        db.session.commit()

def clear_sat_board(app):
    with app.app_context():
        Notice.query.filter_by(slot="토810").delete()
        Notice.query.filter_by(slot="토1012").delete()
        Notice.query.filter_by(slot="토122").delete()
        Notice.query.filter_by(slot="토13_호별_").delete()
        Notice.query.filter_by(slot="토24").delete()
        db.session.commit()
        SatBoard.query.delete()
        DayNotice.query.delete()
        DisabledSlot.query.update({DisabledSlot.is_disabled: False})
        db.session.commit()

def clear_sun_board(app):
    with app.app_context():
        Notice.query.filter_by(slot="일1반3시반").delete()
        Notice.query.filter_by(slot="일3반5시반").delete()
        Notice.query.filter_by(slot="일1012").delete()
        Notice.query.filter_by(slot="일122").delete()
        Notice.query.filter_by(slot="일24").delete()
        db.session.commit()
        SunBoard.query.delete()
        DayNotice.query.delete()
        DisabledSlot.query.update({DisabledSlot.is_disabled: False})
        db.session.commit()

def mark_divider(app, model, target_slots=None):
    with app.app_context():
        divider_user = User.query.filter_by(name='//').first()
        if not divider_user:
            print("⚠️ '//' user not found. Divider not inserted.")
            return

        for slot in target_slots or []:
            existing = model.query.filter_by(slot=slot, user_name='//').first()
            if not existing:
                divider = model(slot=slot, user_id=divider_user.id, user_name='//')
                db.session.add(divider)
        db.session.commit()

def mark_all_dividers(app):
    now = datetime.now()
    day = now.weekday()
    hour = now.hour
    minute = now.minute

    if day == 0:
        if hour == 9 and minute == 0:
            mark_divider(app, MonBoard, ["월1012"])
        if hour == 11 and minute == 0:
            mark_divider(app, MonBoard, ["월122"])
        if hour == 13 and minute == 0:
            mark_divider(app, MonBoard, ["월24"])

    if day == 1:
        if hour == 9 and minute == 0:
            mark_divider(app, TueBoard, ["화1012"])
        if hour == 11 and minute == 0:
            mark_divider(app, TueBoard, ["화122"])
        if hour == 13 and minute == 0:
            mark_divider(app, TueBoard, ["화24"])
        if hour == 18 and minute == 0:
            mark_divider(app, TueBoard, ["화79"])

    if day == 2:
        if hour == 9 and minute == 0:
            mark_divider(app, WedBoard, ["수1012"])
        if hour == 12 and minute == 0:
            mark_divider(app, WedBoard, ["수122"])
        if hour == 13 and minute == 0:
            mark_divider(app, WedBoard, ["수24"])

    if day == 3:
        if hour == 9 and minute == 0:
            mark_divider(app, ThuBoard, ["목1012"])
        if hour == 11 and minute == 0:
            mark_divider(app, ThuBoard, ["목122"])
        if hour == 12 and minute == 0:
            mark_divider(app, ThuBoard, ["목13_호별_"])
        if hour == 13 and minute == 0:
            mark_divider(app, ThuBoard, ["목24"])
        if hour == 18 and minute == 0:
            mark_divider(app, ThuBoard, ["목79"])

    if day == 4:
        if hour == 9 and minute == 0:
            mark_divider(app, FriBoard, ["금1012"])
        if hour == 11 and minute == 0:
            mark_divider(app, FriBoard, ["금122"])
        if hour == 12 and minute == 0:
            mark_divider(app, FriBoard, ["금13_호별_"])
        if hour == 13 and minute == 0:
            mark_divider(app, FriBoard, ["금24"])
        if hour == 18 and minute == 0:
            mark_divider(app, FriBoard, ["금79"])

    if day == 5:
        if hour == 7 and minute == 0:
            mark_divider(app, SatBoard, ["토810"])
        if hour == 9 and minute == 0:
            mark_divider(app, SatBoard, ["토1012"])
        if hour == 11 and minute == 0:
            mark_divider(app, SatBoard, ["토122"])
        if hour == 12 and minute == 0:
            mark_divider(app, SatBoard, ["토13_호별_"])
        if hour == 13 and minute == 0:
            mark_divider(app, SatBoard, ["토24"])

    if day == 6:
        if hour == 10 and minute == 0:
            mark_divider(app, SunBoard, ["일1012"])
        if hour == 12 and minute == 0:
            mark_divider(app, SunBoard, ["일122"])
        if hour == 14 and minute == 0:
            mark_divider(app, SunBoard, ["일24"])
        if hour == 12 and minute == 30:
            mark_divider(app, SunBoard, ["일1반3시반"])
        if hour == 14 and minute == 30:
            mark_divider(app, SunBoard, ["일3반5시반"])



# db = SQLAlchemy()


def create_app():
    app = Flask(__name__,static_url_path='/static')
    app.config.from_envvar('APP_CONFIG_FILE')

    #ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    #블루프린트
    from .views import main_views
    app.register_blueprint(main_views.bp)

    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: clear_mon_board(app), 'cron', day_of_week='mon', hour=23)
    scheduler.add_job(lambda: clear_tue_board(app), 'cron', day_of_week='tue', hour=23)
    scheduler.add_job(lambda: clear_wed_board(app), 'cron', day_of_week='wed', hour=23)
    scheduler.add_job(lambda: clear_thu_board(app), 'cron', day_of_week='thu', hour=23)
    scheduler.add_job(lambda: clear_fri_board(app), 'cron', day_of_week='fri', hour=23)
    scheduler.add_job(lambda: clear_sat_board(app), 'cron', day_of_week='sat', hour=23)
    scheduler.add_job(lambda: clear_sun_board(app), 'cron', day_of_week='sun', hour=23)
    scheduler.add_job(lambda: mark_all_dividers(app), 'cron', second='0')
    scheduler.start()

    if not hasattr(app, 'initialized'):
        app.initialized = True
        with app.app_context():
            db.create_all()
            initialize_users_and_overseers(app)

    return app

def initialize_users_and_overseers(app):
    with app.app_context():
        # 우선 divider 유저가 존재하는지 확인
        divider_user = User.query.filter_by(name='//').first()
        if not divider_user:
            divider_user = User(name='//')
            db.session.add(divider_user)
            db.session.commit()  # 먼저 커밋해서 DB에 반영

        # 나머지 유저 전부 삭제 (단, // 제외)
        all_users = User.query.all()
        for user in all_users:
            if user.name != '//':
                db.session.delete(user)
        db.session.commit()

        # overseer 삭제
        Overseer.query.delete()
        db.session.commit()

        users = ['김형민','강민성','김진숙','박봉임','박영수','서정현','성윤영','이은미','전재호','전지은','한주연','임정완','최소진',
                 '김경호','김진명','김귀덕','김미경','이예빛나','이윤남','이현숙','정병호','정우숙','차복순','최순남','최혜경',
                 '박정현','심지훈','권순자','김영길','모모코','박덕희','박홍숙','송현','이수림','전은희','한선욱','한성희','김지아',
                 '현승우','김경준','김연례','김재심','김진윤','김희숙','박원숙','이성재','최예진','하혜자','함성희','허수봉','허숙자',
                 '김동석','김서현','김수석','김영식','김은주','김원숙','김정현','김지현','노경임','이영주','임애경','김재호','조경옥','최병선',
                 '김양호','안승현','김재희','박말호','박종서','박혜인','양현미','장명희','장영숙','전상옥','정은실','조미선','최미례','문행숙','박시원','최현우',
                 '강신혜','문지원','최세욱','안병철','한순아','배소연','유수아','서정우','김누리','황미희','김민서']


        overseers =['김형민','전재호','김경호','김진명','박정현','심지훈','한성희','현승우','김경준','김진윤','이성재','김동석','김재호','정병호','김양호','안승현','박말호','최세욱','서정우','박종서']
        ov = [name + '인도' for name in overseers]

        for overseer in ov:
            u = Overseer(name = overseer)
            db.session.add(u)
            db.session.commit()

        allUsers = ov + users

        for user in allUsers:
            u = User(name = user)
            db.session.add(u)
            db.session.commit()
