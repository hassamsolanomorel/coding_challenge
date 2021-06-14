# Coding Challenge App

Completed By Hassam Solano-Morel

## Get Things Running!

### Using virtualenv
From the project root run:
```
# Create virtual environment.
# Path to python3.6 is only required if your system's python version is
#  less than 3.6. Otherwise the flag can be skipped.
virtualenv -p=<PATH/TO/PYTHON3.6> .env

# Activate the environment
source .env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the service
python -m run

# Run Tests
pytest --cov
```

### On Host machine with Python 3.6+ (no virtual environment)
From the project root run:
```
# Install dependencies
pip install -r requirements.txt

# Run the service
python -m run

# Run Tests
pytest --cov
```

### Using Docker Compose
From the project root run:
```
# Install dependencies & Run the service
docker-compose up

# Run Tests
docker-compose -f docker-compose-tests.yml up
```

## Note on Running Tests
To make running tests more efficient VCRpy has been included as part of the testing suite, along with HTTP recordings for appropriate tests. Check out the link in `app/tests/contracttests/base.py` if you're curious on how VCRpy works (it is a pretty sweet library).

If you'd like to re-record tests, you'll need to replace the access_token specified in `app/tests/contracttests/base.py` as noted in the included comments.

## Making Requests
Regardless of which method you chose for running the service the following `host:port` combination should work for making calls:
```
curl -i "http://127.0.0.1:5000/health-check"
```

## Note Worthy Endpoints
[GET] `/profile/<org_name>` : Get a unified code base stats summary for a given user/orgization/team. Currently supported data sources are Github and Bitbucket. Check out the docstring in `app/routes.py: get_profile_for` for details on query params (hint you're gonna need a Github access token).

## What'd I'd like to improve on...
1. Hitting the `/profile/<org_name>` endpoint  with a user that does not exist at a datasource can cause the whole request to fail. This doesn't sound right.
2. Upgrade to Python3.7+. This would enable AsyncIO to more easily play along with Flask. When using Python3.6, Flask views do not support being defined using `async` and thus can't use the `await` keywords. Using coroutines to run external calls (especially to the Github API) concurrently would significantly improve the performance of `/profile/<org_name>`.
3. Implement proper secret keeping. It would be nice to not depend on the client to pass in their own access_token. Properly implemented secret keeping using something like Hashi Corp's Vault would be a more appropriate approach for preparing this service for production.
4. For the Bitbucket data source I was unable to figure out a way to distinguish between original repos vs forked repos. For this reason ALL Bitbucket repos count towards the `total_repos` value but NOT for either of `num_original_repos` or `num_forked_repos`.
