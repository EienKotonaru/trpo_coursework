from flask import Flask, render_template, request

from src.views import CreateGroup, GroupsList, Menu, CreateCriteria, CreateValues, Registration, Login, Logout, \
    ProfileLoader


class Application:
    def __init__(self, port):
        self.port = port
        self.server = Flask(__name__, static_url_path='/static')
        self.server.url_map.strict_slashes = False

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
            self.server.add_url_rule('/add_values/<group_id>', view_func=CreateValues.as_view('new_values'))
