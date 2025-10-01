from oneday import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'),
                        nullable=False)

    user=db.relationship('User', backref=db.backref('question_set')


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship(Question, backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

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

    def __repr__(self):
        return f"<Course {self.classid}>"
