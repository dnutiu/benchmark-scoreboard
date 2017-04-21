# scoreboard-benchmark 

![Travis CI](https://travis-ci.com/Metonimie/benchmark-scoreboard.svg?token=A1YGCrBhxwT3nHmAHZ9Q&branch=master)

This is a simple web app used for an university projects.

You will need **Python 2.6+ or Python 3.3+**  to run this app.
Flask doesn't support Python 3.2.

It should provide a simple score board display
for some benchmarking data which is gathered from another application.

## Installing

To install and run the application, you must do the following:

Rename the config.lock.py to config.py, so you can safely modify the config.py and still have
config.lock.py as a template.
and update the file to match your configuration settings.

Then run:

```bash
pip install -r requirements.txt
python setup.py install
python application.py
```
You may set BSFLASK_ENV environment variable to production, development or testing.
### Running Tests

In the root directory, run the following command:

```bash
python -m unittest
```
