# scoreboard-benchmark 

This is a simple web app used for an university projects.

It should provide a simple score board display
for some benchmarking data which is gathered from another application.

## Installing

First, rename the config.lock.py to config.py
and update the file to match your configuration settings.

Then run:

```
python3 setup.py install
nohup python3 application.py &
```

## Posting data

For now, you can post data using curl.

```
curl -H "Content-Type: application/json" -X POST -d '{"text":"Hello Darkness","score": 5000}' http://localhost:5000/upload

```

## Milestones:

1. Make simple view which displays benchmarks. [Done 13 Apr 2017]
    * Improve design
    * Add about us page
    * Try to use a mysql database
2. Add user registration
3. Perfect
