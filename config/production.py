from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\x85\xb8\xcc\xfe\xef\xf7T\xe8]\xef?\xa6\xa6\x17\xf4\xa3'
