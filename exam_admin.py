"""
Exam模块操作类
"""
import json
import uuid
import time

class ExamAction:
    sql = None
    def __init__(self, MySQL):
        self.sql = MySQL

    # 获取所有考题类型
    def get_exam_type(self, uinfo):
        '''
        :param uinfo: 权限相关
        :return: mysql中查询的json结果
        '''
        sql = "select ID,NAME,REVISION from EXAM_TYPE where IS_DELETE=0"               # 1
        result = self.sql.execute_query(sql,)
        print('执行了')
        print(result)
        if result != -1:
            if len(result) == 0:
                return json.dumps({"status": 1, "msg": "尚未创建题型"})
            return json.dumps({"status": 1, "data": result})
        else:
            return json.dumps({"status": -1, "msg": "未知的查询错误"})
    # 添加考题类型
    def add_exam_type(self, data, uinfo):
        print('执行了')
        uid = uinfo.get('uid')
        dm = uinfo.get('dm')
        dms = uinfo.get('dms')
        print(uinfo)
        sql = 'select count(*) as `rows` from EXAM_TYPE ' \
              'where NAME = %s and IS_DELETE = 0 and FIND_IN_SET(DATA_MASTER, %s)'
        result = self.sql.execute_query(sql, (data.get('name'), dms))
        print(result)
        if result == -1:
            return json.dumps({"status": -1, "msg": "添加题型失败，未知错误"})
        else:
            if result[0]["rows"] > 0:
                return json.dumps({"status": -1, "msg": "添加失败，该题型已存在"})
        sql = 'insert into EXAM_TYPE(ID, NAME, IS_DELETE, ' \
              'REVISION, CREATED_BY, CREATED_TIME, DATA_MASTER) ' \
              'values (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP(), %s)'
        result = self.sql.execute_non_query(sql, (str(uuid.uuid1()), data.get("name"),
                                                  str(0), int(time.time() * 1000),
                                                  uid, dm))
        print(result)
        if result > 0:
            return json.dumps({"status": 1, "msg": "数据添加成功", "data": result})
        else:
            return json.dumps({"status": -1, "msg": "添加数据失败"})
    # 删除考题类型
    def del_exam_type(self, data, uinfo):
        uid = uinfo.get('uid')
        dms = uinfo.get('dms')
        sql = 'select count(*) as `rows` from EXAM_CONTENT ' \
              'where TYPE_ID = %s and IS_DELETE = 0'
        result = self.sql.execute_query(sql, data.get('id'))
        print(data.get('id'))
        print(result)
        print('执行了')
        if result[0]['rows'] == 0:
            sql = 'update EXAM_TYPE set IS_DELETE=1 where ID=%s and IS_DELETE = 0 and FIND_IN_SET(DATA_MASTER,  %s)'
            result = self.sql.execute_non_query(sql, (data.get('id'), dms))
            if result == -1:
                return json.dumps({"status": -1, "msg": "删除数据失败，未知错误"})
            return json.dumps({"status": 1, "msg": "删除成功"})
        if result == -1:
            return json.dumps({"status": -1, "msg": "删除数据失败，未知错误"})
        else:
            if result[0]["rows"] > 0:
                return json.dumps({"status": -1, "msg": "删除失败，请先删除'作业项目'中使用此类型数据"})
    # 编辑题型
    def edit_exam_type(self, data, uinfo):
        uid = uinfo.get('uid')
        dms = uinfo.get('dms')
        sql = 'update EXAM_TYPE set NAME=%s,' \
              'REVISION = %s, UPDATED_BY = %s, ' \
              'UPDATED_TIME = CURRENT_TIMESTAMP() where ID = %s and REVISION = %s and FIND_IN_SET(DATA_MASTER, %s)'
        params = (data.get("name"),
                  int(time.time() * 1000), uid, data.get('id'),
                  data.get('revision'), dms)
        result = self.sql.execute_non_query(sql, params)
        if result > 0:
            return json.dumps({"status": 1, "msg": "更新成功", "data": result})
        else:
            return json.dumps({"status": -1, "msg": "更新数据失败"})

    # 查看相应题型下的考题
    def get_exam_content(self, data, uinfo):
        uid = uinfo.get('uid')
        dm = uinfo.get('dm')
        dms = uinfo.get('dms')
        id = data.get('id')
        sql = "select ID,QUESTION,ANSWER,MARK,REVISION from EXAM_CONTENT where TYPE_ID=%s and IS_DELETE=0"
        result = self.sql.execute_query(sql, id)
        print(result)
        if result != -1:
            if len(result) > 0:
                return json.dumps({"status": 1, "data": result})
            else:
                return json.dumps({"status": -1, "data": '暂未创建题目'})
        else:
            return json.dumps({"status": -1, "msg": "未知的查询错误"})
    # 添加题目
    def add_exam_content(self, data, uinfo):
        uid = uinfo.get('uid')
        dm = uinfo.get('dm')
        dms = uinfo.get('dms')
        sql = 'select count(*) as `rows` from EXAM_CONTENT ' \
              'where QUESTION = %s and IS_DELETE = 0 and FIND_IN_SET(DATA_MASTER, %s)'
        result = self.sql.execute_query(sql, (data.get('question'), dms))
        if result == -1:
            return json.dumps({"status": -1, "msg": "添加题型失败，未知错误"})
        else:
            if result[0]["rows"] > 0:
                return json.dumps({"status": -1, "msg": "添加失败，该题型已存在"})
        sql = 'insert into EXAM_CONTENT(ID, QUESTION, ANSWER, TYPE_ID,MARK, IS_DELETE, ' \
              'REVISION, CREATED_BY, CREATED_TIME, DATA_MASTER) ' \
              'values (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP(), %s)'
        result = self.sql.execute_non_query(sql, (str(uuid.uuid1()), data.get("question"), data.get("answer"),
                                                  data.get("type_id"), data.get('mark'), str(0),
                                                  int(time.time() * 1000), uid, dm))

        if result > 0:
            return json.dumps({"status": 1, "msg": "", "data": result})
        else:
            return json.dumps({"status": -1, "msg": "添加题目失败"})

    # 删除题目
    def del_exam_content(self, data, uinfo):
        uid = uinfo.get('uid')
        dm = uinfo.get('dm')
        dms = uinfo.get('dms')
        sql = 'update EXAM_CONTENT ' \
              'set IS_DELETE=1 where ID=%s and IS_DELETE = 0 and FIND_IN_SET(DATA_MASTER, %s)'
        result = self.sql.execute_non_query(sql, (data.get('id'), dms))
        print(result)
        if result > 0:
            return json.dumps({'status': 1, 'msg': '删除成功'})
        else:
            return json.dumps({'status': -1, 'msg': '题目删除失败，未知错误'})
    # 编辑题目
    def edit_exam_content(self, data, uinfo):
        uid = uinfo.get('uid')
        dms = uinfo.get('dms')
        sql = 'update EXAM_CONTENT set QUESTION=%s, ANSWER=%s, MARK=%s, REVISION=%s,' \
              'TYPE_ID = %s, UPDATED_BY = %s, UPDATED_TIME = CURRENT_TIMESTAMP() where ID = %s and REVISION = %s '\
              'and FIND_IN_SET(DATA_MASTER, %s)'
        result = self.sql.execute_non_query(sql, (data.get("question"), data.get("answer"),
                                                  data.get("mark"), int(time.time()*1000),
                                                  data.get('type_id'), uid, data.get('id'),
                                                  data.get('revision'), dms))
        print(result)
        if result > 0:
            return json.dumps({"status": 1, "msg": "更新成功"})
        else:
            return json.dumps({"status": -1, "msg": "更新数据失败"})







