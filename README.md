## 地摊货二手商品交易平台

----

#### 依赖的包

```python
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

```python
flask db init
flask db migrate
flask db upgrade
```

初始化创建表时，先删除`migrations`文件夹，执行
```python
flask db init
flask db migrate
flask db upgrade
```
当表发生变化时，执行
```python
flask db migrate
flask db upgrade
```

这是一次测试,测试
