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
import flask
import json
import os


#  General Configurations
app = flask.Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db.init_app(app)


@app.before_first_request
def create_test_databases():
    db.drop_all()
    db.create_all()
    b1 = Result(text="asda", score=100)
    b2 = Result(text="i7 flips flops", score=400)
    db.session.add(b1)
    db.session.add(b2)
    db.session.commit()


@app.route("/upload", methods=['POST'])
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


@app.route("/")
def index():
    results = Result.query.all()
    return flask.render_template("index.html", results=results)


@app.errorhandler(404)
def page_not_found_error(e):
    return flask.render_template("404.html"), 404

if __name__ == "__main__":
    app.run("0.0.0.0")
