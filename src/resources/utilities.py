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
from flask_cache import Cache
import os

cache = Cache()


def to_zero_count(page_no):
    """
    Will subtract 1 from the argument it gets, converting it to an int.
    If the conversion fails or the argument it's negatives it returns zero instead.
    >>> to_zero_count(3)
    2
    >>> to_zero_count('a')
    0

    Args:
        page_no: An integer

    Returns:
        It returns page_no - 1 if page_no can be safely converted to an integer else it returns zero.
        If page_no is negative, it returns zero.

    """
    try:
        page_no = int(page_no) - 1
        if page_no < 0:
            page_no = 0
    except (TypeError, ValueError):  # page_no is not an int
        page_no = 0
    return page_no


def get_env_variable(variable, fallback):
    """
    Will try to retrieve the environment variable from the system and if it fails
    it returns the fallback value.
    
    Args:
        variable: The environment variable that should be retrieved
        fallback: The default return value in case the environment variable is not retrieved
    
    Returns:
        On success is returns the variable's value from the environment, on failure it returns the
        value provided by fallback

    >>> get_env_variable('HOMES', 'fallback')
    'fallback'
    
    >>> import os
    >>> os.environ['TEST'] = '13'
    >>> get_env_variable("TEST", "14")
    '13'
    
    """
    try:
        return os.environ[variable]
    except KeyError:
        return fallback


@cache.memoize(60*5)
def get_highest_score():
    """
    Will retrieve the result that has the highest score from the database.
    
    Returns:
        The score of the highest rated result else it raises an exception.
    
    Raises:
        LookupError if the database is empty.
    """
    result = Result.query.order_by(Result.score.desc()).first()
    if result:
        # If we return zero then we're going to have a problem
        if result.score > 0:
            return result.score
        else:
            return 1
    else:
        raise LookupError("The database is empty.")


@cache.memoize(60*5)
def get_progress_bar_score(current):
    """
    Will compute the procent of the highest score compared to the current score.
    
    Args:
        current - The result with the current score.
    
    Returns:
        The computed score, if it's greater than %100 then returns 100.
    """
    highest = get_highest_score()
    score = (current * 100) / highest
    if score > 100:
        return 100.0
    else:
        return score


@cache.memoize(60*5)
def get_progress_bar_class(score):
    """
    Returns the Boostrap class for the progress-bar based on the score.
    """
    highest = get_highest_score()
    if score > highest / 2:
        return 'progress-bar-success'
    elif score > highest / 4:
        return 'progress-bar-warning'
    else:
        return 'progress-bar-danger'
