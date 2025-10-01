from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# from flask_bcrypt import Bcrypt
# from flask_cors import CORS

import config


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM 적용
    db.init_app(app)
    migrate.init_app(app, db)
    from .import models

    # bcrypt = Bcrypt(app)
    # CORS(app, supports_credentials=True)

   
    # 블루프린트
    from .views import main_views, question_views, answer_views, auth_views, course_views, reservation_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(course_views.bp)
    app.register_blueprint(reservation_views.bp)


    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime



    return app