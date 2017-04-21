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
from src.config import ProductionConfig
import multiprocessing

bind = "{ip}:{port}".format(ip=ProductionConfig.BIND_IP, port=ProductionConfig.BIND_PORT)
workers = multiprocessing.cpu_count() * 2 + 1
reload = False
#daemon = True
#user = "denis"
#group = "www-data"