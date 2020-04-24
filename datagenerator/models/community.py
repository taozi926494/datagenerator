from datagenerator import db, Base


class Case(Base):
    __tablename__ = 'case'
    # 提交人的昵称
    nick_name = db.Column(db.String(50))
    # 提交内容名称
    table_name = db.Column(db.String(50))
    # 提交内容
    configs = db.Column(db.Text)
    # 引用数量
    quote_num = db.Column(db.Integer)
    # 积攒数量
    like_num = db.Column(db.Integer)
    # 添加到首页的快捷配置
    fast_config = db.Column(db.Integer, default=0)
    # 审核状态
    status = db.Column(db.Integer, default=0)

    @classmethod
    def insert(cls, configs):
        obj = cls()
        for k, v in configs.items():
            setattr(obj, k, v)
        db.session.add(obj)
        db.session.commit()

    def to_dict(self):
        return dict(
            id=self.id,
            nick_name=self.nick_name,
            table_name=self.table_name,
            configs=self.configs,
            quote_num=self.quote_num,
            like_num=self.like_num,
            date_created=str(self.date_created),
            fast_config=self.fast_config,
            status=self.status
        )


class Suggestion(Base):
    __tablename__ = 'suggestion'
    # 提交人的昵称
    nick_name = db.Column(db.String(50))
    # 提交内容
    content = db.Column(db.Text)
    # 审核状态
    status = db.Column(db.Integer, default=0)

    @classmethod
    def insert(cls, configs):
        obj = cls()
        for k, v in configs.items():
            setattr(obj, k, v)
        db.session.add(obj)
        db.session.commit()

    def to_dict(self):
        return dict(
            id=self.id,
            nick_name=self.nick_name,
            content=self.content,
            status=self.status,
            date_created=str(self.date_created),
        )


class SuggestionReply(Base):
    __tablename__ = 'suggestionreply'
    nick_name = db.Column(db.String(50))
    reply_target = db.Column(db.String(50))
    content = db.Column(db.Text)
    suggestion_id = db.Column(db.Integer, db.ForeignKey("suggestion.id"))
    # 审核状态
    status = db.Column(db.Integer, default=0)

    @classmethod
    def insert(cls, configs):
        obj = cls()
        for k, v in configs.items():
            setattr(obj, k, v)
        db.session.add(obj)
        db.session.commit()

    def to_dict(self):
        return dict(
            id=self.id,
            date_created=str(self.date_created),
            nick_name=self.nick_name,
            reply_target=self.reply_target,
            content=self.content,
            suggestion_id=self.suggestion_id,
            status=self.status
        )


class UserRecord(Base):
    __tablename__ = 'userrecord'
    # 导出数据客户端IP
    ip = db.Column(db.String(50))
    # 配置项内容
    configs = db.Column(db.Text)
    # 导出数据的数据量
    export_data_number = db.Column(db.Integer)
    # 文件类型
    export_file_type = db.Column(db.String(50))
    # 文件名
    export_filename = db.Column(db.String(50))


    @classmethod
    def insert(cls, configs):
        obj = cls()
        for k, v in configs.items():
            setattr(obj, k, v)
        db.session.add(obj)
        db.session.commit()

    def to_dict(self):
        return dict(
            id=self.id,
            date_created=str(self.date_created),
            ip=self.ip,
            export_data_number=self.export_data_number,
            export_file_type=self.export_file_type,
            export_filename=self.export_filename,
            configs=self.configs
        )
