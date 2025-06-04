import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel   #,EmailCaptchaModel
from exts import db, redis_client


#验证前端数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱验证失败，格式错误")])#字符串型
    captcha = wtforms.StringField(validators=[Length(min=4,max=4,message="验证码格式错误")])
    username = wtforms.StringField(validators=[Length(min=3,max=20,message="用户名格式错误")])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message="密码格式错误")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

#邮箱是否使用，验证码是否正确
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="邮箱已被注册")

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        # captcha_model = EmailCaptchaModel.query.filter_by(email=email,captcha=captcha).first()
        stored_captcha = redis_client.get(f"captcha:{email}")
        if not stored_captcha:
            raise wtforms.ValidationError(message="验证码错误")
        else:
            pass
            # db.session.delete(captcha_model)#影响运行，后面用缓存过期处理
            # db.session.commit()

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱验证失败，格式错误")])  # 字符串型
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message="标题格式错误")])# 字符串型
    content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误")])

class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="没有传入问题id")])


