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
import math
import flask

scoreboard = flask.Blueprint('scoreboard', __name__, template_folder='templates')


@scoreboard.route("/upload")
def upload():
    """
        Returns a page containing instructions on how to upload things.
    """
    return flask.render_template('upload.html')

# @scoreboard.route("/result", methods=['GET'])
# def result_get():
#     """
#     Instead of method not allowed we redirect to scoreboard.upload
#     """
#     return flask.redirect(flask.url_for('scoreboard.upload'))


@scoreboard.route("/result", methods=['POST'])
def result_post():
    """
    Allows the upload of resources via POST.
    """
    content = flask.request.get_json()
    error = None
    gpu = cpu = log = score = None

    try:
        gpu = content['gpu']
        cpu = content['cpu']
        log = content['log']
        score = int(content['score'])
    except KeyError:  # Json doesn't contain the keys we need.
        error = "invalid json keys: gpu, cpu, log, score"
    except TypeError:  # The types from the json object are not correct.
        error = "invalid json object"

    if error:
        return flask.jsonify({'error': error, 'success': False}), 400

    # Add data to the database
    entry = Result(gpu=gpu, cpu=cpu, log=log, score=score)
    db.session.add(entry)
    db.session.commit()

    location = "/result/{}".format(entry.id)

    return flask.jsonify({'success': True, 'location': location}), 201, {'location': location}


@scoreboard.route("/result/<id>", methods=['GET'])
def result(id):
    """
    Fetches an entry from the database and displays it in a view.
    The entry is retrieved from the database and the ID is a primary key for the entry.
    """
    entry_name = Result.query.filter_by(id=id).first()
    if entry_name:
        return flask.render_template("result.html", name=entry_name)
    else:
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
        if page_no < 0:
            page_no = 0
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
