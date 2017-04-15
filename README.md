# scoreboard-benchmark 

This is a simple web app used for an university projects.

It should provide a simple score board display
for some benchmarking data which is gathered from another application.

## Installing

To install and run the application, you must do the following:

First, rename the config.lock.py to config.py
and update the file to match your configuration settings.

Then run:

```bash
python3 setup.py install
nohup python3 application.py &
```

### Running Tests

In the root directory, run the following command:

```bash
python -m unittest
```

## Posting data

You can post data using curl. There are no restrictions on whoever can post data.

```bash
curl -H "Content-Type: application/json" -X POST -d '{"gpu":"GPU DUMMY TEXT","cpu":"CPU DUMMY TEXT","log":"DETAILED LOG","score": 1}' http://localhost:5000/upload
```

## Milestones:

1. Make simple view which displays benchmarks. [Done 13 Apr 2017]
    * Improve design [Done]
    * Add about us page [?]
    * Try to use a mysql database
2. Add user registration
3. Perfect
