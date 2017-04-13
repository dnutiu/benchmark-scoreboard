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
import flask

scoreboard = flask.Blueprint('scoreboard', __name__, template_folder='templates')


@scoreboard.route("/upload", methods=['POST'])
def upload():
    content = flask.request.get_json()
    try:
        text = flask.escape(content['text'])
        score = int(content['score'])
    except KeyError:  # Json doesn't contain the keys we need.
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
    except TypeError: # The types from the json object are not correct.
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    entry = Result(text=text, score=score)
    db.session.add(entry)
    db.session.commit()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@scoreboard.route("/entry/<id>")
def entry(id):
    entry_name = Result.query.filter_by(id=id).first()
    if entry_name:
        return flask.render_template("entry.html", name=entry_name)

    flask.abort(404)

@scoreboard.route("/")
def index():
    results = Result.query.order_by(Result.score.desc()).all()
    return flask.render_template("index.html", results=results)
