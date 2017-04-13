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
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Result(db.Model):
    """
        The result model will store benchmark results.
    """
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    gpu = db.Column(db.String(256))
    cpu = db.Column(db.String(256))
    log = db.Column(db.String(4086))
    score = db.Column(db.Integer)

    def __init__(self, gpu=None, cpu=None, log=None, score=0):
        self.gpu = gpu
        self.cpu = cpu
        self.log = log
        self.score = score

    def __repr__(self):
        return self.text
