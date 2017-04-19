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
from src.models import db, Result
from src.application import create_app
import unittest
import os
import json


class ScoreboardTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.drop_all()
        os.remove("src/test_database.sqlite")
        self.app_context.pop()

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_not_found(self):
        response = self.client.get("/404notfound")
        self.assertEqual(response.status_code, 404)

    def test_entry(self):
        response = self.client.get("/result/1")
        self.assertEqual(response.status_code, 404)

        data = Result(cpu="TestCPU", gpu="TestGPU", log="TestLOG")
        db.session.add(data)
        db.session.commit()

        response = self.client.get("/result/1")
        self.assertEqual(response.status_code, 200)

    def test_add_entry(self):
        data = dict(
            name="Test",
            gpu="CpuTesting2",
            cpu="GPUTesting2",
            log="This is a logfile",
            score=200
        )
        response = self.client.post('/result', data=json.dumps(data), content_type='application/json')

        self.assertTrue("true" in response.get_data(as_text=True))
        self.assertEqual(response.status_code, 201)

    def test_search(self):
        e = Result(name="Test", cpu="TestCPU", gpu="TestGPU", log="TestLOG", score=11)
        response = self.client.post('/', data={"result_name": "test"})
        self.assertTrue("No results found" in response.get_data(as_text=True))

        db.session.add(e)
        db.session.commit()

        response = self.client.post('/', data={"result_name": "test"})
        self.assertFalse("No results found" in response.get_data(as_text=True))

    def test_get_upload(self):
        response = self.client.get('/upload')
        self.assertEqual(response.status_code, 200)

    def test_pagination(self):
        data1 = Result(cpu="TestCPU", gpu="TestGPU", log="TestLOG", score=11)
        data2 = Result(cpu="TestCPU", gpu="TestGPU", log="TestLOG", score=22)
        data3 = Result(cpu="TestCPU", gpu="TestGPU", log="TestLOG", score=33)

        response = self.client.get("/")
        self.assertTrue("No results found" in response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

        db.session.add(data1)
        db.session.commit()

        response = self.client.get("/?page=1")
        self.assertTrue("11" in response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

        db.session.add(data2)
        db.session.commit()

        response = self.client.get("/?page=2")
        self.assertTrue("11" in response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

        db.session.add(data3)
        db.session.commit()

        response = self.client.get("/?page=3")
        self.assertTrue("11" in response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
