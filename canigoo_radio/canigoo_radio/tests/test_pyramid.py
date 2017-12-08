# This file is a part of the Canigoo Radio project
#
#    Copyright (C) 2017 Franck Bret <franckbret@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import base64
import datetime

from anyblok_pyramid.tests.testcase import PyramidBlokTestCase

from . import create_user, create_presenter, create_show, create_event


def get_basic_auth_headers(user, password='secret'):
    credentials = "{}:{}".format(user, password)
    b64_credentials = base64.b64encode(
        credentials.encode('utf-8')).decode('utf-8')
    authorization = 'Basic {}'.format(b64_credentials)
    return {
        'Authorization': authorization
    }


class TestApiBasicAuthLogin(PyramidBlokTestCase):
    """User BasicAuth Credentials test class
    """

    def setUp(self):
        super(TestApiBasicAuthLogin, self).setUp()
        self.user = create_user(self)

    def test_post_credentials(self):
        response = self.webserver.post(
                '/api/v1/login',
                headers=get_basic_auth_headers(
                    self.user.username, password='pop'))
        self.assertEqual(response.status, '200 OK')
        self.assertIsNotNone(response.request.authorization)
        self.assertEqual(response.request.authorization[0], 'Basic')
        self.assertEqual("%s %s" % response.request.authorization,
                         response.request.headers.get('Authorization'))

    def test_post_credentials_invalid_password(self):
        response = self.webserver.post(
            '/api/v1/login',
            headers=get_basic_auth_headers(
                self.user.username, password='invalid'), status=401)
        self.assertEqual(response.status, '401 Unauthorized')
        self.assertIsNotNone(response.json_body.get('errors', None))
        self.assertEqual(len(response.json_body.get('errors')), 1)
        self.assertEqual(response.json_body.get(
            'errors')[0].get('location'), 'header')
        self.assertEqual(response.json_body.get(
            'errors')[0].get('name'), 'password')

    def test_post_credentials_invalid_username(self):
        response = self.webserver.post(
            '/api/v1/login',
            headers=get_basic_auth_headers(
                'invalid', password='bob'), status=401)
        self.assertEqual(response.status, '401 Unauthorized')
        self.assertIsNotNone(response.json_body.get('errors', None))
        self.assertEqual(len(response.json_body.get('errors')), 1)
        self.assertEqual(response.json_body.get(
            'errors')[0].get('location'), 'header')
        self.assertEqual(response.json_body.get(
            'errors')[0].get('name'), 'username')
        self.assertEqual(response.status_code, 401)

    def test_get_protected_view(self):
        response_protected = self.webserver.get(
                '/api/v1/users',
                headers=get_basic_auth_headers(
                    self.user.username, password='pop'))
        self.assertEqual(response_protected.status_code, 200)
        self.assertIsNone(
            response_protected.json_body[0].get('password', None))

    def test_get_protected_view_without_credentials(self):
        response_protected = self.webserver.get(
            '/api/v1/users', status=401)
        self.assertIsNone(response_protected.request.authorization)
        self.assertEqual(response_protected.status, '401 Unauthorized')
        self.assertIsNotNone(response_protected.json_body.get('errors', None))
        self.assertEqual(len(response_protected.json_body.get('errors')), 1)
        self.assertEqual(response_protected.json_body.get(
            'errors')[0].get('location'), 'header')
        self.assertEqual(response_protected.json_body.get(
            'errors')[0].get('name'), 'auth')
        self.assertEqual(response_protected.status_code, 401)


class TestApiPresenter(PyramidBlokTestCase):
    """Presenter api test class
    """

    def setUp(self):
        super(TestApiPresenter, self).setUp()
        self.user = create_user(self)
        self.presenter = create_presenter(self)

    def test_get_presenter_view(self):
        res = self.webserver.get(
                '/api/v1/presenters/%s' % self.presenter.uuid,
                headers=get_basic_auth_headers(
                    self.user.username, password='pop'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json_body.get('uuid'), str(self.presenter.uuid))
        self.assertEqual(res.json_body.get('name'), self.presenter.name)

    def test_get_presenter_view_dschema(self):
        res = self.webserver.get(
                '/api/v1/presenters/%s' % self.presenter.uuid,
                headers=get_basic_auth_headers(
                    self.user.username, password='pop'))
        self.assertCountEqual(
            list(res.json_body.keys()), ['uuid', 'shows', 'name'])

    def test_get_presenters_view(self):
        res = self.webserver.get(
                '/api/v1/presenters',
                headers=get_basic_auth_headers(
                    self.user.username, password='pop'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json_body), 1)

    def test_post_presenter_view(self):
        response = self.webserver.post_json(
                '/api/v1/presenters',
                params={'name': 'Dj FooFoo'},
                headers=get_basic_auth_headers('bob', password='pop'),
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json_body.get('name'), "Dj FooFoo")

    def test_post_bad_key_presenter_view(self):
        response = self.webserver.post_json(
                '/api/v1/presenters',
                params={'badkey': 'Dj FooFoo'},
                headers=get_basic_auth_headers('bob', password='pop'),
                status=400,
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.json_body.get('errors')), 1)
        self.assertEqual(response.json_body.get(
            'errors')[0].get('location'), 'body')
        self.assertEqual(response.json_body.get(
            'errors')[0].get('description'), 'badkey.\n')

    def test_delete_presenter_view(self):
        response = self.webserver.delete(
                    '/api/v1/presenters/%s' % self.presenter.uuid,
                    headers=get_basic_auth_headers('bob', password='pop'),
                    )
        self.assertEqual(response.status_code, 200)
        response = self.webserver.get(
                    '/api/v1/presenters',
                    headers=get_basic_auth_headers('bob', password='pop'),
                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json_body, None)


