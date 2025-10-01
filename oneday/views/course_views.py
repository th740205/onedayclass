from flask import Blueprint, render_template, request, redirect, url_for, flash
from oneday import db
from oneday.models import Course

bp = Blueprint("course", __name__, url_prefix="/course")

@bp.route("/")     # → /course/ 매칭
@bp.route("")      # → /course  매칭
def index():
    return redirect(url_for("course.workspace"))


@bp.route("/workspace")
def workspace():
    courses = Course.query.order_by(Course.created_at.desc()).all()  # ✅ DB 조회
    return render_template("course/workspace.html", courses=courses)

@bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        classid = request.form.get("classid", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price", "0").strip()

        if not classid or not description:
            flash("클래스 ID와 설명은 필수입니다.", "danger")
            return redirect(url_for("course.create"))

        if Course.query.filter_by(classid=classid).first():
            flash("이미 존재하는 클래스 ID입니다.", "warning")
            return redirect(url_for("course.create"))

        course = Course(classid=classid, description=description, price=int(price or 0))
        db.session.add(course)
        db.session.commit()

        flash(f"클래스가 등록되었습니다: {classid}", "success")
        return redirect(url_for("course.workspace"))

    return render_template("course/create.html")
