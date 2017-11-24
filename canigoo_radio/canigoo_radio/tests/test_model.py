# This file is a part of the Canigoo Radio project
#
#    Copyright (C) 2017 Franck Bret <franckbret@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.

from anyblok.tests.testcase import BlokTestCase
import datetime
from . import create_user, create_presenter, create_show, create_event


class TestCanigooBlok(BlokTestCase):
    """ Test User, Presenter, Show, Event models python api"""

    def setUp(self):
        self.user = create_user(self)
        self.presenter = create_presenter(self)
        self.show = create_show(self, presenter=self.presenter)
        self.event = create_event(self, show=self.show)

    def test_create_user(self):
        self.assertEqual(self.registry.User.query().count(), 1)
        self.assertEqual(self.user.username, "bob")
        self.assertEqual(self.user.password, "pop")

    def test_create_presenter(self):
        self.assertEqual(self.registry.Presenter.query().count(), 1)
        self.assertEqual(self.presenter.name, "Dj Foo")

    def test_create_show(self):
        self.assertEqual(self.registry.Show.query().count(), 1)
        self.assertEqual(self.show.name, "FooBar radio show")

    def test_create_event(self):
        self.assertEqual(
            self.registry.Event.query().count(), 1)
        self.assertEqual(
            self.event.name, "FooEvent #1")

    def test_event_get_duration(self):
        self.assertEqual(
            self.event.get_duration(), datetime.timedelta(0, 3600))

    def test_event_get_current(self):
        self.assertEqual(
            self.registry.Event.get_current(), self.event)
        self.assertEqual(
            self.registry.Event.get_current(at=datetime.datetime.now()),
            self.event
        )

    def test_event_get_next(self):
        event2 = create_event(self,
                              start=self.event.end,
                              end=self.event.end + datetime.timedelta(hours=1),
                              name="FooEvent #2",
                              show=self.show)
        self.assertEqual(
            self.registry.Event.get_next(),
            event2
        )

    def test_event_get_previous(self):
        event2 = create_event(
                    self,
                    start=self.event.start - datetime.timedelta(hours=1),
                    end=self.event.start,
                    name="FooEvent #0",
                    show=self.show)
        self.assertEqual(
            self.registry.Event.get_previous(),
            event2
        )

    def test_event_overlap(self):
        create_event(
            self,
            start=self.event.start + datetime.timedelta(minutes=10),
            end=self.event.end - datetime.timedelta(minutes=10),
            name="FooEvent #2",
            show=self.show)

        self.assertEqual(self.registry.Event.query().count(), 2)

        self.assertEqual(
            len(self.registry.Event.overlap(
                start=datetime.datetime.now() + datetime.timedelta(minutes=10),
                end=datetime.datetime.now() + datetime.timedelta(minutes=40)
                )), 2)

        self.assertEqual(
            len(self.registry.Event.overlap(
                start=datetime.datetime.now() + datetime.timedelta(minutes=1),
                end=datetime.datetime.now() + datetime.timedelta(minutes=2)
                )), 1)

        self.assertEqual(
            self.registry.Event.overlap(
                start=datetime.datetime.now() + datetime.timedelta(
                    minutes=100),
                end=datetime.datetime.now() + datetime.timedelta(minutes=200)
                ), None)
