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
import os
import logging
import tempfile
from logging.handlers import SysLogHandler
from src.models import db

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
        This class contains general configuration settings that are available everywhere.
        You may edit this class and the ProductionConfig class if you wish to deploy.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DEBUG = True
    # Server Settings
    ADMIN_EMAIL = "metonymy@fedoraproject.org"
    ADMIN_NAME = "Metonymy"
    BIND_IP = ""
    BIND_PORT = 5000
    CACHE_TYPE = "memcached"
    CACHE_DEFAULT_TIMEOUT = 60
    CACHE_KEY_PREFIX = "benchmark_scoreboard"
    # Pagination
    MAX_RESULTS_PER_PAGE = 50
    MAX_PAGES = 2

    # Unix logging settings
    syslog_handler = SysLogHandler()
    syslog_handler.setLevel(logging.WARNING)

    @staticmethod
    def init_app(app):
        app.logger.addHandler(Config.syslog_handler)


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
    CACHE_TYPE = "filesystem"
    CACHE_DIR = tempfile.gettempdir()

    @staticmethod
    def init_app(app):
        app.logger.addHandler(Config.syslog_handler)
        with app.app_context():
            db.create_all()


class ProductionConfig(Config):
    BOOTSTRAP_USE_MINIFIED = True
    DEBUG = False
    #  Database Configuration
    MYSQL_USERNAME = os.environ.get("BSFLASK_MYSQL_USERNAME", None)
    MYSQL_PASSWORD = os.environ.get("BSFLASK_MYSQL_PASSWORD", None)
    MYSQL_HOSTNAME = os.environ.get("BSFLASK_MYSQL_HOSTNAME", None)
    MYSQL_DATABASE = os.environ.get("BSFLASK_MYSQL_DATABASE", None)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{hostname}/{database}'\
        .format(username=MYSQL_USERNAME, password=MYSQL_PASSWORD,
                hostname=MYSQL_HOSTNAME, database=MYSQL_DATABASE)

    @staticmethod
    def init_app(app):
        app.logger.addHandler(Config.syslog_handler)
        with app.app_context():
            db.create_all()


class TestingConfig(Config):
    MAX_RESULTS_PER_PAGE = 1
    CACHE_TYPE = "null"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test_database.sqlite')

    @staticmethod
    def init_app(app):
        app.logger.addHandler(Config.syslog_handler)
        with app.app_context():
            db.drop_all()
            db.create_all()

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
