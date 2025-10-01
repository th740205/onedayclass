from flask import Blueprint, render_template, request

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    page = request.args.get('page', default=1, type=int)  # 페이지 번호
    question_list = Question.query.order_by(Question.create_date.desc()).paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/')
def home():
    return render_template('home.html')