from sqlalchemy import and_, desc

from datagenerator import app
import json
import datetime
from flask import Blueprint, request, jsonify, render_template
from datagenerator.models.community import *
from datagenerator.models.user import *
from sqlalchemy import func

bp = Blueprint('bp', __name__)


@app.route('/', methods=['GET'])
def index():
    """
    系统首页，即系统入口
    :return: 渲染模板
    """
    return render_template('index.html')


@app.route('/totalsuggestion', methods=['get'])
def total_suggestion():
    """
    功能: 获取审核已通过的所有案例
    :return: 返回所有案例数
    """
    try:
        data = Suggestion.query.filter(Suggestion.status > 0).count()
        return json.dumps({'code': 200,
                           'data': data})
    except Exception as e:
        return json.dumps({'code': 500, 'data': e})


@app.route('/totalsuggestionadmin', methods=['get'])
def total_suggestion_admin():
    try:
        return json.dumps({'code': 200,
                           'data': Suggestion.query.count()})
    except:
        return json.dumps({'code': 500, 'data': '操作错误！'})


@app.route('/adoptsuggestion', methods=['GET'])
def adopt_suggestion():
    try:
        # 审核案例的id
        obj_id = request.args.get('id')
        # 审核案例的推荐指数
        # 数据库中找到该案例对象
        obj = Suggestion.query.filter_by(id=obj_id).first()
        # 修改该案例的审核标志位
        obj.status = 1
        # 提交操作
        db.session.commit()
        return json.dumps({'code': 200, 'data': 'success', "msg": "审核成功"})
    except:
        return json.dumps({"code": 500, "status": "error", "msg": "审核错误"})


@app.route('/adoptsuggestionreply', methods=['GET'])
def adopt_suggestion_reply():
    try:
        # 审核案例的id
        obj_id = request.args.get('id')
        # 审核案例的推荐指数
        # 数据库中找到该案例对象
        obj = SuggestionReply.query.filter_by(id=obj_id).first()
        # 修改该案例的审核标志位
        obj.status = 1
        # 提交操作
        db.session.commit()
        return json.dumps({'code': 200, 'data': 'success', "msg": "审核成功"})
    except:
        return json.dumps({"code": 500, "status": "error", "msg": "审核错误"})


@app.route('/listsuggestion', methods=['post'])
def list_suggestion():
    """
    功能: 列出所有意见数据
    :return: 成功返回data, 失败返回相应的异常。data的值格式如下:
             [
             {'id':1,
             'nice_name':'ffvfbfb',
             'suggestion':'这是测试意见'，
             'date_created':'2019-07-15 15:10:30'}
             ]
    """

    try:
        page = int(request.form.get('page')) - 1
        num = int(request.form.get('num'))
        # 获取指定页码以及数量的意见列表
        suggestions = Suggestion.query.filter(Suggestion.status > 0).offset(num * page).limit(num).all()
        data = []
        for suggestion in suggestions:
            suggestion_dict = suggestion.to_dict()
            # 获取该意见下的所有评论回复
            suggestion_reply = SuggestionReply.query.filter_by(suggestion_id=suggestion.id).all()
            # 定义一个临时变量列表，用于存储回复列表
            _temp = []
            # 遍历所有回复
            for suggestion_reply_item in suggestion_reply:
                # 获取实例对象，转换为字典
                suggestion_reply_item_dict = suggestion_reply_item.to_dict()
                # 加载到临时列表内
                _temp.append(suggestion_reply_item_dict)
            suggestion_dict['reply'] = _temp
            data.append(suggestion_dict)

        return json.dumps({'code': 200, 'data': data})
    except Exception as e:
        print(e)
        return json.dumps({"code": 500, "status": "error", "msg": "内部错误 %s" % str(e)})


