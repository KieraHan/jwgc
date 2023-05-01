from flask import Blueprint
from flask import Flask, render_template, request, jsonify, redirect, url_for,Response
import json
from pybo import db
from pybo.models import User,Overseer,TueBoard,ThuBoard,SatBoard,SunBoard,DisabledSlot,Notice,DayNotice

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        username = request.form['username']
        user_list = User.query.filter_by(name=username).first()
        if user_list:
            return redirect(url_for('main.show', username=username))
        else:
            return render_template('index1.html', error="회원이 아닙니다.")
    return render_template('index1.html')
@bp.route('/<username>')
def show(username):
    return render_template('gygc_booking.html', username=username)

@bp.route('/apply', methods=['POST'])
def apply():
    username = request.form['username']
    slot = request.form['slot']
    day = request.form['day']
    slot_name = request.form['slot_name']  # 추가된 부분

    user = User.query.filter_by(name=username).first()
    if not user:
        return jsonify({"error": "회원이 아닙니다."}), 400

    #선택된 요일에 따라 슬롯의 개수가 다름.
    if day == '화':
        existing_applicant = TueBoard.query.filter_by(slot=slot_name,user_id=user.id).first()  # 수정된 부분
        print(existing_applicant)
        if existing_applicant:
            return jsonify({"error": "이미 해당 시간대에 신청하셨습니다."}), 400

        day_slot =  ["10~12시", "12~2시", "2~4시", "7~9시"]
        #화요일에 해당하는 모델에 신청자를 추가한다.
        board = TueBoard(slot=slot, user_id=user.id, user_name=user.name)
        print(board)
        db.session.add(board)
        db.session.commit()
        # 해당 요일의 모든 신청자 목록을 가져옵니다.
        applicants = TueBoard.query.filter_by(slot="10~12시").all()
        names1 = [applicant.user.name for applicant in applicants]
        applicants = TueBoard.query.filter_by(slot="12~2시").all()
        names2 = [applicant.user.name for applicant in applicants]
        applicants = TueBoard.query.filter_by(slot="2~4시").all()
        names3 = [applicant.user.name for applicant in applicants]
        applicants = TueBoard.query.filter_by(slot="7~9시").all()
        names4 = [applicant.user.name for applicant in applicants]
        return jsonify({"message": "신청이 완료되었습니다.", "names1": names1,"names2": names2,"names3": names3,"names4": names4}), 200
    elif day =='목':
        existing_applicant = ThuBoard.query.filter_by(slot=slot_name, user_id=user.id).first()  # 수정된 부분
        if existing_applicant:
            return jsonify({"error": "이미 해당 시간대에 신청하셨습니다."}), 400

        day_slot =["12~2시", "2~4시", "7~9시"]
        board = ThuBoard(slot=slot, user_id=user.id, user_name=user.name)
        db.session.add(board)
        db.session.commit()

        applicants = ThuBoard.query.filter_by(slot="12~2시").all()
        names1 = [applicant.user.name for applicant in applicants]
        applicants = ThuBoard.query.filter_by(slot="2~4시").all()
        names2 = [applicant.user.name for applicant in applicants]
        applicants = ThuBoard.query.filter_by(slot="7~9시").all()
        names3 = [applicant.user.name for applicant in applicants]
        return jsonify({"message": "신청이 완료되었습니다.", "names1": names1, "names2": names2, "names3": names3}), 200

    elif day == '토':
        existing_applicant = SatBoard.query.filter_by(slot=slot_name, user_id=user.id).first()  # 수정된 부분
        if existing_applicant:
            return jsonify({"error": "이미 해당 시간대에 신청하셨습니다."}), 400

        day_slot = ["10~12시(웨돔)","10~12시(마두)","12~2시(마두)","2~4시(마두)"]
        board = SatBoard(slot=slot, user_id=user.id, user_name=user.name)
        db.session.add(board)
        db.session.commit()

        applicants = SatBoard.query.filter_by(slot="10~12시(웨돔)").all()
        names1 = [applicant.user.name for applicant in applicants]
        applicants = SatBoard.query.filter_by(slot="10~12시(마두)").all()
        names2 = [applicant.user.name for applicant in applicants]
        applicants = SatBoard.query.filter_by(slot="12~2시(마두)").all()
        names3 = [applicant.user.name for applicant in applicants]
        applicants = SatBoard.query.filter_by(slot="2~4시(마두)").all()
        names4 = [applicant.user.name for applicant in applicants]
        return jsonify({"message": "신청이 완료되었습니다.", "names1": names1, "names2": names2, "names3": names3,"names4": names4}), 200

    elif day == '일':
        existing_applicant = SunBoard.query.filter_by(slot=slot_name, user_id=user.id).first()  # 수정된 부분
        if existing_applicant:
            return jsonify({"error": "이미 해당 시간대에 신청하셨습니다."}), 400
        day_slot = ["1:30~3:30"]
        board = SunBoard(slot=slot, user_id=user.id, user_name=user.name)
        db.session.add(board)
        db.session.commit()

        applicants = SunBoard.query.filter_by(slot="1:30~3:30").all()
        names1 = [applicant.user.name for applicant in applicants]
        return jsonify({"message": "신청이 완료되었습니다.", "names1": names1}), 200


