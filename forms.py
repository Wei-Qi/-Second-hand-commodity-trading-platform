from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField,TextAreaField,FloatField,IntegerField
from wtforms.validators import DataRequired,EqualTo,ValidationError,Length,Email,InputRequired

class LoginForm(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired(u"邮箱不能为空"), Email("请按邮箱格式输入"),
                                            Length(10,20,message=u'长度位于10~20之间')],render_kw={'placeholder':u'输入邮箱'})
    password = PasswordField('密码', validators=[DataRequired(u"密码不能为空"),
                                                     Length(10,20,message=u'长度位于10~20之间')],render_kw={'placeholder':u'输入密码'})

class RegistrationForm(FlaskForm):
    username = StringField('用户名',
                           validators=[DataRequired(u"用户名不能为空"), Length(min=2, max=20,message=u'长度位于2~20之间')])
    email = StringField('邮箱',
                        validators=[DataRequired(u"邮箱不能为空"), Email()])
    password = PasswordField('密码', validators=[DataRequired(),Length(min=10, max=20,message=u'长度位于10~20之间')])
    confirm_password = PasswordField('确认密码',
                                     validators=[DataRequired(), EqualTo('password')])
    captcha = StringField('验证码', validators=[DataRequired(u"验证码不能为空"),],render_kw={'placeholder':u'输入验证码'})
