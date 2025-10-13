from oneday import db
from sqlalchemy.sql import func

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    image_path = db.Column(db.String(200), nullable=True)
    user=db.relationship('User', backref=db.backref('question_set'))



class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship(Question, backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),
                        nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)


# 예약
class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    class_name = db.Column(db.String(100), nullable=False)
    reserved_date = db.Column(db.Date, nullable=False)
    reserved_time = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)

# 클래스등록
class Course(db.Model):
    __tablename__ = "course"

    id = db.Column(db.Integer, primary_key=True)
    classid = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)                 # 설명
    price = db.Column(db.Integer, nullable=False, default=0)         # 가격(원)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.func.now())             # 생성시각(DB가 기록)
    duration_minutes = db.Column(db.Integer, nullable=False, default=60)
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    image_path = db.Column(db.String(200), nullable=True)

    # 추가 이미지 (옵션)
    images = db.relationship("CourseImage", backref="course", lazy="selectin", cascade="all, delete-orphan")


class CourseImage(db.Model):
    __tablename__ = "course_image"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id", ondelete="CASCADE"), nullable=False, index=True)
    path = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())

    def __repr__(self):
        return f"<CourseImage course_id={self.course_id} path={self.path!r}>"