# @bp.route('/get_applicants', methods=['POST'])
# def get_applicants():능
#     slot = request.form.get('slot')
#     applicants = TueBoard.query.filter_by(slot=slot).all()
#     names = [applicant.username for applicant in applicants]
#     return jsonify({'names': names})

@bp.route('/update', methods=['POST'])
def update():
    username = request.form['username']
    day = request.form['day']

    if day == '화':
        # 해당 요일의 모든 신청자 목록을 가져옵니다.
        applicants = TueBoard.query.filter_by(slot="10~12시").all()
        names1 = [applicant.user.name for applicant in applicants]
        applicants = TueBoard.query.filter_by(slot="12~2시").all()
        names2 = [applicant.user.name for applicant in applicants]
        applicants = TueBoard.query.filter_by(slot="2~4시").all()
        names3 = [applicant.user.name for applicant in applicants]
        applicants = TueBoard.query.filter_by(slot="7~9시").all()
        names4 = [applicant.user.name for applicant in applicants]
        return jsonify({"message": "화요일 신청자명단 업데이트","names1": names1,"names2": names2,"names3": names3,"names4": names4}), 200
    elif day =='목':
        applicants = ThuBoard.query.filter_by(slot="12~2시").all()
        names1 = [applicant.user.name for applicant in applicants]
        applicants = ThuBoard.query.filter_by(slot="2~4시").all()
        names2 = [applicant.user.name for applicant in applicants]
        applicants = ThuBoard.query.filter_by(slot="7~9시").all()
        names3 = [applicant.user.name for applicant in applicants]
        return jsonify({"message": "화요일 신청자명단 업데이트","names1": names1,"names2": names2,"names3": names3}), 200
    elif day == '토':
        applicants = SatBoard.query.filter_by(slot="10~12시(웨돔)").all()
        names1 = [applicant.user.name for applicant in applicants]
        applicants = SatBoard.query.filter_by(slot="10~12시(마두)").all()
        names2 = [applicant.user.name for applicant in applicants]
        applicants = SatBoard.query.filter_by(slot="12~2시(마두)").all()
        names3 = [applicant.user.name for applicant in applicants]
        applicants = SatBoard.query.filter_by(slot="2~4시(마두)").all()
        names4 = [applicant.user.name for applicant in applicants]
        return jsonify({"message": "화요일 신청자명단 업데이트","names1": names1,"names2": names2,"names3": names3,"names4": names4}), 200
    elif day == '일':
        applicants = SunBoard.query.filter_by(slot="1:30~3:30").all()
        names1 = [applicant.user.name for applicant in applicants]
        return jsonify({"message": "화요일 신청자명단 업데이트","names1": names1}), 200


