from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, FloatField, \
    IntegerField, RadioField, FileField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length, Email, InputRequired, NumberRange
from EmailCaptcha.emailcaptcha import emailcaptcha
from flask_wtf.file import FileField, FileRequired, FileAllowed


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(u"邮箱不能为空"), Email(u"请按邮箱格式输入"),
                                          Length(10, 20, message=u'长度位于10~20之间')], render_kw={'placeholder': u'输入邮箱'})
    password = PasswordField('密码', validators=[DataRequired(u"密码不能为空"),
                                               Length(10, 20, message=u'长度位于10~20之间')],
                             render_kw={'placeholder': u'输入密码'})


class RegistrationForm(FlaskForm):
    username = StringField('用户名',
                           validators=[DataRequired(u"用户名不能为空"), Length(min=2, max=20, message=u'长度位于2~20之间')],
                           render_kw={'placeholder': u'用户名'})
    email = StringField('邮箱',
                        validators=[DataRequired(u"邮箱不能为空"), Email(u"请按邮箱格式输入")], render_kw={'placeholder': u'邮箱'})
    alipayaccount = StringField('支付宝账号',
                                validators=[DataRequired(u"支付宝账号不能为空"), Email(u"请按支付宝账号格式输入")],
                                render_kw={'placeholder': u'支付宝账号'})
    password = PasswordField('密码', validators=[DataRequired(), Length(min=10, max=20, message=u'长度位于10~20之间')],
                             render_kw={'placeholder': u'密码'})
    confirm_password = PasswordField('确认密码',
                                     validators=[DataRequired(), EqualTo('password', message=u"密码不一致")],
                                     render_kw={'placeholder': u'重复密码'})
    captcha = StringField('验证码', validators=[DataRequired(u"验证码不能为空")], render_kw={'placeholder': u'输入验证码'})

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        res = emailcaptcha.get_captcha_by_email(email)
        if '请先获取验证码' == res:
            raise ValidationError(res)
        elif res.lower() != captcha.lower():
            raise ValidationError('验证码错误')


class ForgetPasswordForm(FlaskForm):
    email = StringField('邮箱',
                        validators=[DataRequired(u"邮箱不能为空"), Email(u"请按邮箱格式输入")], render_kw={'placeholder': u'邮箱'})
    password = PasswordField('密码', validators=[DataRequired(), Length(min=10, max=20, message=u'长度位于10~20之间')],
                             render_kw={'placeholder': u'密码'})
    confirm_password = PasswordField('确认密码',
                                     validators=[DataRequired(), EqualTo('password', message=u"密码不一致")],
                                     render_kw={'placeholder': u'重复密码'})
    captcha = StringField('验证码', validators=[DataRequired(u"验证码不能为空")], render_kw={'placeholder': u'输入验证码'})

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        res = emailcaptcha.get_captcha_by_email(email)
        if '请先获取验证码' == res:
            raise ValidationError(res)
        elif res != captcha:
            raise ValidationError('验证码错误')


class ChangeUserInfoForm(FlaskForm):
    username = StringField('用户名',
                           validators=[DataRequired(u"用户名不能为空"), Length(min=2, max=20, message=u'长度位于2~20之间')],
                           render_kw={'placeholder': u'用户名'})
    usersex = RadioField('性别', choices=[('0', '男'), ('1', '女')], default='1')
    userphone = StringField('联系电话',
                            validators=[DataRequired(u'联系电话不能为空'), Length(min=11, max=11, message=u'请输入11位的联系电话')],
                            render_kw={'placeholder': u'联系电话'})
    useralicount = StringField('支付宝账户',
                               validators=[DataRequired(u"支付宝账户不能为空"), Email(u"请按邮箱格式输入")],
                               render_kw={'placeholder': u'请输入支付宝账户'})
    userimage = FileField(
        label="上传您的图片",
        validators=[
            # 文件必须选择;
            FileRequired('请选择文件'),
            # 指定文件上传的格式;
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '只接收.jpg .jpeg .png .gif格式的文件')
        ]
    )

    def validate_userphone(self, field):
        userphone = field.data
        if not userphone.isdigit():
            raise ValidationError('联系方式中只能有数字')


