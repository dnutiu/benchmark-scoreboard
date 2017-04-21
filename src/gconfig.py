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
    
    This the configuration file for the GUnicorn server.
"""
import multiprocessing
import os

# If BSFLASK_ENV is development or environment then gunicorn will bind to Config.APP_IP and Config.APP_PORT
# else it will create a unix socket benchmark_scoreboard.sock that may be used by Nginx
configuration = None
try:
    configuration = os.environ['BSFLASK_ENV']
except KeyError:
    print("Environment key BSFLASK_ENV not defined.")

if configuration is not None and configuration == 'production':
    bind = "unix:benchmark_scoreboard.sock"
else:
    from src.config import Config
    bind = "{ip}:{port}".format(ip=Config.BIND_IP, port=Config.BIND_PORT)

workers = multiprocessing.cpu_count() * 2 + 1
reload = False
# Allow access to name and group.
umask = 0x007
