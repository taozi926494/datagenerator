from datagenerator import db, Base


class User(Base):
    __tablename__ = 'user'
    # 登录用户的用户名，用户名的唯一性
    username = db.Column(db.String(50), unique=True)
    # 用户密码
    password = db.Column(db.String(300))

    def verify_password(self, password):
        """
        功能：对密码进行解析
        :param password: 待解析的密码
        :return: None
        """
        return True if password == self.password else False
