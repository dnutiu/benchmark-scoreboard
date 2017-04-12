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
from setuptools import setup, find_packages

long_description = open("README.md").read()

setup(
    name="scoreboard-benchmark",
    version="0.1",
    packages=find_packages(),
    long_description=long_description,
    install_requires=[
        'flask>=0.12.1',
        'flask-bootstrap'
    ],
    author="Denis Nutiu",
    author_email="denis.nutiu@gmail.com",
    description="This is a simple web applications that displays scores",
    license="GPLv3",
    keywords="flask benchmark scores ",
    url="N/a",
)