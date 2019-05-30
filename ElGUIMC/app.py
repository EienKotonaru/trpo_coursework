from flask import Flask, render_template, request

from src.views import CreateGroup, GroupsList, Menu, CreateCriteria, CreateValues, Registration, Login, Logout, \
    ProfileLoader, ShowRoles, ChangePermissions, StudentSettings, StudentsList, AssignCriterias, CreateTsr, \
    CreateRequest, ShowRequests, RemoveRequest, ShowRequest, RequestList, EditRequestStatus


class Application:
    def __init__(self, port):
        self.port = port
        self.server = Flask(__name__, static_url_path='/static')
        self.server.url_map.strict_slashes = False
        self.create_app()

    def create_app(self) -> None:
        with self.server.app_context():
            self.server.add_url_rule('/', view_func=Menu.as_view('menu'))
            self.server.add_url_rule('/registration', view_func=Registration.as_view('new_user'))
            self.server.add_url_rule('/login', view_func=Login.as_view('auth_user'))
            self.server.add_url_rule('/logout', view_func=Logout.as_view('logout'))
            self.server.add_url_rule('/load_profiles', view_func=ProfileLoader.as_view('new_profiles'))
            self.server.add_url_rule('/create_group', view_func=CreateGroup.as_view('new_group'))
            self.server.add_url_rule('/groups', view_func=GroupsList.as_view('all_groups'))
            self.server.add_url_rule('/add_criteria/<group_id>', view_func=CreateCriteria.as_view('new_criteria'))
            self.server.add_url_rule('/add_tsr', view_func=CreateTsr.as_view('new_tsr'))
            self.server.add_url_rule('/add_values/<student_id>', view_func=CreateValues.as_view('new_values'))
            self.server.add_url_rule('/all_students', view_func=StudentsList.as_view('all_students'))
            self.server.add_url_rule('/permissions', view_func=ShowRoles.as_view('permissions'))
            self.server.add_url_rule('/change_permissions/<role_id>', view_func=ChangePermissions
                                     .as_view('change_permissions'))
            self.server.add_url_rule('/settings', view_func=StudentSettings
                                     .as_view('settings'))
            self.server.add_url_rule('/assign_criterias/<student_id>', view_func=AssignCriterias
                                     .as_view('assign_criterias'))
            self.server.add_url_rule('/create_request', view_func=CreateRequest.as_view('create_request'))
            self.server.add_url_rule('/remove_request/<request_id>', view_func=RemoveRequest.as_view('remove_request'))
            self.server.add_url_rule('/request/<request_id>', view_func=ShowRequest.as_view('show_request'))
            self.server.add_url_rule('/student_requests', view_func=ShowRequests.as_view('student_requests'))
            self.server.add_url_rule('/all_requests', view_func=RequestList.as_view('all_requests'))
            self.server.add_url_rule('/edit_request/<request_id>', view_func=EditRequestStatus.as_view('change_request'))
