## 地摊货二手商品交易平台

---

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

---

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

#### 最新任务

删除商品功能中需要对相关图片进行删除（好像数据库会自动一起删除）

商品下架功能的实现
