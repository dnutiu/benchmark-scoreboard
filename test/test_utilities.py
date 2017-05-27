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
import src.resources.utilities as ut
import src.application
import unittest
import os


class UtilitiesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = src.application.create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.drop_all()
        os.remove("src/test_database.sqlite")
        self.app_context.pop()

    def test_to_zero_count(self):
        r = ut.to_zero_count(2)
        self.assertEqual(1, r)

        r = ut.to_zero_count(0)
        self.assertEqual(0, r)

        r = ut.to_zero_count('asd')
        self.assertEqual(0, r)

        r = ut.to_zero_count(True)
        self.assertEqual(0, r)

        r = ut.to_zero_count(-100)
        self.assertEqual(0, r)

        r = ut.to_zero_count(10.52)
        self.assertEqual(9, r)

    def test_get_environment_variable(self):
        self.assertEqual(ut.get_env_variable("TESTING", "false"), 'false')
        os.environ['TESTING'] = 'True'
        self.assertEqual(ut.get_env_variable("TESTING", "false"), 'True')

    def test_get_highest_score(self):
        with self.assertRaises(LookupError):
            ut.get_highest_score()

        data1 = Result(cpu="TestCPU", gpu="TestGPU", log="TestLOG", score=11)

        db.session.add(data1)
        db.session.commit()

        score = ut.get_highest_score()
        self.assertEqual(score, 11)

        data2 = Result(cpu="TestCPU", gpu="TestGPU", log="TestLOG", score=24)

        db.session.add(data2)
        db.session.commit()

        score = ut.get_highest_score()
        self.assertEqual(score, 24)

    def test_get_progress_bar_score(self):
        data1 = Result(score=100)

        db.session.add(data1)
        db.session.commit()

        score = ut.get_progress_bar_score(50)
        self.assertEqual(score, 50)

    def test_get_progress_bar_class(self):
        data1 = Result(score=100)

        db.session.add(data1)
        db.session.commit()

        success = ut.get_progress_bar_class(80)
        self.assertEqual("progress-bar-success", success)

        warn = ut.get_progress_bar_class(49)
        self.assertEqual("progress-bar-warning", warn)

        danger = ut.get_progress_bar_class(24)
        self.assertEqual("progress-bar-danger", danger)
