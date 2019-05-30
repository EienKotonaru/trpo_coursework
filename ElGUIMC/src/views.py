import codecs
import json

from flask import render_template, redirect, request, make_response
from flask.views import MethodView
from flask import jsonify

from src.criteria.CriteriaModule import CriteriaModule
from src.group.GroupModule import GroupModule
from src.role.RoleModule import RoleModule
from src.user.UserModule import UserModule
from src.utils.decorators import login_required
from src.utils.functions import get_role_name
from src.value.ValueModule import ValueModule
from src.student.StudentModule import StudentModule
from src.profile.ProfileModule import ProfileModule
from src.employee.EmployeeModule import EmployeeModule
from src.tsr.TsrModule import TsrModule
from src.request.RequestModule import RequestModule


user_module = UserModule()
group_module = GroupModule()
student_module = StudentModule()
criteria_module = CriteriaModule()
value_module = ValueModule()
role_module = RoleModule()
profile_module = ProfileModule()
employee_module = EmployeeModule()
tsr_module = TsrModule()
request_module = RequestModule()

DES_KEY = b"eguimc19"


class Menu(MethodView):
    @login_required
    def get(self):
        return render_template('menu.html', user_group=get_role_name())


class Registration(MethodView):
    def get(self):
        return render_template('registration.html')

    def post(self):
        uuid = user_module.ldap_login(request.form['username_ais'], request.form['password_ais'])
        profile_id, role_name = profile_module.get_link_info(uuid)
        role_id = role_module.get_role_id(role_name)
        user_module.register(request.form['email'], request.form['password'], profile_id, role_id)
        return render_template('menu.html')


class Login(MethodView):
    def get(self):
        return render_template('login.html')

    def post(self):
        user_id = user_module.login(request.form['email'], request.form['password'])
        resp = make_response(redirect('/'))
        resp.set_cookie('userID', user_id)
        return resp


class Logout(MethodView):
    @login_required
    def get(self):
        if request.cookies.get('userID'):
            resp = make_response(redirect('/'))
            resp.set_cookie('userID', "", expires=0)
            return resp
        return redirect('/')


class CreateGroup(MethodView):
    @login_required
    def get(self):
        can_add = group_module.check_groups_number()
        return render_template('create_group.html', can_add=can_add, user_group=get_role_name())

    @login_required
    def post(self):
        group_module.check_and_create(request.form['name'], request.form['description'])
        return redirect('/groups')


class GroupsList(MethodView):
    @login_required
    def get(self):
        group_set = group_module.get_groups_list()
        return render_template('show_groups.html', groups=group_set.groups, user_group=get_role_name())


class CreateCriteria(MethodView):
    @login_required
    def get(self, group_id):
        group = group_module.get_single_group(group_id)
        criterias = criteria_module.get_criterias_by_group(group_id)
        return render_template('create_criteria.html', group=group, criterias=criterias, user_group=get_role_name())

    @login_required
    def post(self, group_id):
        if request.form['type'] == "save":
            criteria_id = criteria_module.check_and_create(request.form['name'],
                                                           request.form['measure'],
                                                           group_id)
            return jsonify({"success": True, "id": criteria_id})
        elif request.form['type'] == "delete":
            criteria_module.remove_criteria(request.form['id'])
            return jsonify({"success": True})


class CreateValues(MethodView):
    @login_required
    def get(self, group_id):
        group = group_module.get_single_group(group_id)
        criterias = criteria_module.get_criterias_by_group(group_id)
        values_history = value_module.get_values_history(criterias)
        return render_template('add_values.html', group=group, criterias=criterias, values_history=values_history, user_group=get_role_name())

    @login_required
    def post(self, group_id):
        value_module.create_values_for_criterias(request.form.getlist('value'), request.form.getlist('criteria_id'))
        return redirect('/add_values/' + str(group_id))


class ProfileLoader(MethodView):
    @login_required
    def get(self):
        return render_template('load_users.html', user_group=get_role_name())

    @login_required
    def post(self):
        if 'xml' in request.form:
            xml = request.files.get('xml')
            student_module.import_from_xml(xml.read())
        elif 'json' in request.form:
            json_file = request.files.get('json')
            employee_module.import_from_json(json.loads(json_file.read().decode('utf-8')))
        return redirect('/load_profiles')


class ShowRoles(MethodView):
    @login_required
    def get(self):
        roles = role_module.get_roles_list()
        return render_template('show_roles.html', roles=roles, user_group=get_role_name())