@bp.route('/cancel', methods=['POST'])
def cancel():
    username = request.form['username']
    slot_name = request.form['slot_name']
    day = request.form['day']

    user = User.query.filter_by(name=username).first()
    if not user:
        return jsonify({"error": "회원이 아닙니다."}), 400

    # 취소할 신청을 찾습니다.
    if day == "화":
        application_to_cancel = TueBoard.query.filter_by(user_id=user.id, slot=slot_name).first()
        if application_to_cancel:
            db.session.delete(application_to_cancel)
            db.session.commit()

            applicants = TueBoard.query.filter_by(slot="10~12시").all()
            names1 = [applicant.user.name for applicant in applicants]
            applicants = TueBoard.query.filter_by(slot="12~2시").all()
            names2 = [applicant.user.name for applicant in applicants]
            applicants = TueBoard.query.filter_by(slot="2~4시").all()
            names3 = [applicant.user.name for applicant in applicants]
            applicants = TueBoard.query.filter_by(slot="7~9시").all()
            names4 = [applicant.user.name for applicant in applicants]

            return jsonify({"message": "신청이 취소되었습니다." ,"names1": names1,"names2": names2,"names3": names3,"names4": names4}), 200
        else:
            return jsonify({"error": "신청을 찾을 수 없습니다."}), 400
    elif day == "목":
        application_to_cancel = ThuBoard.query.filter_by(user_id=user.id, slot=slot_name).first()
        if application_to_cancel:
            db.session.delete(application_to_cancel)
            db.session.commit()

            applicants = ThuBoard.query.filter_by(slot="12~2시").all()
            names1 = [applicant.user.name for applicant in applicants]
            applicants = ThuBoard.query.filter_by(slot="2~4시").all()
            names2 = [applicant.user.name for applicant in applicants]
            applicants = ThuBoard.query.filter_by(slot="7~9시").all()
            names3 = [applicant.user.name for applicant in applicants]
            return jsonify({"message": "신청이 취소되었습니다.", "names1": names1, "names2": names2, "names3": names3}), 200

        else:
            return jsonify({"error": "신청을 찾을 수 없습니다."}), 400

    elif day == "토":
        application_to_cancel = SatBoard.query.filter_by(user_id=user.id, slot=slot_name).first()
        if application_to_cancel:
            db.session.delete(application_to_cancel)
            db.session.commit()

            applicants = SatBoard.query.filter_by(slot="10~12시(웨돔)").all()
            names1 = [applicant.user.name for applicant in applicants]
            applicants = SatBoard.query.filter_by(slot="10~12시(마두)").all()
            names2 = [applicant.user.name for applicant in applicants]
            applicants = SatBoard.query.filter_by(slot="12~2시(마두)").all()
            names3 = [applicant.user.name for applicant in applicants]
            applicants = SatBoard.query.filter_by(slot="2~4시(마두)").all()
            names4 = [applicant.user.name for applicant in applicants]
            return jsonify({"message": "신청이 취소되었습니다.", "names1": names1, "names2": names2, "names3": names3, "names4": names4}), 200

        else:
            return jsonify({"error": "신청을 찾을 수 없습니다."}), 400
    elif day == "일":
        application_to_cancel = SunBoard.query.filter_by(user_id=user.id, slot=slot_name).first()
        if application_to_cancel:
            db.session.delete(application_to_cancel)
            db.session.commit()

            applicants = SunBoard.query.filter_by(slot="1:30~3:30").all()
            names1 = [applicant.user.name for applicant in applicants]
            return jsonify({"message": "신청이 취소되었습니다.", "names1": names1}), 200

        else:
            return jsonify({"error": "신청을 찾을 수 없습니다."}), 400





