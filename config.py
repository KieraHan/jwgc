import os
# 파이보에 ORM을 적용하려면 데이터베이스 설정이 필요하다. 루트 디렉터리에 config.py 파일을 생성하고 다음과 같은 코드를 작성하자.
BASE_DIR = os.path.dirname(__file__)


SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR,'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

#
# SQLALCHEMY_DATABASE_URI는 데이터베이스 접속 주소이고 SQLALCHEMY_TRACK_MODIFICATIONS는 SQLAlchemy의 이벤트를 처리하는 옵션이다.
# 이 옵션은 파이보에 필요하지 않으므로 False로 비활성화하자.
# SQLALCHEMY_DATABASE_URI 설정에 의해 SQLite 데이터베이스가 사용되고 데이터베이스 파일은 프로젝트 홈 디렉터리 바로 밑에 pybo.db 파일로 저장된다.