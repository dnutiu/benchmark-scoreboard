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
import sqlalchemy_utils

db = SQLAlchemy()


class Result(db.Model):
    """
        The result model will store benchmark results.
    """
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(50))
    gpu = db.Column(db.String(256))
    cpu = db.Column(db.String(256))
    log = db.Column(db.Text)
    score = db.Column(db.Integer, index=True)
    ip = db.Column(sqlalchemy_utils.IPAddressType)

    def __init__(self, name="Anonymous", gpu=None, cpu=None, log=None, ip=None, score=1):
        self.name = name
        self.gpu = gpu
        self.cpu = cpu
        self.log = log
        self.score = score
        self.ip = ip

    def __repr__(self):
        return self.gpu

    __table_args__ = (
        db.CheckConstraint(score > 0, name="positive_score_constraint"),
        {}
    )
