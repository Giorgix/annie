import flask
from flask.ext.sqlalchemy import SQLAlchemy


app = flask.Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
db = SQLAlchemy(app)


from annie.api.users.views import UserApi

user_blueprint = flask.Blueprint('user', __name__)

user_api_view = UserApi.as_view('user_api')
user_blueprint.add_url_rule(
    '/users/',
    defaults={'user_id': None},
    view_func=user_api_view,
    methods=['GET']
)
user_blueprint.add_url_rule(
    '/users/',
    view_func=user_api_view,
    methods=['POST']
)
user_blueprint.add_url_rule(
    '/users/<int:user_id>/',
    view_func=user_api_view,
    methods=['GET', 'PUT', 'DELETE']
)


app.register_blueprint(user_blueprint)
