"""
    Author: Denis Nutiu <denis.nutiu@gmail.com>
    This file is part of scoreboard-benchmark.

    scoreboard-benchmark  is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    scoreboard-benchmark  is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with scoreboard-benchmark .  If not, see <http://www.gnu.org/licenses/>.
"""
try:  # This is mainly required for Travis CI automated testing.
    from src.config import config
except ImportError:
    from src.config_lock import config

from src.models import db
from src.views.errors import error_pages
from src.views.scoreboard import scoreboard
from src.resources.utilities import cache
import os
import flask_bootstrap
import flask


def create_app(config_name):
    app = flask.Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    cache.init_app(app)
    config[config_name].init_app(app)
    flask_bootstrap.Bootstrap(app)
    app.register_blueprint(scoreboard)
    app.register_blueprint(error_pages)

    return app

try:
    configuration = os.environ['BSFLASK_ENV']
    print("Running with configuration: " + configuration)
    app = create_app(configuration)
except (IndexError, KeyError):
    print("Using default configuration.")
    app = create_app('default')


if __name__ == "__main__":
    app.run(app.config["BIND_IP"], app.config["BIND_PORT"])