@app.route('/listsuggestionadmin', methods=['post'])
def list_suggestion_admin():
    """
    功能: 列出所有意见数据
    :return: 成功返回data, 失败返回相应的异常。data的值格式如下:
             [
             {'id':1,
             'nice_name':'ffvfbfb',
             'suggestion':'这是测试意见'，
             'date_created':'2019-07-15 15:10:30'}
             ]
    """

    try:
        page = int(request.form.get('page')) - 1
        num = int(request.form.get('num'))
        suggestions = Suggestion.query.order_by(Suggestion.status).offset(num * page).limit(num).all()
        data = []
        for suggestion in suggestions:
            suggestion_dict = suggestion.to_dict()
            # 获取该意见下的所有评论回复
            suggestion_reply = SuggestionReply.query.filter_by(suggestion_id=suggestion.id).all()
            # 定义一个临时变量列表，用于存储回复列表
            _temp = []
            # 遍历所有回复
            for suggestion_reply_item in suggestion_reply:
                # 获取实例对象，转换为字典
                suggestion_reply_item_dict = suggestion_reply_item.to_dict()
                # 加载到临时列表内
                _temp.append(suggestion_reply_item_dict)
            suggestion_dict['reply'] = _temp
            data.append(suggestion_dict)
        return json.dumps({'code': 200, 'data': data})
    except Exception as e:
        print(e)
        return json.dumps({"code": 500, "status": "error", "msg": "内部错误 %s" % str(e)})


@app.route('/addsuggestion', methods=['POST'])
def add_suggestion():
    '''
    功能: 添加意见
    :return: 成功返回success, 失败返回相应的异常
    '''
    try:
        content = request.form.get('content')
        if not content:
            return jsonify({
                'code': 400,
                'msg': '添加建议的内容不能为空'
            })
        configs = {
            "nick_name": request.form.get('nick_name', '一位不方便透露身份的网友'),
            "content": content,
        }
        Suggestion.insert(configs)
        return json.dumps({"code": 200, "status": "success", "msg": "添加成功"})
    except:
        return json.dumps({"code": 500, "status": "error", "msg": "添加错误"})


@app.route('/delsuggestion', methods=['GET'])
def del_suggestion():
    try:
        obj_id = request.args.get('id')
        # 删除该意见的所有回复
        reply_obj = SuggestionReply.query.filter_by(suggestion_id=obj_id).all()
        for item in reply_obj:
            db.session.delete(item)
            db.session.commit()
        obj = Suggestion.query.filter_by(id=obj_id).first()
        db.session.delete(obj)
        db.session.commit()
        return json.dumps({'code': 200, 'data': 'success', "msg": "删除成功"})
    except:
        return json.dumps({"code": 500, "status": "error", "msg": "删除错误"})


@app.route('/delsuggestionreply', methods=['GET'])
def del_suggestion_reply():
    try:
        obj_id = request.args.get('id')
        obj = SuggestionReply.query.filter_by(id=obj_id).first()
        db.session.delete(obj)
        db.session.commit()
        return json.dumps({'code': 200, 'data': 'success', "msg": "删除成功"})
    except:
        return json.dumps({"code": 500, "status": "error", "msg": "删除错误"})


@app.route('/replysuggestion', methods=['POST'])
def reply_suggestion():
    try:
        nick_name = request.form.get('nick_name', '一位不方便透露身份的网友')
        reply_target = request.form.get('reply_target')
        content = request.form.get('content')
        suggestion_id = int(request.form.get('suggestion_id'))

        if not (content and suggestion_id):
            return json.dumps({'code': 400, 'msg': '添加建议的内容不能为空'})
        configs = {"nick_name": nick_name,"reply_target":reply_target, "content": content, "suggestion_id": suggestion_id}
        print('ssssssssssss', configs)
        SuggestionReply.insert(configs)
        return json.dumps({"code": 200, "status": "success", "msg": "添加成功"})
    except:
        return json.dumps({"code": 500, "status": "error", "msg": "添加错误"})


@app.route('/listcase', methods=['post'])
def list_case():
    '''
    功能: 列出所有案例模型数据
    :return: 成功返回data, 失败返回相应的异常。data的值格式如下:
             [
             {'id':1,
             'nice_name':'ffvfbfb',
             'table_name': '人口信息表',
             'configs':'[{"component": "NameConfig","id": "1562834639872","fieldName": "name","dataType": "Name","
                        options": {"sex": "random","__unique": false,"__display": true,"__fieldName": "name"},
                        "relation": {"fieldNames": "sex","type": "COR_RELATION","allowTypes": ["Sex"]},
                        "__unique": false,"__display": true},]'，
             'quote_num':0,
             'like_num':0,
             'date_created':'2019-07-15 15:10:30'}
             ]
    '''
    try:
        page = int(request.form.get('page')) - 1
        num = int(request.form.get('num'))
        cases = Case.query.filter(Case.status > 0).order_by(desc(Case.fast_config)).offset(num * page).limit(num).all()

        data = []
        for case in cases:
            case_dict = case.to_dict()
            data.append(case_dict)
        return json.dumps({'code': 200, 'data': data})
    except Exception as e:
        print(e)
        return json.dumps({"code": 500, "status": "error", "msg": "内部错误 %s" % str(e)})


