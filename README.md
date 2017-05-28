# scoreboard-benchmark 

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5898b8005f634dc48c611a3c3337d30e)](https://www.codacy.com/app/Metonimie/benchmark-scoreboard?utm_source=github.com&utm_medium=referral&utm_content=Metonimie/benchmark-scoreboard&utm_campaign=badger)

![Travis CI](https://travis-ci.com/Metonimie/benchmark-scoreboard.svg?token=A1YGCrBhxwT3nHmAHZ9Q&branch=master)

This is a simple web app that I've build for an university projects.
It is supposed to retrieve and store results from outside and present them in a nice way.
The results are benchmarking tests that are run by the java application.

You will need **Python 3.3+**  to run this app.
Flask doesn't support Python 3.2 and some packages won't work with Python 2 but you may get it running with some tweaks.

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
python application.py
```
You may set BSFLASK_ENV environment variable to production, development or testing.
### Running Tests

In the root directory, run the following command:

```bash
python -m unittest
```
