# This file is a part of the AnyBlok / Pyramid / REST api project
#
#    Copyright (C) 2017 Franck Bret <franckbret@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from pyramid.view import view_defaults, forbidden_view_config
from pyramid.authentication import extract_http_basic_credentials
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.security import forget

from cornice import Service

from anyblok_pyramid import current_blok


@view_defaults(installed_blok=current_blok())
@forbidden_view_config()
def forbidden_view(request):
    if request.authenticated_userid is None:
        request.errors.add(
                'header',
                'auth',
                'You must be authenticated to access this resource.')
        response = HTTPUnauthorized()
        response.headers.update(forget(request))
        response.json_body = dict(errors=request.errors)
    # user is logged in but doesn't have permissions, reject wholesale
    else:
        request.errors.add(
                'header',
                'permission',
                'You do not have permission to access this resource.')
        response = HTTPForbidden()
        response.headers.update(forget(request))
        response.json_body = dict(errors=request.errors)
    return response

# TODO, better cors_policy + settings through configuration file
cors_policy = dict(
        enabled=False,
        headers=(
            'Access-Control-Allow-Origin',
            'Authorization',
            'Origin',
            'X-Requested-With',
            'Content-Type',
            'Accept'),
        origins=('*'),
        credentials=True,
        max_age=3600)

user_login = Service(
        name='user_login',
        path='/api/v1/login',
        description="User authentication",
        cors_policy=cors_policy)


@view_defaults(installed_blok=current_blok())
@user_login.post()
def user_login_post(request):
    if not request.unauthenticated_userid:
        request.errors.add(
                'header',
                'check unauthenticated user_id',
                'something is wrong, can not get unauthenticated_user_id'
                'at login')
        request.errors.status = 401
        return

    try:
        # here password is extracted as a readable one from request
        username, password = extract_http_basic_credentials(request)
    except TypeError:
        request.errors.add(
                'header',
                'extract_http_basic_credentials',
                'can not parse the given credentials')
        request.errors.status = 401
        return

    registry = request.anyblok.registry
    user = registry.User.query().filter_by(username=username).first()

    if not user:
        request.errors.add('header', 'username', 'wrong username')
        request.errors.status = 401
        return

    if user and user.password == password:
        return dict(id=str(user.id), username=username)
    else:
        request.errors.add('header', 'password', 'wrong password')
        request.errors.status = 401
        return


user_logout = Service(
        name='user_logout',
        path='/api/v1/logout',
        description="User logout")


@view_defaults(installed_blok=current_blok())
@user_logout.post()
def user_logout_post(request):
    if request.session:
        request.session.clear()
        request.session.save()
    return dict(message="bye")
