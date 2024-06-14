import os

from flask import Flask
from datetime import datetime
from pony.flask import Pony
from pony.orm import Database, LongStr, PrimaryKey, Required, Set, Optional, db_session

# from flask_socketio import SocketIO, emit

# from flask_restful import Resource, Api
# Define database and entities
db = Database()


class InvoiceItem(db.Entity):
    id = PrimaryKey(int, auto=True)
    file_name = Required(str)
    upload_date = Required(datetime)
    rows_count = Required(int)
    invoice = Set('Invoice')


class Invoice(db.Entity):
    id = PrimaryKey(int, auto=True)
    invoice_item = Required(InvoiceItem)


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)
    password = Required(str)
    posts = Set('Post')
    role = Optional('Role')


class Role(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    access_flags = Optional(str, default='r')
    users = Set(User)
    role_routes = Set('RoleDenyRoute')


class RoleDenyRoute(db.Entity):
    id = PrimaryKey(int, auto=True)
    route = Required(str)
    role = Optional(Role)


class Post(db.Entity):
    _table_ = 'post'

    id = PrimaryKey(int, auto=True)
    author_id = Required(User)
    created = Required(datetime, default=lambda: datetime.now())
    title = Required(str)
    body = Required(LongStr)


def create_app(test_config=None) -> Flask:
    """
    Create and configure an instance of the Flask application.
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # A default secret that should be overridden by instance config
        # DO NOT USE THIS SECRET KEY FOR PRODUCTION!!!
        SECRET_KEY="dev",
        # store the database in the instance folder
        # PONY={'provider': 'sqlite',
        #       'filename': os.path.join(app.instance_path, "pony_blog.db"),
        #       'create_db': True}
        PONY={'provider': 'mysql', 'host': '127.0.0.1', 'user': 'root', 'passwd': 'qwerty', 'db': 'web11'}
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Wrap application requests with Pony's db_session
    Pony(app)

    # Generate database schema mapping
    db.bind(**app.config['PONY'])
    db.generate_mapping(create_tables=True)

    # Apply the blueprints to the app
    from . import auth
    # from . import blog
    from . import dashboard
    from . import cover
    from . import main
    from . import main_invoices
    from . import main_books
    from . import main_distributions
    from . import main_forecast
    from . import main_reports

    app.register_blueprint(auth.bp)
    # app.register_blueprint(blog.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(cover.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(main_invoices.bp)
    app.register_blueprint(main_books.bp)
    app.register_blueprint(main_distributions.bp)
    app.register_blueprint(main_forecast.bp)
    app.register_blueprint(main_reports.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")
    #
    # api = Api(app)
    # api.add_resource(auth.api_register, '/api/register')

    # app_socketio = SocketIO(app, async_mode='threading')

    # if __name__ == '__main__':
    #     socketio.run(app, debug=True)
    return app
