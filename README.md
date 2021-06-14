# Coding Challenge App

Completed By Hassam Solano-Morel

## Install:

### Using a virtual env
You can use a virtual environment (venv):
```
source activate bin/activate
```

### On Host machine with Python 3.6+ (no virtual environment)
Just pip install from the requirements file
```
pip install -r requirements.txt
```

### Using Docker Compose
```
docker-compose build
```

## Running the code

### Using Docker Compose
```
# start up docker container
docker-compose up
```

### Spin up the service on Host machine
If you're using a virtual environment, be sure you've completed the appropriate install instructions
```
# start up local server
python -m run
```


## Running Tests
To make running tests more efficient VCRpy has been included as part of the testing suite, along with HTTP recordings for appropriate tests. Check out the link in `app/tests/contracttests/base.py` if you're curious on how VCRpy works (it is a pretty sweet library).

### On Host machine
```
pytest --cov
```

### Using Docker Compose
```
docker-compose -f docker-compose-tests.yml
```

## Making Requests
Regardless of which method you chose for running the service the following `host:port` combination should work for making calls:
```
curl -i "http://127.0.0.1:5000/health-check"
```

## Note Worthy Endpoints
[GET] `/profile/<org_name>` : Get a unified code base stats summary for a given user/orgization/team. Currently supported data sources are Github and Bitbucket. Check out the docstring in `app/routes.py:get_profile_for` for details on query params (hint you're gonna need a Github access token).

## What'd I'd like to improve on...
1. Hitting the `/profile/<org_name>` endpoint  with a user that does not exist at a datasource can cause the whole request to fail. This doesn't sound right.
2. Upgrade to Python3.7+. This would enable AsyncIO to more easily play along with Flask. When using Python3.6, Flask views do not support being defined using `async` and thus can't use the `await` keywords. Using coroutines to run external call (especially to the Github API) would significantly improve the performance of `/profile/<org_name>`
