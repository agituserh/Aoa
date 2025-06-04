import random
from flask import Blueprint, render_template, jsonify, redirect, url_for, session,flash

from decorators import login_required
from exts import redis_client

from exts import mail, db
from flask_mail import Message
from flask import request
import string
from models import  UserModel  #,EmailCaptchaModel
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash  # 加密密码

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                flash("没有此用户")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):

                # cookie不能存储太多东西，用来识别用户，存放登录与授权
                # flask的session(服务端会话？)会经过加密放入cookie
                session['user_id'] = user.id
                return redirect("/")
            else:
                flash("密码错误")
                return (url_for("auth.login"))
        else:
            for i, errors in form.errors.items():
                for error in errors:
                    flash(error)

            return redirect(url_for("auth.login"))


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))  # 防止泄露密码
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))  # = redirect("/auth/login") 重定向到某名称
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(error)
            return redirect(url_for("auth.register"))

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@bp.route("/delete_account")
@login_required  # 确保用户已登录
def delete_account():
    user_id = session.get("user_id")
    if not user_id:
        flash("用户未登录")
        return redirect(url_for("auth.login"))

    user = UserModel.query.get(user_id)
    if not user:
        flash("用户不存在")
        return redirect(url_for("auth.login"))

    try:
        # 删除关联数据（如问题、回答）
        # QuestionModel.query.filter_by(author_id=user_id).delete()
        # AnswerModel.query.filter_by(author_id=user_id).delete()

        # 删除用户
        db.session.delete(user)
        db.session.commit()

        session.clear()  # 清除会话
        flash("账号已注销")
        return redirect("/")  # 跳转至首页或注册页
    except Exception as e:
        db.session.rollback()
        flash(f"注销失败: {str(e)}")
        return redirect(url_for("qa.index"))


@bp.route("/captcha/email")
def get_email_captcha():
    email = request.args.get("email")
    source = string.digits * 4  # ['0123456789']*4 用于采样生成验证码
    captcha = random.sample(source, 4)


    message = Message(subject="test2", recipients=[email], body=f"发送成功了吗？验证码是{captcha}")
    mail.send(message)


    captcha=str(captcha)
    redis_key = f"captcha:{email}"
    redis_client.setex(redis_key, 300, captcha)  # 300秒 = 5分钟

    # email_captcha = EmailCaptchaModel(email=email, captcha="".join(captcha))
    # db.session.add(email_captcha)
    # db.session.commit()
    return jsonify({"code": 200, "message": "", "data": None})