class TestApiShow(PyramidBlokTestCase):
    """Show api test class
    """

    def setUp(self):
        super(TestApiShow, self).setUp()
        self.user = create_user(self)
        self.presenter = create_presenter(self)
        self.show = create_show(self, presenter=self.presenter)

    def test_get_show_view(self):
        res = self.webserver.get(
                '/api/v1/shows/%s' % self.show.uuid,
                headers=get_basic_auth_headers(
                    self.user.username, password='pop'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json_body.get('uuid'), str(self.show.uuid))
        self.assertEqual(res.json_body.get('name'), self.show.name)

    def test_get_show_view_dschema(self):
        res = self.webserver.get(
                '/api/v1/shows/%s' % self.show.uuid,
                headers=get_basic_auth_headers(
                    self.user.username, password='pop'))
        self.assertCountEqual(list(
            res.json_body.keys()),
            ['uuid', 'presenter', 'events', 'name'])

    def test_get_shows_view(self):
        res = self.webserver.get(
                '/api/v1/shows',
                headers=get_basic_auth_headers(
                    self.user.username, password='pop'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json_body), 1)

    def test_post_show_view(self):
        response = self.webserver.post_json(
                '/api/v1/shows',
                params={'name': 'GooGoo Radio Show',
                        'presenter': '%s' % self.presenter.uuid},
                headers=get_basic_auth_headers('bob', password='pop'),
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json_body.get('name'), "GooGoo Radio Show")

    def test_post_bad_key_show_view(self):
        response = self.webserver.post_json(
                '/api/v1/shows',
                params={'badkey': 'Goo'},
                headers=get_basic_auth_headers('bob', password='pop'),
                status=400,
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.json_body.get('errors')), 1)
        self.assertEqual(response.json_body.get(
            'errors')[0].get('location'), 'body')
        self.assertEqual(response.json_body.get(
            'errors')[0].get('description'), 'badkey.\n')

    def test_delete_show_view(self):
        response = self.webserver.delete(
                    '/api/v1/shows/%s' % self.show.uuid,
                    headers=get_basic_auth_headers('bob', password='pop'),
                    )
        self.assertEqual(response.status_code, 200)
        response = self.webserver.get(
                    '/api/v1/shows',
                    headers=get_basic_auth_headers('bob', password='pop'),
                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json_body, None)


class TestApiEvent(PyramidBlokTestCase):
    """Event api test class
    """

    def setUp(self):
        super(TestApiEvent, self).setUp()
        self.user = create_user(self)
        self.presenter = create_presenter(self)
        self.show = create_show(self, presenter=self.presenter)
        self.event = create_event(self, show=self.show)

    def test_get_event_view(self):
        res = self.webserver.get(
                '/api/v1/events/%s' % self.event.uuid,
                headers=get_basic_auth_headers(
                    self.user.username, password='pop'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json_body.get('uuid'), str(self.event.uuid))
        self.assertEqual(res.json_body.get('name'), self.event.name)

    def test_get_event_view_dschema(self):
        res = self.webserver.get(
                '/api/v1/events/%s' % self.event.uuid,
                headers=get_basic_auth_headers(
                    self.user.username, password='pop'))
        self.assertCountEqual(
            list(res.json_body.keys()),
            ['uuid', 'show', 'name', 'created_at', 'edited_at',
             'start', 'end'])

    def test_get_events_view(self):
        res = self.webserver.get(
                '/api/v1/events',
                headers=get_basic_auth_headers(
                    self.user.username, password='pop'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json_body), 1)

    def test_post_event_view(self):
        start = self.event.start + datetime.timedelta(hours=1)
        end = start + datetime.timedelta(hours=1)

        response = self.webserver.post_json(
                '/api/v1/events',
                params={'name': 'GooGoo Radio Show #2',
                        'start': '%s' % start.isoformat(),
                        'end': '%s' % end.isoformat(),
                        'show': '%s' % self.show.uuid},
                headers=get_basic_auth_headers('bob', password='pop'),
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json_body.get('name'),
            "GooGoo Radio Show #2")

    def test_post_bad_key_event_view(self):
        response = self.webserver.post_json(
                '/api/v1/events',
                params={'badkey': 'Goo'},
                headers=get_basic_auth_headers('bob', password='pop'),
                status=400,
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.json_body.get('errors')), 1)
        self.assertEqual(response.json_body.get(
            'errors')[0].get('location'), 'body')
        self.assertEqual(response.json_body.get(
            'errors')[0].get('description'), 'badkey.\n')

    def test_delete_event_view(self):
        response = self.webserver.delete(
                    '/api/v1/events/%s' % self.event.uuid,
                    headers=get_basic_auth_headers('bob', password='pop'),
                    )
        self.assertEqual(response.status_code, 200)
        response = self.webserver.get(
                    '/api/v1/events',
                    headers=get_basic_auth_headers('bob', password='pop'),
                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json_body, None)
