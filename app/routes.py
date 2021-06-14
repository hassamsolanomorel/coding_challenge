"""
Package: app
Filename: routes.py
Author(s): Hassam S, DivvyDose Team

Define service routes

Author's Note:
    For a small service having one route.py module works. However for larger
    projects we will want to break up where we define our endpoints. An example
    file structure that could work:
        /app
            /v1
                /endpoints
                    /health_check.py
                    /profile.py
                    /etc ...
                /utils
                /<any other appropriate dir related to v1>
            /v2
                /...
    This structure would allow us to:
        1) More easly organize/group our endpoints based http resource
        2) Sets up a structure that will be easier to navigate as new service
            versions are created.
        3) We can use Python introspection to define endpoints URIs, so clients
            would hit something like: '/v1/profile/<org_name>'. This has the
            advantage of allowing our service to support multiple API
            versions at the same time. This would be VERY handy especially when
            transitioning the service to a new API version. Endpoints can be
            transitioned and tested without sunsetting older versions.

"""
# Python Imports
import json
# 3rd Party Imports

from flask import Response
from flask import request

# Project Imports
import app.datasources as d_sources
from app.utils.profile_utils import merge_profiles


def configure_routes(app):

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
        Endpoint to get a combined profile for a given orgnization/team/user
        PARAMS: org_name: string - The name of the orgnization/team/user
        VALID_QUERY_PARAMS:
            1. (REQUIRED) access_token: string - Github access token. Needed to
                    avoid rate limiting issues.

            *** TODO: accept access tokens for any given number of datasources.
            For this implementation we only care to gather the Github token
            since Bitbucket is much less restrictive when it comes to
            unauthenticated api access.***

            2. (OPTIONAL) sources: comma-seprated [str] - The sources we want
                    to pull profile information from.
                    VALID_VALUES = see (app/datasources/__init__.py :class_map)
        """
        app.logger.info(f"Getting profile for: {org_name}")

        # ***VALIDATE THE DESIRED DATASOURCES***

        datasources = request.args.get('sources')
        app.logger.info(f"Requested datasources {datasources}")
        # Lets make sure datasources were passed in
        if datasources:
            # Since we expect a comma-separated list we need to split that
            datasources = datasources.split(',')
        else:
            # By default we want to get info from all available sources
            datasources = d_sources.all_sources()

        # Check that all desired datasources are valid. Since we want to give
        # the client specific feedback on which source is invalid we'll do a
        # traditional FOR loop (vs in line check for inclusion)
        # TODO: Improvement - we COULD accept a partial number of datasources.
        #   i.e. if the client passes an invalid source we can just filter that
        #   value out, process the request, and let the client know.
        for source_type in datasources:
            if source_type not in d_sources.class_map:
                return Response('Datasource type: {} is NOT currently '
                                'supported. Valid values are: '
                                '{}'.format(source_type, d_sources.class_map),
                                400)

        # ***ENSURE WE HAVE ALL REQUIRED ACCESS TOKENS***

        # If we want to get github info we will require an access token from
        # the client.
        # TODO: As more datasources are added we need to rethink this logic so
        #   it does not become unmanagable. Maybe add a 'required_token_key'
        #   property to datasources? ¯\_(ツ)_/¯
        if 'github' in datasources and not request.args.get('access_token'):
            return Response('Please provide a valid Github access token as '
                            'query paramater ex."?access_token={TOKEN_VALUE}"',
                            400)

        access_token = request.args.get('access_token')
        profiles = []

        # ***PROCESS REQUEST***
        try:
            for source_type in datasources:
                source = d_sources.class_map[source_type]
                user = source(org_name, access_token=access_token)
                profiles.append(user.get_profile_summary())
                app.logger.info(f"Got profile for {source_type}!")

            unified_profile = merge_profiles(profiles, d_sources.profile_keys)
            app.logger.info("Returning: {}".format(unified_profile))
            return Response(json.dumps(unified_profile),
                            status=200)
        except Exception as e:
            # TODO: Get more specifc here can capture things like
            # 1. Invalid credentials
            # 2. Rate limits
            # 3. Other more specifc exceptions based on the datasource
            return Response(str(e), 500)
