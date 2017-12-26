# This file is a part of the Canigoo radio project
#
#    Copyright (C) 2017 Franck Bret <franckbret@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
""" A set of http endpoints for rest api backend
"""
import os
import beets.library

from cornice.resource import resource
from cornice import Service

from anyblok.config import Configuration

from anyblok_pyramid import current_blok

from anyblok_pyramid_rest_api.crud_resource import (
    CrudResource
)
from anyblok_pyramid_rest_api.validator import (
    base_validator,
    model_schema_validator
)

from . validators import RootAcl
from .. liquidsoap_client import LiquidsoapClient
from .. schema import (
    UserApiSchema,
    PresenterApiSchema,
    ShowApiSchema,
    EventApiSchema
)


_BEETS_DB = os.path.expanduser(Configuration.get('beets_db', "~/canigoo.db"))


@resource(collection_path='/api/v1/users',
          path='/api/v1/users/{uuid}',
          schema=UserApiSchema(),
          permission='authenticated',
          validators=(model_schema_validator,),
          installed_blok=current_blok())
class UserResource(CrudResource, RootAcl):
    model = 'Model.User'


@resource(collection_path='/api/v1/presenters',
          path='/api/v1/presenters/{uuid}',
          schema=PresenterApiSchema(),
          permission='authenticated',
          validators=(model_schema_validator,),
          installed_blok=current_blok())
class PresenterResource(CrudResource, RootAcl):
    model = 'Model.Presenter'


@resource(collection_path='/api/v1/shows',
          path='/api/v1/shows/{uuid}',
          schema=ShowApiSchema(),
          permission='authenticated',
          validators=(model_schema_validator,),
          installed_blok=current_blok())
class ShowResource(CrudResource, RootAcl):
    model = 'Model.Show'


@resource(collection_path='/api/v1/events',
          path='/api/v1/events/{uuid}',
          schema=EventApiSchema(),
          permission='authenticated',
          validators=(model_schema_validator,),
          installed_blok=current_blok())
class EventResource(CrudResource, RootAcl):
    model = 'Model.Event'


liquidsoap_client = Service(name='liquidsoap_client',
                            path='/api/v1/liquidsoap',
                            permission='authenticated',
                            validators=(base_validator,),
                            installed_blok=current_blok(),
                            description='Liquidsoap client api endpoint')


@liquidsoap_client.get()
def liquidsoap_client_get(request):
    """ Retrieve for now status for icecast and Liquidsoap
    """
    sock = LiquidsoapClient()
    icecast_status = sock.send("icecast.status")
    version = sock.send("version")
    uptime = sock.send("uptime")
    operators = sock.send("list")
    res = dict(version=version,
               icecast_status=icecast_status,
               uptime=uptime,
               operators=operators)
    return res


@liquidsoap_client.post()
def liquidsoap_client_post(request):
    """ Send Liquidsoap commands
    """
    sock = LiquidsoapClient()
    cmd = request.validated.get('body').get('cmd', "")
    res = sock.send(cmd)
    return res or ""


tracks = Service(name='tracks',
                 path='/api/v1/tracks',
                 validators=(base_validator,),
                 installed_blok=current_blok(),
                 description='Tracklisting')


@tracks.get()
def tracks_collection_get(request):
    """Return tracklisting if any and current event
    """
    registry = request.anyblok.registry
    model = registry.get('Model.Event')
    res = model.get_current()
    return dict(name=res.name,
                show=res.show.name,
                presenter=res.show.presenter.name) if res else dict()


library_item = Service(name='library_item',
                       path='/api/v1/library/items',
                       permission='authenticated',
                       validators=(base_validator,),
                       installed_blok=current_blok(),
                       description='Library Item')


@library_item.get()
def library_item_collection_get(request):
    """ Returns a collection of library items from Beets
    """
    search = request.validated['querystring'].get('search', '')
    lib = beets.library.Library(_BEETS_DB)
    q = lib.items(search)
    res = [dict(item) for item in q.rows]
    return res


on_air = Service(name='on_air',
                 path='/api/v1/on-air',
                 description="Liquidsoap metadata of the current track")


@on_air.get()
def on_air_get(request):
    sock = LiquidsoapClient()
    current = sock.send("request.on_air")
    if type(current) == str():
        meta = sock.send('request.metadata %s' % current)
        return dict(meta=sock.parse_metadatas(meta)) if meta else dict()
    elif type(current) == dict() and "error" in current.keys():
        request.errors.add('body', "liquidsoap socket connection failed")
    else:
        return dict()
