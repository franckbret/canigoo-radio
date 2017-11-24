# This file is a part of the AnyBlok / Pyramid / REST api project
#
#    Copyright (C) 2017 Franck Bret <franckbret@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.

from pyramid.security import ALL_PERMISSIONS
from pyramid.security import Allow
from pyramid.security import Authenticated


def check_basic_auth_credentials(username, password, request):

    registry = request.anyblok.registry
    user = registry.User.query().filter_by(username=username).first()

    if user and user.password == password:
        # an empty list is enough to indicate logged-in
        return []


class RootAcl:

    __acl__ = (
        (Allow, Authenticated, ALL_PERMISSIONS),
    )
