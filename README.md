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
pip install python-alipay-sdk --upgrade
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





## 问题

1. 商品修改页面弹出问题
2. 个人信息栏中需要修改 删除导航栏
3. 主页  修改（最后做）
4. 商品管理页面增加查看页面
5. 后台管理增加搜索(对不同状态的商品进行模糊搜索)
5. 连接服务器数据库
6. 设置用户头像（zwq）

