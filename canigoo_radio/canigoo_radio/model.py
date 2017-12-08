# This file is a part of the Canigoo Radio project
#
#    Copyright (C) 2017 Franck Bret <franckbret@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
"""Canigoo radio models
"""
from datetime import datetime
from uuid import uuid1

from sqlalchemy import and_, or_

from anyblok import Declarations
from anyblok.column import (Integer, String, DateTime, Password, UUID)
from anyblok.relationship import Many2One

from .exception import EventOverlapException


Mixin = Declarations.Mixin
Model = Declarations.Model


@Declarations.register(Mixin)
class IdColumn:
    """ `ìd` primary key mixin
    """
    id = Integer(primary_key=True)


@Declarations.register(Mixin)
class UuidColumn:
    """ `UUID` id primary key mixin
    """
    uuid = UUID(primary_key=True, default=uuid1, binary=False)


@Declarations.register(Mixin)
class TrackModel:
    """ A mixin to store record creation and edition date
    """
    created_at = DateTime(default=datetime.now, nullable=False)
    edited_at = DateTime(
        default=datetime.now, auto_update=True, nullable=False)


@Declarations.register(Model)
class User(UuidColumn):
    """ User model with password
    """
    email = String(label="Email", unique=True, nullable=False)
    username = String(label="Username", nullable=False)
    password = Password(crypt_context={'schemes': ['pbkdf2_sha512']},
                        nullable=False)

    def __str__(self):
        return ('{self.username}').format(self=self)

    def __repr__(self):
        msg = ('<User: {self.username}>')

        return msg.format(self=self)


@Declarations.register(Model)
class Presenter(UuidColumn):
    """Presenter Model
    A presenter has in charge shows and events
    """
    name = String(nullable=False)

    def __str__(self):
        return ('{self.name}').format(self=self)

    def __repr__(self):
        msg = ('<Presenter: {self.name}>')

        return msg.format(self=self)


@Declarations.register(Model)
class Show(UuidColumn):
    """Show model
    Properties sample:
    dict(auto=dict(), playlist=dict())
    """
    name = String(nullable=False)
    presenter = Many2One(
        label="Presenter", model=Model.Presenter, one2many="shows")

    def __str__(self):
        return ('{self.name}').format(self=self)

    def __repr__(self):
        msg = ('<Show: {self.name}>')

        return msg.format(self=self)


@Declarations.register(Model)
class Event(UuidColumn, TrackModel):
    """Calendar Event model

    Properties sample:
        dict(auto=dict(query=""),
        playlist=dict(tracklisting=list("trk1", "trk2")),
        live=dict()
    """
    name = String(nullable=False)
    start = DateTime(label="Start")
    end = DateTime(label="End")
    show = Many2One(
        label="Show", model=Model.Show, one2many="events")

    def get_duration(self):
        """ Returns a timedelta duration object
        """
        if self.end and self.start:
            return self.end - self.start
        else:
            return None

    @classmethod
    def get_current(cls, at=None):
        E = cls.registry.Event
        if not at:
            at = datetime.now()
        return E.query().filter(
            E.start < at, E.end > at).order_by(E.start.desc()).first() or None

    @classmethod
    def get_next(cls, at=None):
        E = cls.registry.Event
        if not at:
            at = datetime.now()
        return E.query().filter(
            E.start > at).order_by(E.start.asc()).first() or None

    @classmethod
    def get_previous(cls, at=None):
        E = cls.registry.Event
        if not at:
            at = datetime.now()
        return E.query().filter(
            E.end < at).order_by(E.start.desc()).first() or None

    @classmethod
    def overlap(cls, start=None, end=None):
        E = cls.registry.Event
        Q = E.query().filter(
                or_(
                    and_(E.start < start, E.end > end),
                    and_(E.start < end, E.end > start)
                    )
                ).order_by(
                    E.start.desc())
        return Q.count() and Q.all() or None

    @classmethod
    def insert(cls, *args, **kwargs):
        """Overload insert method in order to raise on event creation if any
        overlap with other events is detected
        """
        overlap = cls.overlap(start=kwargs['start'], end=kwargs['end'])
        if overlap:
            raise EventOverlapException(
                """The event you want to create starting at %r and ending at %r
                overlap with %r""" % (kwargs['start'], kwargs['end'], overlap))
        return super(Event, cls).insert(*args, **kwargs)

    def __str__(self):
        return ('{self.name}').format(self=self)

    def __repr__(self):
        msg = ('<Event: {self.name} ({start} / {end})>')
        return msg.format(
            self=self,
            start=self.start.strftime('%Y-%m-%d %H:%M:%S'),
            end=self.end.strftime('%Y-%m-%d %H:%M:%S'))
