from flask import Flask, render_template, request, jsonify, redirect, url_for,Response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import json
import config

db = SQLAlchemy()
migrate = Migrate()


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

    if __name__ == '__main__':
        app.run(debug=True)

    return app




    #
    # # db.init_app(app)
    # #
    # # with app.app_context():
    # #     db.create_all()
    # #
    # #     from . import models
    # #
    # #     table_data = {'10~12시': [], '12~2시': [], '2~4시': []}
    # #     members = ['전재호', '한선욱', '권순자', '송현', '한성희']
    # #
    # #     for name in members:
    # #         new_user = models.User(name=name)
    # #         db.session.add(new_user)
    # #     db.session.commit()
    # #
    # #     all_users = models.User.query.all()
    # #     for user in all_users:
    # #         print(f'User ID: {user.id}, Name: {user.name}')
    #
    #
    # @app.route('/', methods=['GET', 'POST'])
    # def index():
    #     if request.method == 'POST':
    #         username = request.form['username']
    #         if username in members:
    #             return redirect(url_for('calendar', username=username))
    #         else:
    #             return render_template('index.html', error="회원이 아닙니다.")
    #     return render_template('index.html')
    #
    # # @app.route('/calendar/<username>')
    # # def calendar(username):
    # #     global table_data
    # #     return render_template('calendar2.html', username=username)
    #
    #
    # @app.route('/calendar/<username>')
    # def calendar(username):
    #     global table_data
    #     return render_template('calendar2.html', username=username, table_data=table_data)
    #
    #
    # @app.route('/booking/<username>')
    # def booking(username):
    #     global table_data
    #     return render_template('booking8.html', username=username,table_data=table_data)
    #
    # @app.route('/apply', methods=['POST'])
    # def apply():
    #     #개인이 칸에 신청하는 경우
    #     # global table_data
    #     # cell_id = request.form['cell_id']
    #     # username = request.form['username']
    #     # action = request.form['action']
    #     #
    #     # if action == 'apply':
    #     #     if cell_id in table_data and table_data[cell_id] is not None:
    #     #         return jsonify(success=False, message="이미 신청된 셀입니다.")
    #     #     table_data[cell_id] = username
    #     # elif action == 'cancel':
    #     #     table_data.pop(cell_id, None)
    #     #
    #     # return jsonify(success=True)
    #     global table_data
    #     board = request.form['board']
    #     username = request.form['username']
    #     action = request.form['action']
    #
    #     if action == 'apply':
    #         if len(table_data[board]) >= 30:
    #             return jsonify(success=False, message="이미 꽉 찬 게시판입니다.")
    #         else:
    #             table_data[board].append(username)
    #     elif action == 'cancel':
    #         table_data[board].remove(username)
    #
    #     return jsonify(success=True)
    #
    # @app.route('/get_table_data', methods=['GET'])
    # def get_table_data():
    #     return jsonify(table_data)
    #
    # @app.route('/reset', methods=['POST'])
    # def reset():
    #     global table_data
    #     table_data = {
    #         "10~12시": [],
    #         "12~2시": [],
    #         "2~4시": [],
    #     }
    #     return jsonify(success=True)
    #
    # @app.route('/board_data', methods=['GET'])
    # def board_data():
    #     board = request.args.get('board')
    #     names = table_data[board]
    #     return jsonify(names=names)
    #
    # @app.route('/notice', methods=['POST'])
    # def post_notice():
    #     board = request.form.get('board')
    #     notice = request.form.get('notice')
    #     if not notice:
    #         return jsonify({'success': False, 'message': '게시판과 공지 내용을 모두 입력해주세요.'}), 400
    #
    #     # 공지를 저장하거나, 데이터베이스에 저장하는 등의 로직 수행
    #
    #     return jsonify({'success': True})
    #

    # if __name__ == '__main__':
    #     app.run(debug=True)
    #
    # return app