@app.route('/listcaseadmin', methods=['POST'])
def list_case_admin():
    try:
        page = int(request.form.get('page')) - 1
        num = int(request.form.get('num'))
        cases = Case.query.order_by(Case.status).offset(num * page).limit(num).all()
        data = []
        for case in cases:
            case_dict = case.to_dict()
            data.append(case_dict)
        return json.dumps({'code': 200, 'data': data})
    except Exception as e:
        print(e)
        return json.dumps({"code": 500, "status": "error", "msg": "内部错误 %s" % str(e)})


@app.route('/getfastconfigs', methods=['GET'])
def get_fast_configs():
    try:
        cases = Case.query.filter(and_(Case.status > 0, Case.fast_config > 0)).order_by(desc(Case.fast_config)).all()
        data = []
        for case in cases:
            case_dict = case.to_dict()
            data.append(case_dict)
        return json.dumps({'code': 200, 'data': data})
    except Exception as e:
        print(e)
        return json.dumps({"code": 500, "status": "error", "msg": "内部错误 %s" % str(e)})


@app.route('/totalcase', methods=['get'])
def total_case():
    return json.dumps({'code': 200, 'data': Case.query.filter(Case.status > 0).count()})


@app.route('/updatecase', methods=['POST'])
def update_case():
    '''
   功能: 更新引用与点赞次数统计数据
   :return: 成功返回success, 失败返回相应的异常
   '''
    try:
        case_id = request.form.get('id')
        case = Case.query.filter_by(id=case_id).first()
        type = request.form.get('type')

        if type == 'like':
            case.like_num += 1
        elif type == 'quote':
            case.quote_num += 1
        else:
            return json.dumps({"code": 400, "status": "error", "msg": "请求参数type值错误"})
        db.session.commit()
        return json.dumps({'code': 200, 'data': 'success'})
    except Exception as e:
        return json.dumps({"code": 500, "status": "error", "msg": "查询错误"})


@app.route('/delcase', methods=['GET'])
def delcase():
    try:
        obj_id = request.args.get('id')
        obj = Case.query.filter_by(id=obj_id).first()
        db.session.delete(obj)
        db.session.commit()
        return json.dumps({'code': 200, 'data': 'success', "msg": "删除成功"})
    except:
        return json.dumps({"code": 500, "status": "error", "msg": "删除错误"})


@app.route('/recommendcase', methods=['GET'])
def recommend_case():
    try:
        # 审核案例的id
        obj_id = request.args.get('id')
        # 审核案例的推荐指数
        star = request.args.get('star', 1)
        # 数据库中找到该案例对象
        obj = Case.query.filter_by(id=obj_id).first()
        # 修改该案例的审核标志位
        obj.fast_config = star
        # 提交操作
        db.session.commit()
        return json.dumps({'code': 200, 'data': 'success', "msg": "审核成功"})
    except:
        return json.dumps({"code": 500, "status": "error", "msg": "审核错误"})


@app.route('/adoptcase', methods=['GET'])
def adopt_case():
    try:
        # 审核案例的id
        obj_id = request.args.get('id')
        # 审核案例的推荐指数
        # 数据库中找到该案例对象
        obj = Case.query.filter_by(id=obj_id).first()
        # 修改该案例的审核标志位
        obj.status = 1
        # 提交操作
        db.session.commit()
        return json.dumps({'code': 200, 'data': 'success', "msg": "审核成功"})
    except:
        return json.dumps({"code": 500, "status": "error", "msg": "审核错误"})


@app.route('/totalcaseadmin', methods=['GET'])
def total_case_admin():
    try:
        return json.dumps(
            {'code': 200,
             'data': len(Case.query.all())
             }
        )
    except:
        return json.dumps({'code': 500, 'mgs': '操作错误'})


@app.route('/addcase', methods=['POST'])
def add_case():
    '''
    功能: 保存并分享案例模型
    :return: 成功返回success, 失败返回相应的异常
    '''
    try:
        table_name = request.form.get('table_name')
        configs = request.form.get('configs')
        if not table_name:
            return jsonify({
                'code': 400,
                'msg': '分享表名不能为空'
            })
        if not configs:
            return jsonify({
                'code': 400,
                'msg': '分享配置项不能为空'
            })

        configs = {
            "nick_name": request.form.get('nick_name', '一位不方便透露身份的网友'),
            "table_name": table_name,
            "configs": configs,
            "quote_num": request.form.get('quote_num', 0),
            "like_num": request.form.get('like_num', 0)
        }
        Case.insert(configs)
        return json.dumps({"code": 200, "status": "success", "msg": "添加成功"})
    except:
        return json.dumps({"code": 500, "status": "error", "msg": "添加错误"})


