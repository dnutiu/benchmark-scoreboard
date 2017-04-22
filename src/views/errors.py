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
import flask

error_pages = flask.Blueprint('error_pages', __name__, template_folder='templates')

report_string = "===============\n" \
                "{headers}" \
                "Path: {path}\n" \
                "Ip: {ip}\n" \
                "Message: {message}\n"


@error_pages.app_errorhandler(404)
def page_not_found_error(e):
    error = report_string.format(headers=flask.request.headers, ip=flask.request.remote_addr,
                                 message=e, path=flask.request.path)
    flask.current_app.logger.info(error)
    return flask.render_template("404.html"), 404


@error_pages.app_errorhandler(500)
def internal_server_error(e):
    error = report_string.format(headers=flask.request.headers, ip=flask.request.remote_addr,
                                 message=e, path=flask.request.path)
    flask.current_app.logger.error(error)
    return flask.render_template("500.html"), 500


@error_pages.app_errorhandler(405)
def method_not_allowed_error(e):
    error = report_string.format(headers=flask.request.headers, ip=flask.request.remote_addr,
                                 message=e, path=flask.request.path)
    flask.current_app.logger.warning(error)
    return flask.render_template("405.html"), 405


@error_pages.app_errorhandler(400)
def bad_request_error(e):
    error = report_string.format(headers=flask.request.headers, ip=flask.request.remote_addr,
                                 message=e, path=flask.request.path)
    flask.current_app.logger.info(error)
    return flask.render_template("400.html"), 400
