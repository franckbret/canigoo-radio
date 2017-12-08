# This file is a part of the Canigoo radio project
#
#    Copyright (C) 2017 Franck Bret <franckbret@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
"""Canigoo Radio Blok
"""
from uuid import UUID
from datetime import datetime

from anyblok.blok import Blok
from anyblok_pyramid.adapter import uuid_adapter, datetime_adapter

from pyramid.renderers import JSON
from pyramid.authentication import BasicAuthAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .views.validators import check_basic_auth_credentials, RootAcl


class Canigoo_radio(Blok):
    """Canigoo radio's Blok class definition
    """
    version = "0.1.0"
    author = "Franck Bret"
    required = ['anyblok-core']

    @classmethod
    def import_declaration_module(cls):
        """Python module to import in the given order at start-up
        """
        from . import model  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        """Python module to import while reloading server (ie when
        adding Blok at runtime
        """
        from . import model  # noqa
        reload(model)

    @classmethod
    def pyramid_load_config(cls, config):

        # Set an authorization policy
        authz_policy = ACLAuthorizationPolicy()
        config.set_authorization_policy(authz_policy)

        # Set an authentication policy (basic auth based)
        authn_policy = BasicAuthAuthenticationPolicy(
            check_basic_auth_credentials)
        config.set_authentication_policy(authn_policy)

        # Set Acl (this will assemble authorization and authentication
        # policies)
        config.set_root_factory(lambda request: RootAcl())

        # include configuration for dependencies modules
        config.include("cornice")
        config.include("cornice_swagger")
        config.include("pyramid_jinja2")

        # Json api renderer
        json_renderer = JSON()
        json_renderer.add_adapter(UUID, uuid_adapter)
        json_renderer.add_adapter(datetime, datetime_adapter)
        config.add_renderer('json', json_renderer)

        # Add json api base route
        config.add_route('canigoo_api_v1', '/api/v1/')

        # Scan available views
        config.scan(cls.__module__ + '.views')
