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
from src.models import Result, db
from src.resources import utilities
import math
import flask

scoreboard = flask.Blueprint('scoreboard', __name__, template_folder='templates')


@utilities.cache.cached(timeout=60*10)
@scoreboard.route("/upload")
def upload():
    """
        Returns a page containing instructions on how to upload things.
    """
    return flask.render_template('upload.html')


@scoreboard.route("/result", methods=['GET'])
def result_get():
    """
    Instead of method not allowed we redirect to scoreboard.upload
    """
    return flask.redirect(flask.url_for('scoreboard.upload'))


@scoreboard.route("/result", methods=['POST'])
def result_post():
    """
    Allows the upload of resources via POST.
    """
    try:
        content = flask.request.get_json()

        name = content['name']
        gpu = content['gpu']
        cpu = content['cpu']
        log = content['log']
        score = int(content['score'])
        if score <= 0:
            raise ValueError("Score must be positive!")
    except KeyError as e:  # Json doesn't contain the keys we need.
        error = "Key not found: {}.".format(str(e))
    except TypeError as e:  # If we don't get a string
        error = str(e)
    except ValueError as e:
        error = str(e)
    else:
        # Add data to the database
        entry = Result(name=name, gpu=gpu, cpu=cpu, log=log, score=score)
        db.session.add(entry)
        db.session.commit()

        flask.current_app.logger.info("{} added result with id: {}.".format(flask.request.remote_addr, entry.id))

        location = "/result/{}".format(entry.id)

        return flask.jsonify({'success': True}), 201, {'location': location}
    # Exception occurred
    return flask.jsonify({'error': error, 'success': False}), 400


@utilities.cache.cached(timeout=60*5)
@scoreboard.route("/result/<id>", methods=['GET'])
def result(id):
    """
    Fetches an entry from the database and displays it in a view.
    The entry is retrieved from the database and the ID is a primary key for the entry.
    """
    entry_name = Result.query.filter_by(id=id).first()
    if entry_name:
        progress_bar_data = dict()
        progress_bar_data['value'] = utilities.get_progress_bar_score(entry_name.score)
        progress_bar_data['class'] = utilities.get_progress_bar_class(entry_name.score)
        return flask.render_template("result.html", name=entry_name, progress_bar=progress_bar_data)
    else:
        flask.abort(404)


@utilities.cache.cached(timeout=60)
@scoreboard.route("/", methods=['GET', 'POST'])
def index():
    """
    This method returns the index page.
    """
    results_per_page = flask.current_app.config["MAX_RESULTS_PER_PAGE"]
    max_pages = flask.current_app.config["MAX_PAGES"]

    # We're extracting the page argument from the url, if it's not present we set page_no to zero.
    page_no = utilities.to_zero_count(flask.request.args.get('page'))
    searched_name = flask.request.args.get('result_name')

    # The filters dictionary is used to filter the data
    filters = {}
    if searched_name is not None and searched_name is not '':
        filters['name'] = searched_name

    # Computing the offset for the results
    offset = page_no * results_per_page

    # We're getting the results length and data
    results_length = Result.query.filter_by(**filters).count()
    results = Result.query.filter_by(**filters).order_by(Result.score.desc()).offset(offset).limit(results_per_page)

    # This is used by the view to display available pages, if any.
    available_pages = math.floor((results_length - offset) / results_per_page)

    # Compute the available pages to the left
    pages_left = min(page_no, max_pages)
    # Compute the available pages to the right
    pages_right = min(max_pages, available_pages)
    # Create pagination information tuple
    pagination_information = results_length, results_per_page, page_no + 1, pages_left, pages_right

    return flask.render_template("index.html",
                                 results=results,
                                 pagination=pagination_information)
