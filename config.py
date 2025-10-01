import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, 'oneday.db')}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY", SECRET_KEY)  # (Flask-WTF 쓸 때)

SECRET_KEY = "dev"