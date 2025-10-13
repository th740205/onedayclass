from flask import Blueprint, request, redirect, url_for, flash, render_template, session, g
from werkzeug.security import generate_password_hash

from oneday import db
from oneday.forms import UserCreateForm, UserLoginForm
from oneday.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')



# ✅ 메인 페이지 (mypage.html)
@bp.route("/mypage")
def mypage():
    return render_template("auth/mypage.html")
# ✅ HTML 페이지 서빙 라우트
@bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = UserCreateForm()
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if password != password2:
            flash("비밀번호가 일치하지 않습니다.")
        else:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("이미 존재하는 이메일입니다.")
            else:
                user = User(username=name, email=email, password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
                flash("회원가입이 완료되었습니다.")
                return redirect(url_for("auth.login"))
    return render_template("auth/signup.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = UserLoginForm()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["user_name"] = user.username
            flash(f"{user.username}님 환영합니다!")
            return redirect(url_for("auth.mypage"))
        else:
            flash("이메일 또는 비밀번호가 올바르지 않습니다.")
    return render_template("auth/login.html", form=form)



# # ✅ API: 회원가입
# @bp.route("/api/signup", methods=["POST"])
# def api_signup():
#     data = request.get_json()
#     name = data.get("name")
#     email = data.get("email")
#     password = data.get("password")
#
#     if not (name and email and password):
#         return jsonify({"success": False, "msg": "모든 필드를 입력하세요."}), 400
#
#     pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
#
#     try:
#         conn = sqlite3.connect(DB_FILE)
#         c = conn.cursor()
#         c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, pw_hash))
#         conn.commit()
#         conn.close()
#     except sqlite3.IntegrityError:
#         return jsonify({"success": False, "msg": "이미 가입된 이메일입니다."}), 400
#
#     return jsonify({"success": True, "msg": "회원가입 성공"})
#
# # ✅ API: 로그인
# @bp.route("/api/login", methods=["POST"])
# def api_login():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")
#
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT id, name, password FROM users WHERE email=?", (email,))
#     row = c.fetchone()
#     conn.close()
#
#     if row and bcrypt.check_password_hash(row[2], password):
#         session["user_id"] = row[0]
#         session["user_name"] = row[1]
#         return jsonify({"success": True, "msg": "로그인 성공", "name": row[1]})
#     else:
#         return jsonify({"success": False, "msg": "잘못된 이메일 또는 비밀번호입니다."}), 401
#
# # ✅ API: 로그아웃
# @bp.route("/api/logout", methods=["POST"])
# def api_logout():
#     session.clear()
#     return jsonify({"success": True, "msg": "로그아웃 되었습니다."})
#
# # ✅ API: 현재 로그인 사용자 정보
# @app.route("/api/me", methods=["GET"])
# def api_me():
#     if "user_id" in session:
#         return jsonify({"logged_in": True, "id": session["user_id"], "name": session["user_name"]})
#     else:
#         return jsonify({"logged_in": False})


#-----------------------------------------------

# @bp.route('/signup/', methods=['GET', 'POST'])
# def signup():
#     form = UserCreateForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if not user:
#             user = User(username=form.username.data,
#                         password=generate_password_hash(form.password1.data),
#                         email=form.email.data)
#             db.session.add(user)
#             db.session.commit()
#             return redirect(url_for('main.index'))
#         else:
#             flash('이미 존재하는 사용자입니다.')
#     return render_template('auth/signup.html', form=form)
# 라우팅 함수보다 먼저 실행
# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')
#     if user_id is None:
#         g.user = None
#     else:
#         g.user = User.query.get(user_id)
#
#
# @bp.route('/logout/')
# def logout():
#     session.clear()
#     return redirect(url_for('main.index'))

