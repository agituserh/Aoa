from flask import Blueprint, render_template, request, g, redirect, url_for, flash
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel
from exts import db
from decorators import login_required

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
def index():
    page = request.args.get("page", default=1, type=int)
    per_page = 5
    pagination = QuestionModel.query.order_by(QuestionModel.create_time.desc()) \
        .paginate(page=page, per_page=per_page)
    return render_template("index.html", pagination=pagination)


@bp.route("/qa/public", methods=['GET', 'POST'])
@login_required  # 登录状态装饰器
def public_qa():
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            for i, errors in form.errors.items():
                for error in errors:
                    flash(error)
            return redirect(url_for("qa.public_qa"))


@bp.route("/qa/delete/<qa_id>")
@login_required  # 登录状态装饰器
def delete_question(qa_id):
    question = QuestionModel.query.get(qa_id)
    if question.author_id == g.user.id:
        db.session.delete(question)
        db.session.commit()
    else:
        flash(f"你没有权限删除该问题。")
    return redirect("/")


@bp.route("/qa/detial/<qa_id>")
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("detail.html", question=question)


# @bp.route("/answer/public",methods=['POST'])
@bp.post("/answer/public")
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question_id))
    else:
        for i, errors in form.errors.items():
            for error in errors:
                flash(error)
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))


@bp.route("/search")
def search():
    page = request.args.get("page", default=1, type=int)
    per_page = 5
    q = request.args.get("q")
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)) \
        .paginate(page=page, per_page=per_page)
    return render_template("index.html", pagination=questions)
