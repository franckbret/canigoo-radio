# This file is a part of the Canigoo Radio project
#
#    Copyright (C) 2017 Franck Bret <franckbret@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.

from marshmallow import Schema, validates_schema, ValidationError

from anyblok_marshmallow.schema import ModelSchema
from anyblok_marshmallow.fields import Nested
from anyblok_pyramid_rest_api.schema import (
    FullRequestSchema,
)


class UserSchema(ModelSchema):
    """Schema for 'Model.User'
    """
    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise ValidationError('Unknown field', unknown)

    class Meta:
        model = 'Model.User'


class UserRequestSchema(FullRequestSchema):
    """Request validation for UserSchema
    """
    body = Nested(UserSchema(partial=True))
    path = Nested(UserSchema(only_primary_key=True))
    querystring = Nested(UserSchema(partial=True))


class UserApiSchema(Schema):
    # fields for incoming request validation
    collection_post = Nested(UserRequestSchema(only=('body',)))
    collection_get = Nested(UserRequestSchema(only=('querystring',)))
    get = Nested(UserRequestSchema(only=('path',)))
    put = Nested(UserRequestSchema(only=('body', 'path',)))
    patch = Nested(UserRequestSchema(only=('body', 'path',)))
    delete = Nested(UserRequestSchema(only=('path',)))
    # fields for response deserialization
    dschema = Nested(UserSchema(exclude=('password',)))
    dschema_collection = Nested(UserSchema(many=True, exclude=('password',)))


class PresenterSchema(ModelSchema):
    """Schema for 'Model.Presenter'
    """
    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise ValidationError('Unknown field', unknown)

    class Meta:
        model = 'Model.Presenter'


class PresenterRequestSchema(FullRequestSchema):
    """Request validation for PresenterSchema
    """
    body = Nested(PresenterSchema(partial=True))
    path = Nested(PresenterSchema(only_primary_key=True))
    querystring = Nested(PresenterSchema(partial=True))


class PresenterApiSchema(Schema):
    # fields for incoming request validation
    collection_post = Nested(PresenterRequestSchema(only=('body',)))
    collection_get = Nested(PresenterRequestSchema(only=('querystring',)))
    get = Nested(PresenterRequestSchema(only=('path',)))
    put = Nested(PresenterRequestSchema(only=('body', 'path',)))
    patch = Nested(PresenterRequestSchema(only=('body', 'path',)))
    delete = Nested(PresenterRequestSchema(only=('path',)))
    # fields for response deserialization
    dschema = Nested(PresenterSchema())
    dschema_collection = Nested(PresenterSchema(many=True))


class ShowSchema(ModelSchema):
    """Schema for 'Model.Show'
    """
    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise ValidationError('Unknown field', unknown)

    class Meta:
        model = 'Model.Show'


class ShowRequestSchema(FullRequestSchema):
    """Request validation for ShowSchema
    """
    body = Nested(ShowSchema(partial=True))
    path = Nested(ShowSchema(only_primary_key=True))
    querystring = Nested(ShowSchema(partial=True))


class ShowApiSchema(Schema):
    # fields for incoming request validation
    collection_post = Nested(ShowRequestSchema(only=('body',)))
    collection_get = Nested(ShowRequestSchema(only=('querystring',)))
    get = Nested(ShowRequestSchema(only=('path',)))
    put = Nested(ShowRequestSchema(only=('body', 'path',)))
    patch = Nested(ShowRequestSchema(only=('body', 'path',)))
    delete = Nested(ShowRequestSchema(only=('path',)))
    # fields for response deserialization
    dschema = Nested(ShowSchema())
    dschema_collection = Nested(ShowSchema(many=True))


class EventSchema(ModelSchema):
    """Schema for 'Model.Event'
    """
    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise ValidationError('Unknown field', unknown)

    class Meta:
        model = 'Model.Event'


class EventRequestSchema(FullRequestSchema):
    """Request validation for EventSchema
    """
    body = Nested(EventSchema(partial=True))
    path = Nested(EventSchema(only_primary_key=True))
    querystring = Nested(EventSchema(partial=True))


class EventApiSchema(Schema):
    # fields for incoming request validation
    collection_post = Nested(EventRequestSchema(only=('body',)))
    collection_get = Nested(EventRequestSchema(only=('querystring',)))
    get = Nested(EventRequestSchema(only=('path',)))
    put = Nested(EventRequestSchema(only=('body', 'path',)))
    patch = Nested(EventRequestSchema(only=('body', 'path',)))
    delete = Nested(EventRequestSchema(only=('path',)))
    # fields for response deserialization
    dschema = Nested(EventSchema())
    dschema_collection = Nested(EventSchema(many=True))
