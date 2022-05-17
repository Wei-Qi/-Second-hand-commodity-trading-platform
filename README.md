## 地摊货二手商品交易平台

----

#### 依赖的包

```text
flask_mail
werkzeug
flask_sqlalchemy
flask_migrate
flask_login
flask_wtf
email-validator
pymysql
```

----

#### 数据库更改的方法

```text
flask db init
flask db migrate
flask db upgrade
```

初始化创建表时，先删除`migrations`文件夹，执行
```text
flask db init
flask db migrate
flask db upgrade
```
当表发生变化时，执行
```text
flask db migrate
flask db upgrade
```


#### bug
修改一次用户信息后，返回的页面中无法再次点击修改信息按钮

####问题
ChangeUserInfoForm表中的属性命名规则不一致