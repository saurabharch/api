"""
    cloudplayer.api.controller.favourite
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2018 by Nicolas Drebenstedt
    :license: GPL-3.0, see LICENSE for details
"""
import tornado.gen

from cloudplayer.api.model.account import Account
from cloudplayer.api.model.favourite import Favourite
import cloudplayer.api.controller


class FavouriteController(cloudplayer.api.controller.Controller):

    __model__ = Favourite

    def read(self, ids):
        if ids['id'] == 'mine':
            provider_id = ids['provider_id']
            account_id = self.current_user[provider_id]
            account = self.db.query(Account).get((account_id, provider_id))
            ids['id'] = account.favourite.id
        return super().read(ids)