@app.route('/login', methods=['POST'])
def login():
    """
    功能: 更新引用与点赞次数统计数据
    :return: 成功返回success, 失败返回相应的异常
    """
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            # 依据用户名查表，获得对用的用户对象
            obj = User.query.filter_by(username=username).first()
            # 判断用户名是否存在，不存在，返回对应的信息
            if not obj:
                return json.dumps({'code': 201, 'status': 'error', 'msg': '没有找到该用户！'})
            # 进行密码验证，判断密码是否正确，正确
            elif obj.verify_password(password):
                return json.dumps({ 'code': 200,
                                    'status': 'success',
                                    'msg': '登录成功！'})
            else:
                return json.dumps({'code': 201, 'status': 'error', 'msg': '密码错误！'})
        else:
            return jsonify({
                'code': 400,
                'msg': '内容不能为空'
            })
    except:
        return json.dumps({"code": 500, "status": "error", "msg": "查询错误"})


@app.route('/adduserrecord', methods=['POST'])
def add_user_record():
    try:
        configs = {
            'ip': request.remote_addr,
            'configs': request.form.get('configs'),
            'export_data_number': request.form.get('export_data_number'),
            'export_file_type': request.form.get('export_file_type'),
            'export_filename': request.form.get('export_filename'),
        }
        UserRecord.insert(configs)
        return json.dumps({"code": 200, "status": "error", "msg": "查询错误"})
    except:
        return json.dumps({"code": 500, "status": "error", "msg": "查询错误"})


@app.route('/getuserrecord',methods=['GET'])
def get_table():

    try:
        ip_filter = request.args.get('ipchoice')
        time_filter = request.args.get('timefilter')

        start_time = request.args.get('starttime')
        if start_time != "NaN":
            start_time = datetime.datetime.fromtimestamp(int(start_time)/1000)

        end_time = request.args.get('endtime')
        if end_time != "NaN":
            end_time = datetime.datetime.fromtimestamp(int(end_time)/1000)

        page_size = int(request.args.get('pagesize'))
        current_page = int(request.args.get('currentpage')) - 1
        if request.args.get('firstvisit') == '0':
            ip_list = []
            user_record = UserRecord.query.all()
            for item in user_record:
                if item.to_dict()['ip'] not in ip_list:
                    ip_list.append(item.to_dict()['ip'])
        if ip_filter == "ALL":
            if time_filter == "ALL":
                # ip与时间都为全部
                temp = UserRecord.query
                user_record = temp.offset(page_size * current_page).limit(page_size).all()
                count = temp.count()
            else:
                # ip无限制， 时间有限制
                temp = UserRecord.query.filter(
                                func.date_format(UserRecord.date_created, '%Y-%m-%d') <= end_time.strftime('%Y-%m-%d'),
                                func.date_format(UserRecord.date_created, '%Y-%m-%d') >= start_time.strftime('%Y-%m-%d')
                              )
                user_record = temp.offset(page_size * current_page).limit(page_size).all()
                count = temp.count()
        else:
            # ip限制， 时间无限制
            if time_filter == "ALL":
                temp = UserRecord.query.filter(
                    UserRecord.ip==ip_filter)
                user_record = temp.offset(page_size * current_page).limit(page_size).all()
                count = temp.count()
            else:
                # ip限制， 时间限制
                temp = UserRecord.query.filter(
                    func.date_format(UserRecord.date_created, '%Y-%m-%d') <= end_time.strftime('%Y-%m-%d'),
                    func.date_format(UserRecord.date_created, '%Y-%m-%d') >= start_time.strftime('%Y-%m-%d'),
                    UserRecord.ip == ip_filter)
                user_record = temp.offset(page_size * current_page).limit(page_size).all()
                count = temp.count()
        data = []
        for item in user_record:
            data.append(item.to_dict())
        if request.args.get('firstvisit') == '0':
            return json.dumps({"code": 200, "status": "success", "data": data, "ipfilter":ip_list,"totalNum":count})
        else:
            return json.dumps({"code": 200, "status": "success", "data": data, "totalNum": count})
    except:
        return json.dumps({"code": 500, "status": "error", "msg": "查询错误"})