#슬롯비활성화업데이트
@bp.route('/update_disabled_slot', methods=['POST'])
def update_disabled_slot():
    slot_id = request.form['slot_id']
    is_disabled = request.form['is_disabled'] == 'true'

    disabled_slot = DisabledSlot.query.filter_by(slot_id=slot_id).first()
    if not disabled_slot:
        disabled_slot = DisabledSlot(slot_id=slot_id, is_disabled=is_disabled)
        db.session.add(disabled_slot)
    else:
        disabled_slot.is_disabled = is_disabled

    db.session.commit()
    return jsonify({"message": "슬롯 비활성화 상태가 업데이트되었습니다."}), 200

@bp.route('/get_disabled_slots', methods=['GET'])
def get_disabled_slots():
    disabled_slots = DisabledSlot.query.filter_by(is_disabled=True).all()
    disabled_slot_ids = [ds.slot_id for ds in disabled_slots]
    return jsonify({"disabled_slot_ids": disabled_slot_ids})

#공지등록
@bp.route('/notice', methods=['POST'])
def create_notice():
    print('Received data:', request.form)
    contents = request.form.getlist('contents[]')
    slot = request.form['slot']

    #같은슬롯이름의 데이터를 찾아서 전부 지움.
    Notice.query.filter_by(slot=slot).delete()
    db.session.commit()

    #새로들어온 내용을 넣는다.
    for content in contents:
        notice = Notice(content=content.strip(), slot=slot)
        db.session.add(notice)

    db.session.commit()
    return jsonify({"message": "공지가 등록되었습니다."}), 200

@bp.route('/get_notices', methods=['POST'])
def get_notices():
    slot = request.form['slot']
    notices = Notice.query.filter_by(slot=slot).all()
    notice_contents = [notice.content for notice in notices]
    return jsonify({"notice_contents": notice_contents})

@bp.route('/get_overseer_list', methods=['GET'])
def get_overseer_list():
    overseer_list = Overseer.query.all()
    overseer_names = [overseer.name for overseer in overseer_list]
    return jsonify({"overseer_list": overseer_names})

#요일공지데이터베이스에저장
@bp.route('/save_notice', methods=['POST'])
def save_notice():
    day_of_week = request.form['day_of_week']
    notice = request.form['notice']

    existing_notice = DayNotice.query.filter_by(day_of_week=day_of_week).first()

    if existing_notice:
        existing_notice.notice = notice
    else:
        day_notice = DayNotice(day_of_week=day_of_week, notice=notice)
        db.session.add(day_notice)

    db.session.commit()

    return jsonify({"message": "공지가 저장되었습니다."}), 200

#요일공지레이블창으로 보내기
@bp.route('/get_notice', methods=['GET'])
def get_notice():
    day_of_week = request.args.get('day_of_week')
    day_notice = DayNotice.query.filter_by(day_of_week=day_of_week).first()

    if day_notice:
        return jsonify({"notice": day_notice.notice}), 200
    else:
        return jsonify({"notice": ""}), 200


#데이터베이스에 있는 회원명단출력
@bp.route('/userquanbu')
def us():
    #데이터를 불러와서 저장
    user_list = User.query
    overseer_list = Overseer.query
    #저장된 데이터를 전달
    return render_template('users/user_list.html', user_list=user_list,overseer_list=overseer_list)


@bp.route('/delete_all/<model_name>', methods=['POST'])
def delete_all(model_name):
    if model_name == "user":
        User.query.delete()
    elif model_name == "tueboard":
        TueBoard.query.delete()
    elif model_name == "thuboard":
        ThuBoard.query.delete()
    elif model_name == "satboard":
        SatBoard.query.delete()
    elif model_name == "sunboard":
        SunBoard.query.delete()
    else:
        print("Model not found.")
        return redirect(url_for('index'))

    db.session.commit()
    print(f"All records deleted for {model_name}.")
    return redirect(url_for('main.kongzhi'))
@bp.route('/kongzhi')
def kongzhi():
    return render_template('users/kongzhi.html')

