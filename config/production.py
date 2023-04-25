from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b"\xd3E\xbe\x80\x03\x13\xe2W\x07\xc8G'\xfc\xfc\xe51"
