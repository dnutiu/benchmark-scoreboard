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
import src.resources.utilities as ut
import unittest


class UtilitiesTestCase(unittest.TestCase):

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
        import os
        self.assertEqual(ut.get_env_variable("TESTING", "false"), 'false')
        os.environ['TESTING'] = 'True'
        self.assertEqual(ut.get_env_variable("TESTING", "false"), 'True')