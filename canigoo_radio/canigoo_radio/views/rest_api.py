# This file is a part of the AnyBlok / Pyramid / REST api project
#
#    Copyright (C) 2017 Franck Bret <franckbret@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.

from pyramid.view import view_defaults
from cornice.resource import resource

from anyblok_pyramid import current_blok

from anyblok_pyramid_rest_api.crud_resource import (
    CrudResource
)
from anyblok_pyramid_rest_api.validator import (
    model_schema_validator
)

from . validators import RootAcl
from .. schema import (
    UserApiSchema,
    PresenterApiSchema,
    ShowApiSchema,
    EventApiSchema
)


@resource(collection_path='/api/v1/users',
          path='/api/v1/users/{id}',
          schema=UserApiSchema(),
          permission='authenticated',
          validators=(model_schema_validator,),
          installed_blok=current_blok())
class UserResource(CrudResource, RootAcl):
    model = 'Model.User'


@resource(collection_path='/api/v1/presenters',
          path='/api/v1/presenters/{id}',
          schema=PresenterApiSchema(),
          permission='authenticated',
          validators=(model_schema_validator,),
          installed_blok=current_blok())
class PresenterResource(CrudResource, RootAcl):
    model = 'Model.Presenter'


@resource(collection_path='/api/v1/shows',
          path='/api/v1/shows/{id}',
          schema=ShowApiSchema(),
          permission='authenticated',
          validators=(model_schema_validator,),
          installed_blok=current_blok())
class ShowResource(CrudResource, RootAcl):
    model = 'Model.Show'


@resource(collection_path='/api/v1/events',
          path='/api/v1/events/{id}',
          schema=EventApiSchema(),
          permission='authenticated',
          validators=(model_schema_validator,),
          installed_blok=current_blok())
class EventResource(CrudResource, RootAcl):
    model = 'Model.Event'
