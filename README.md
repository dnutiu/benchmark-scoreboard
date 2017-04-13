# scoreboard-benchmark 

This is a simple web app used for an university projects.

It should provide a simple score board display
for some benchmarking data which is gathered from another application.

## Posting data

For now, you can post data using curl.

'''
curl -H "Content-Type: application/json" -X POST -d '{"text":"Hello Darkness","score": 5000}' http://localhost:5000/upload
'''

## Requires:

* nosetests
* flask
* mysql

## Milestones:

1. Make simple view which displays benchmarks
2. Add user registration
3. Perfect
