import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from werkzeug.utils import secure_filename
from oneday import db
from oneday.models import Course, CourseImage
from oneday.forms import CourseCreateForm
from sqlalchemy.orm import selectinload

bp = Blueprint("course", __name__, url_prefix="/course")


@bp.route("/")     # → /course/ 매칭
@bp.route("")      # → /course  매칭
def index():
    return redirect(url_for("course.workspace"))


# 워크스페이스
@bp.route("/workspace")
def workspace():
    tab = request.args.get("tab", "create")

    if tab == "completed":
        courses = (
            Course.query.filter_by(is_published=True)
            .options(selectinload(Course.images))
            .order_by(Course.created_at.desc())
            .all()
        )
    else:  # create
        courses = (
            Course.query.filter_by(is_published=False)
            .options(selectinload(Course.images))
            .order_by(Course.created_at.desc())
            .all()
        )

    return render_template(
        "course/workspace.html",
        courses=courses,
        active_tab=tab,
    )


# 클래스 생성
@bp.route("/create", methods=["GET", "POST"])
def create():
    form = CourseCreateForm()

    if form.validate_on_submit():
        # 중복 classid 체크
        if Course.query.filter_by(classid=form.classid.data.strip()).first():
            flash("이미 존재하는 클래스 ID입니다.", "warning")
            return redirect(url_for("course.create"))

        # 코스 생성
        course = Course(
            classid=form.classid.data.strip(),
            description=form.description.data.strip(),
            price=int(form.price.data or 0),
            duration_minutes=int(form.duration_minutes.data or 60),
            is_published=True,
        )
        db.session.add(course)
        db.session.flush()  # course.id 확보

        # 업로드 폴더 안에 'courses' 폴더 준비
        upload_root = current_app.config["UPLOAD_FOLDER"]   # .../uploads
        subdir = "courses"
        subdir_path = os.path.join(upload_root, subdir)
        os.makedirs(subdir_path, exist_ok=True)

        # --- 대표 이미지 저장 ---
        main_file = form.image.data
        if main_file and main_file.filename:
            filename = f"{uuid.uuid4().hex}_{secure_filename(main_file.filename)}"
            abs_path = os.path.join(subdir_path, filename)
            main_file.save(abs_path)

            # DB에는 'courses/파일명' 형태로만 저장 (uploads는 넣지 않기!)
            rel_path = f"{subdir}/{filename}".replace("\\", "/")
            course.image_path = rel_path
            db.session.add(CourseImage(course_id=course.id, path=rel_path))

        # --- 추가 이미지 저장 (최대 4장) ---
        extra_files = form.images.data or []
        for f in extra_files[:4]:
            if not f or not f.filename:
                continue
            filename = f"{uuid.uuid4().hex}_{secure_filename(f.filename)}"
            abs_path = os.path.join(subdir_path, filename)
            f.save(abs_path)
            rel_path = f"{subdir}/{filename}".replace("\\", "/")
            db.session.add(CourseImage(course_id=course.id, path=rel_path))

        db.session.commit()

        flash(f"클래스가 등록되었습니다: {course.classid}", "success")
        return redirect(url_for("course.workspace", tab="completed"))

    return render_template("course/create.html", form=form)


@bp.route("/uploads/<path:filename>")
def uploaded_file(filename):
    # 1) 역슬래시 → 슬래시
    cleaned = filename.replace("\\", "/")
    # 2) 혹시 실수로 'uploads/'가 앞에 붙어 오면 제거
    if cleaned.startswith("uploads/"):
        cleaned = cleaned[len("uploads/"):]  # 'uploads/' 제거

    folder = current_app.config["UPLOAD_FOLDER"]  # 예: .../onedayclass/uploads
    full_path = os.path.join(folder, cleaned)

    # 🔎 디버그 로그
    print("[UPLOAD] folder =", folder)
    print("[UPLOAD] request filename =", filename)
    print("[UPLOAD] cleaned =", cleaned)
    print("[UPLOAD] full_path =", full_path)
    print("[UPLOAD] exists? =", os.path.isfile(full_path))

    return send_from_directory(folder, cleaned)