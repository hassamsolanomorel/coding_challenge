# Python Imports
import logging
import json
# 3rd Party Imports
import flask
from flask import Flask
from flask import Response

# Project Imports
from app.datasources.github import GitHubProfile
from app.datasources.bitbucket import BitBucketProfile

app = Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)


@app.route("/profile/<org_name>", methods=["GET"])
def get_profile_for(org_name: str):
    """
    Endpoint to health check API
    """
    app.logger.info(f"{org_name}")
    # Github stuff
    gh_user = GitHubProfile(org_name)
    gh_profile = gh_user.get_profile_summary()

    # Bitbucket stuff
    bb_user = BitBucketProfile(org_name)
    bb_profile = bb_user.get_profile_summary()

    unified_profile = {}

    for k, v in gh_profile.items():
        unified_profile[k] = gh_profile[k]
        if type(gh_profile[k]) is dict:
            continue
        if bb_profile[k]:
            unified_profile[k] += bb_profile[k]

    return Response(json.dumps(unified_profile),
                    status=200)
