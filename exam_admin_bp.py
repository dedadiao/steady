"""
 Exam相关路由
"""
from flask import Blueprint
from flask import request
from 实习.exam.exam_admin import ExamAction
from bps import MySQL, auth_protect


exam_bp = Blueprint('exam', __name__)
null = ''
exam_action = ExamAction(MySQL)

'''查看所有考题类型'''
@exam_bp.route('/exam/type', methods=["GET"])
@auth_protect(request)
def exam_type_info(uinfo):
    '''
    :param uinfo: 用户相关信息
    :return: 查询结果或者错误提示信息
    '''
    result = exam_action.get_exam_type(uinfo)
    return result

'''添加考题类型'''
@exam_bp.route('/exam/type/add', methods=["POST"])
@auth_protect(request)
def exam_type_add(uinfo):
    result = exam_action.add_exam_type(eval(request.data), uinfo)
    return result

'''删除考题类型'''
@exam_bp.route('/exam/type/del', methods=["GET"])
@auth_protect(request)
def exam_type_del(uinfo):
    result = exam_action.del_exam_type(request.args, uinfo)
    return result

'''编辑考题类型'''
@exam_bp.route('/exam/type/edit', methods=["POST"])
@auth_protect(request)
def exam_type_edit(uinfo):
    result = exam_action.edit_exam_type(request.form.to_dict(), uinfo)
    return result

'''查看相应类型的所有考题'''
@exam_bp.route('/exam/content', methods=["GET"])
@auth_protect(request)
def exam_content(uinfo):
    result = exam_action.get_exam_content(request.args, uinfo)
    return result


'''添加题目'''
@exam_bp.route('/exam/content/add', methods=['POST'])
@auth_protect(request)
def exam_content_add(uinfo):
    result = exam_action.add_exam_content(eval(request.data), uinfo)
    return result


'''编辑题目'''
@exam_bp.route('/exam/content/edit', methods=['POST'])
@auth_protect(request)
def exam_content_edit(uinfo):
    result = exam_action.edit_exam_content(request.form.to_dict(), uinfo)
    return result

'''删除题目'''
@exam_bp.route('/exam/content/del', methods=['GET'])
@auth_protect(request)
def exam_content_del(uinfo):
    result = exam_action.del_exam_content(request.args, uinfo)
    return result