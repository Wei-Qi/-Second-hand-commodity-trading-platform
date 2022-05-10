from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField,TextAreaField,FloatField,IntegerField
from wtforms.validators import DataRequired,EqualTo,ValidationError,Length,Email,InputRequired

class LoginForm(FlaskForm):
    email = StringField('email',validators=[DataRequired(u"邮箱不能为空"), Email("请按邮箱格式输入"),
                                            Length(10,20,message=u'长度位于10~20之间')],render_kw={'placeholder':u'输入邮箱'})
    password = PasswordField('password', validators=[DataRequired(u"密码不能为空"),
                                                     Length(10,20,message=u'长度位于10~20之间')],render_kw={'placeholder':u'输入密码'})

