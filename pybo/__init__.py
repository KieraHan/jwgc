from flask import Flask, render_template, request, jsonify, redirect, url_for,Response
from flask_migrate import Migrate
from .models import db,User,Overseer,TueBoard,ThuBoard,SatBoard,SunBoard
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time
import json
import config
migrate = Migrate()

def clear_tue_board(app):
    with app.app_context():
        TueBoard.query.delete()
        db.session.commit()

def clear_thu_board(app):
    with app.app_context():
        ThuBoard.query.delete()
        db.session.commit()

def clear_sat_board(app):
    with app.app_context():
        SatBoard.query.delete()
        db.session.commit()
def clear_sun_board(app):
    with app.app_context():
        SunBoard.query.delete()
        db.session.commit()


# db = SQLAlchemy()


def create_app():
    app = Flask(__name__,static_url_path='/static')
    app.config.from_object(config)

    #ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    #블루프린트
    from .views import main_views
    app.register_blueprint(main_views.bp)

    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: clear_tue_board(app), 'cron', day_of_week='tue', hour=23)
    scheduler.add_job(lambda: clear_thu_board(app), 'cron', day_of_week='thu', hour=23)
    scheduler.add_job(lambda: clear_sat_board(app), 'cron', day_of_week='sat', hour=23)
    scheduler.add_job(lambda: clear_sun_board(app), 'cron', day_of_week='sun', hour=23)
    scheduler.start()

    if not hasattr(app, 'initialized'):
        app.initialized = True
        with app.app_context():
            db.create_all()
            initialize_users_and_overseers(app)

    return app

def initialize_users_and_overseers(app):
    with app.app_context():
        alluser = User.query.all()
        for user in alluser:
            db.session.delete(user)
        db.session.commit()
        alloverseer = Overseer.query.all()
        for overseer in alloverseer:
            db.session.delete(overseer)
        db.session.commit()

        users = ['김형민','김진부','강민성','김내오','김지오','김진숙','남선영','박봉임','박영수','서정현','성윤영','이은미','전재호','전지은','한주연','임정완','최소진',
                 '김경호','김진명','김귀덕','김미경','이예빛나','이윤남','이해안','이현숙','전봉순','정병호','정우숙','차복순','최순남','최혜경','최혜선',
                 '박정현','심지훈','권순자','김민교','김영길','나래','모모코','박덕희','박홍숙','송현','이수림','이재욱','전은희','한선욱','한성희',
                 '현승우','김경준','김연례','김재심','김진윤','김희숙','박원숙','박정숙','이성재','이효선','최예진','하혜자','함성희','허수봉','허숙자',
                 '김동석','이춘배','계현숙','김서현','김수석','김영식','김은주','김원숙','김정현','김지현','김진형','노경임','이영주','임애경','김재호','조경옥','최병선',
                 '김양호','안승현','김재희','박말호','박종서','박혜인','양현미','이혜경','임응진','장명희','장영숙','전상옥','정은실','조미선','최미례']

        for user in users:
            u = User(name = user)
            db.session.add(u)
            db.session.commit()

        overseers =['김형민','이춘배','전재호','김경호','김진명','박정현','심지훈','한성희','현승우','김경준','김진윤','이성재','김동석','정병호','김양호','안승현','박말호']

        for overseer in overseers:
            u = Overseer(name = overseer)
            db.session.add(u)
            db.session.commit()