class ChangePermissions(MethodView):
    @login_required
    def get(self, role_id):
        role = role_module.get_single_role(role_id)
        return render_template('edit_pages.html', role=role, user_group=get_role_name())

    @login_required
    def post(self, role_id):
        if 'save' in request.form:
            role_module.update_pages(role_id, request.form.get('name'), request.form.get('index'))
        elif 'delete' in request.form:
            role_module.delete_page(role_id, request.form.get('index'))
        elif 'new' in request.form:
            role_module.add_page(role_id, request.form.get('name'))
        return redirect('/change_permissions/' + str(role_id))


class StudentSettings(MethodView):
    @login_required
    def get(self):
        user = user_module.get_user()
        student = student_module.get_single_student(user.profile_id)
        return render_template('edit_student.html', student=student, user_group=get_role_name())

    @login_required
    def post(self):
        user = user_module.get_user()
        student_module.set_additional_info(user.profile_id, request.form.get('phone'), request.form.get('address'))
        return redirect('/settings')


class StudentsList(MethodView):
    @login_required
    def get(self):
        students = student_module.get_students_list()
        return render_template('show_students.html', students=students, user_group=get_role_name())


class AssignCriterias(MethodView):
    @login_required
    def get(self, student_id):
        student = student_module.get_single_student(student_id)
        criterias = criteria_module.get_criterias_list()
        return render_template('assign_criterias.html', student=student, criterias=criterias, user_group=get_role_name())


class CreateTsr(MethodView):
    @login_required
    def get(self):
        user = user_module.get_user()
        student = student_module.get_single_student(user.profile_id)
        tsrs = tsr_module.get_tsrs_by_student(student.id)
        return render_template('edit_tsrs.html', tsrs=tsrs, user_group=get_role_name())

    @login_required
    def post(self):
        user = user_module.get_user()
        student = student_module.get_single_student(user.profile_id)
        if "add" in request.form:
            tsr_module.create_tsr(request.form.get('manufacturer'),
                                  request.form.get('usage_since_year'),
                                  request.form.get('type'),
                                  student.id)
        elif "save" in request.form:
            tsr_module.update_tsr(request.form.get('manufacturer'),
                                  request.form.get('usage_since_year'),
                                  request.form.get('type'),
                                  request.form.get('id'))
        elif "delete" in request.form:
            tsr_module.remove_tsr(request.form.get('id'))
        return redirect('/add_tsr')


class CreateRequest(MethodView):
    @login_required
    def get(self):
        user = user_module.get_user()
        student = student_module.get_single_student(user.profile_id)
        tsrs = tsr_module.get_tsrs_by_student(student.id)

        return render_template('create_request.html', tsrs=tsrs, user_group=get_role_name())

    @login_required
    def post(self):
        user = user_module.get_user()
        student = student_module.get_single_student(user.profile_id)
        if "tsr_req" in request.form:
            request_module.create_request(None, 'В рассмотрении', student.id,
                                          tsr_id=request.form.get('tsr'),
                                          problem=request.form.get('problem'))
        elif "doc_req" in request.form:
            request_module.create_request(None, 'В рассмотрении', student.id,
                                          quantity=request.form.get('quantity'),
                                          purpose=request.form.get('purpose'))
        return redirect('/create_request')


class ShowRequests(MethodView):
    @login_required
    def get(self):
        user = user_module.get_user()
        student = student_module.get_single_student(user.profile_id)
        requests = request_module.get_student_requests(student.id)
        return render_template('show_requests.html', requests=requests, user_group=get_role_name())


class RemoveRequest(MethodView):
    @login_required
    def post(self, request_id):
        request_module.remove_request(request_id)
        return redirect('/student_requests')


class ShowRequest(MethodView):
    @login_required
    def get(self, request_id):
        found_request = request_module.get_request_by_id(request_id)
        tsr = None
        if found_request.tsr_id and found_request.problem:
            tsr = tsr_module.get_tsr_by_id(found_request.tsr_id)
        return render_template('show_request.html', found_request=found_request, tsr=tsr, user_group=get_role_name())


class RequestList(MethodView):
    @login_required
    def get(self):
        requests = request_module.get_all_requests()
        return render_template('show_requests.html', requests=requests, user_group=get_role_name())


class EditRequestStatus(MethodView):
    @login_required
    def get(self, request_id):
        found_request = request_module.get_request_by_id(request_id)
        tsr = None
        if found_request.tsr_id and found_request.problem:
            tsr = tsr_module.get_tsr_by_id(found_request.tsr_id)
        return render_template('show_request.html', found_request=found_request, tsr=tsr, user_group=get_role_name())

    @login_required
    def post(self, request_id):
        request_module.change_request_status(request_id, request.form.get("status"))

        return redirect('/edit_request/' + str(request_id))
