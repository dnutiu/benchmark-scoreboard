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
from src.models import Result
from src.models import db
import json
import math
import flask

scoreboard = flask.Blueprint('scoreboard', __name__, template_folder='templates')


@scoreboard.route("/upload", methods=['POST', 'GET'])
def upload():
    """
    This is the upload view. It accepts JSON only.

    Returns:
        This method returns a JSON object with tree variables
        status code, success true if the data was received successfully and false otherwise and
        an error string.
    """
    if flask.request.method == 'GET':
        return flask.render_template('upload.html')

    content = flask.request.get_json()

    try:
        gpu = content['gpu']
        cpu = content['cpu']
        log = content['log']
        score = int(content['score'])
    except KeyError:  # Json doesn't contain the keys we need.
        error = "invalid json keys: gpu, cpu, log, score"
        return json.dumps({'error': error, 'success': False}), 400, {'ContentType': 'application/json'}
    except TypeError:  # The types from the json object are not correct.
        error = "invalid json object"
        return json.dumps({'error': error, 'success': False}), 400, {'ContentType': 'application/json'}

    # Add data to the database
    entry = Result(gpu=gpu, cpu=cpu, log=log, score=score)
    db.session.add(entry)
    db.session.commit()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@scoreboard.route("/entry/<id>")
def entry(id):
    """
        The entry view display an entry based on it's ID.
        The entry is retrieved from the database and the ID is a primary key for the entry.
    """
    entry_name = Result.query.filter_by(id=id).first()
    if entry_name:
        return flask.render_template("entry.html", name=entry_name)

    flask.abort(404)


@scoreboard.route("/")
def index():
    """
        This method returns the index page.
    """
    results_per_page = flask.current_app.config["MAX_RESULTS_PER_PAGE"]
    max_pages = flask.current_app.config["MAX_PAGES"]
    results = Result.query.order_by(Result.score.desc()).all()

    #  We're extracting the page argument from the url, if it's not present we set page_no to zero.
    page_no = flask.request.args.get('page')
    try:
        page_no = int(page_no) - 1
        if page_no < 0: page_no = 0
    except (TypeError, ValueError):  # page_no is not an int
        page_no = 0

    offset = page_no * results_per_page
    available_pages = math.floor((len(results) - offset) / results_per_page)

    # Compute the available pages to the left
    pages_left = min(page_no, max_pages)
    # Compute the available pages to the right
    pages_right = min(max_pages, available_pages)
    # Create pagination information tuple
    pagination_information = len(results), results_per_page, page_no + 1, pages_left, pages_right

    return flask.render_template("index.html",
                                 results=results[offset:offset + results_per_page],
                                 pagination=pagination_information)
