"""
    cloudplayer.api.http.playlist
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by the cloudplayer team
    :license: GPL-3.0, see LICENSE for details
"""
from cloudplayer.api.controller.playlist import PlaylistController
from cloudplayer.api.http import HTTPHandler
from cloudplayer.api.handler import EntityMixin, CollectionMixin


class Entity(EntityMixin, HTTPHandler):

    __controller__ = PlaylistController

    SUPPORTED_METHODS = ('GET', 'PATCH', 'DELETE', 'OPTIONS')


class Collection(CollectionMixin, HTTPHandler):

    __controller__ = PlaylistController

    SUPPORTED_METHODS = ('GET', 'POST', 'OPTIONS')
