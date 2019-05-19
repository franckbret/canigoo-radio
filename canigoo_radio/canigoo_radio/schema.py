# This file is a part of the Canigoo Radio project
#
#    Copyright (C) 2017 Franck Bret <franckbret@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
"""Canigoo radio schema for models and rest api
"""

from anyblok_marshmallow import SchemaWrapper
from marshmallow.schema import Schema
from anyblok_marshmallow.fields import Nested, String


class UserSchema(SchemaWrapper):
    """Schema for 'Model.User'
    """
    model = 'Model.User'


class PresenterSchema(SchemaWrapper):
    """Schema for 'Model.Presenter'
    """
    model = 'Model.Presenter'


class ShowSchema(SchemaWrapper):
    """Schema for 'Model.Show'
    """
    model = 'Model.Show'


class EventSchema(SchemaWrapper):
    """Schema for 'Model.Event'
    """
    model = 'Model.Event'
