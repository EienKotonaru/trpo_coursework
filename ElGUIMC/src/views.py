from flask import render_template, redirect, request, make_response
from flask.views import MethodView
from flask import jsonify

from src.criteria.CriteriaModule import CriteriaModule
from src.group.GroupModule import GroupModule
from src.user.UserModule import UserModule
from src.value.ValueModule import ValueModule

user_module = UserModule()
group_module = GroupModule()
criteria_module = CriteriaModule()
value_module = ValueModule()


class Menu(MethodView):
    def get(self):
        return render_template('menu.html')


class Registration(MethodView):
    def get(self):
        return render_template('registration.html')

    def post(self):
        user_module.register(request.form['email'], request.form['password'])
        return render_template('menu.html') #temp


class Login(MethodView):
    def get(self):
        return render_template('login.html')

    def post(self):
        user_id = user_module.login(request.form['email'], request.form['password'])
        resp = make_response(redirect('/'))
        resp.set_cookie('userID', user_id)
        return resp


class CreateGroup(MethodView):
    def get(self):
        can_add = group_module.check_groups_number()
        return render_template('create_group.html', can_add=can_add)

    def post(self):
        group_module.check_and_create(request.form['name'], request.form['description'])
        return redirect('/groups')


class GroupsList(MethodView):
    def get(self):
        group_set = group_module.get_groups_list()
        return render_template('show_groups.html', groups=group_set.groups)


class CreateCriteria(MethodView):
    def get(self, group_id):
        group = group_module.get_single_group(group_id)
        criterias = criteria_module.get_criterias_by_group(group_id)
        return render_template('create_criteria.html', group=group, criterias=criterias)

    def post(self, group_id):
        if request.form['type'] == "save":
            criteria_id = criteria_module.check_and_create(request.form['name'],
                                                           request.form['weight'],
                                                           request.form['measure'],
                                                           group_id)
            return jsonify({"success": True, "id": criteria_id})
        elif request.form['type'] == "delete":
            criteria_module.remove_criteria(request.form['id'])
            return jsonify({"success": True})


class CreateValues(MethodView):
    def get(self, group_id):
        group = group_module.get_single_group(group_id)
        criterias = criteria_module.get_criterias_by_group(group_id)
        values_history = value_module.get_values_history(criterias)
        return render_template('add_values.html', group=group, criterias=criterias, values_history=values_history)

    def post(self, group_id):
        test=request.form
        value_module.create_values_for_criterias(request.form.getlist('value'), request.form.getlist('criteria_id'))
        return redirect('/add_values/' + str(group_id))