class AddAddressForm(FlaskForm):
    person_name = StringField('收货人',
                              validators=[DataRequired(u"收货人不能为空"), Length(min=2, max=20, message=u'长度位于2~20之间')],
                              render_kw={'placeholder': u'收货人'})
    address = StringField('收货地址',
                          validators=[DataRequired(u"收货地址不能为空"), Length(min=10, max=40, message=u'长度位于10~40之间')],
                          render_kw={'placeholder': u'收货地址'})
    phone = StringField('联系电话',
                        validators=[DataRequired(u'联系电话不能为空'), Length(min=11, max=11, message=u'请输入11位的联系电话')],
                        render_kw={'placeholder': u'联系电话'})

    def validate_phone(self, field):
        phone = field.data
        if not phone.isdigit():
            raise ValidationError('联系电话中只能有数字')


class ChangeAddressForm(FlaskForm):
    address_id = StringField(render_kw={'style': u'display:none'})  # 不展示在页面上，只是用于携带id信息
    person_name = StringField('收货人',
                              validators=[DataRequired(u"收货人不能为空"), Length(min=2, max=20, message=u'长度位于2~20之间')],
                              render_kw={'placeholder': u'收货人'})
    address = StringField('收货地址',
                          validators=[DataRequired(u"收货地址不能为空"), Length(min=10, max=40, message=u'长度位于10~40之间')],
                          render_kw={'placeholder': u'收货地址'})
    phone = StringField('联系电话',
                        validators=[DataRequired(u'联系电话不能为空'), Length(min=11, max=11, message=u'请输入11位的联系电话')],
                        render_kw={'placeholder': u'联系电话'})

    def validate_phone(self, field):
        phone = field.data
        if not phone.isdigit():
            raise ValidationError('联系电话中只能有数字')


class UploadGoodsForm(FlaskForm):
    goods_name = StringField('商品名称',
                             validators=[DataRequired(u"商品名称不能为空"), Length(min=3, max=100, message=u'长度位于3~100之间')])
    goods_describe = TextAreaField("商品描述",
                                   validators=[DataRequired(u"商品描述不能为空"), Length(max=1024, message=u'描述不超过1024个字符')])
    image_names = StringField("图片名称", render_kw={'style': u'display:none'})
    goods_stock = IntegerField('库存', validators=[DataRequired(u"库存不能为空"),
                                                 NumberRange(min=1, max=1000, message=u'库存个数需在1~1000之间')])
    goods_price = FloatField('单价', validators=[DataRequired(u"单价不能为空")])

    def validate_image_names(self, field):
        names = field.data.split()
        print(names)
        if len(names) > 5:
            raise ValidationError("最多上传5张图片")
        elif len(names) < 1:
            raise ValidationError("请至少上传1张图片")


class ReplyCommentForm(FlaskForm):
    userid = StringField(render_kw={'style': u'display:none'})
    commentid = StringField(render_kw={'style': u'display:none'})
    content = StringField('留言', validators=[DataRequired(u"留言不能为空")])


class UpdateGoodsForm(FlaskForm):
    goods_name = StringField('商品名称',
                             validators=[DataRequired(u"商品名称不能为空"), Length(min=3, max=100, message=u'长度位于3~100之间')])
    goods_describe = TextAreaField("商品描述",
                                   validators=[DataRequired(u"商品描述不能为空"), Length(max=1024, message=u'描述不超过1024个字符')])
    image_names = StringField("图片名称", render_kw={'style': u'display:none'})
    goods_stock = IntegerField('库存', validators=[DataRequired(u"库存不能为空"),
                                                 NumberRange(min=1, max=1000, message=u'库存个数需在1~1000之间')])
    goods_price = FloatField('单价', validators=[DataRequired(u"单价不能为空")])

    def validate_image_names(self, field):
        names = field.data.split()
        #print(names)
        if len(names) > 5:
            raise ValidationError("最多上传5张图片")
        elif len(names) < 1:
            raise ValidationError("请至少上传1张图片")


class DelivergoodsForm(FlaskForm):
    order_id=StringField(render_kw={'style': u'display:none'})
    delivery_num=StringField('物流单号',
                             validators=[DataRequired(u"物流单号不能为空")],render_kw={'placeholder': u'物流单号'})

