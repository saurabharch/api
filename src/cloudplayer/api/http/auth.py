"""
    cloudplayer.api.http.auth
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2018 by Nicolas Drebenstedt
    :license: GPL-3.0, see LICENSE for details
"""
import traceback
import urllib

import tornado.auth
import tornado.escape
import tornado.httputil
import tornado.options as opt
import tornado.web

from cloudplayer.api.controller.auth import SoundcloudAuthController
from cloudplayer.api.controller.auth import YoutubeAuthController
from cloudplayer.api.handler import ControllerHandlerMixin
from cloudplayer.api.http import HTTPHandler


class AuthHandler(
        ControllerHandlerMixin, HTTPHandler, tornado.auth.OAuth2Mixin):

    _OAUTH_NO_CALLBACKS = False
    _OAUTH_VERSION = '1.0a'
    _OAUTH_RESPONSE_TYPE = 'code'
    _OAUTH_GRANT_TYPE = 'authorization_code'

    _OAUTH_SCOPE_LIST = []
    _OAUTH_EXTRA_PARAMS = {}

    _OAUTH_AUTHORIZE_URL = NotImplemented
    _OAUTH_USERINFO_URL = NotImplemented

    @property
    def _OAUTH_CLIENT_ID(self):
        return opt.options[self.__provider__]['key']

    @property
    def _OAUTH_CLIENT_SECRET(self):
        return opt.options[self.__provider__]['secret']

    @property
    def _OAUTH_REDIRECT_URI(self):
        return opt.options[self.__provider__]['redirect_uri']

    async def get(self):
        if self.get_argument('code', None) is not None:
            try:
                await self.provider_callback()
            except:  # NOQA
                traceback.print_exc()
            finally:
                self.redirect('/static/close.html')
        else:
            await self.authorize_redirect(
                redirect_uri=self._OAUTH_REDIRECT_URI,
                client_id=self._OAUTH_CLIENT_ID,
                scope=self._OAUTH_SCOPE_LIST,
                response_type=self._OAUTH_RESPONSE_TYPE,
                extra_params=self._OAUTH_EXTRA_PARAMS)

    async def fetch_async(self, url, **kw):
        return await self.controller.fetch_async(url, **kw)

    async def fetch_access(self):
        """Fetches the authenticated user data upon redirect"""
        body = urllib.parse.urlencode({
            'client_id': self._OAUTH_CLIENT_ID,
            'client_secret': self._OAUTH_CLIENT_SECRET,
            'code': self.get_argument('code'),
            'grant_type': self._OAUTH_GRANT_TYPE,
            'redirect_uri': self._OAUTH_REDIRECT_URI})

        response = await self.fetch_async(
            self.controller.OAUTH_ACCESS_TOKEN_URL,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            method='POST',
            body=body)
        return tornado.escape.json_decode(response.body)

    async def fetch_account(self, access_info):
        uri = tornado.httputil.url_concat(
            self._OAUTH_USERINFO_URL,
            {'access_token': True,
             self.controller.OAUTH_TOKEN_PARAM: access_info['access_token']})
        response = await self.fetch_async(uri)
        return tornado.escape.json_decode(response.body)

    async def provider_callback(self):
        # exchange oauth code for access_token
        access_info = await self.fetch_access()
        # retrieve account info using access_token
        account_info = await self.fetch_account(access_info)
        # update or create a new account for this provider
        self.controller.update_account(access_info, account_info)

        # sync user account info back to cookie
        self.current_user['user_id'] = self.controller.account.user_id
        for p in opt.options['providers']:
            self.current_user[p] = None
        for a in self.controller.account.user.accounts:
            self.current_user[a.provider_id] = a.id
        self.set_user_cookie()


class Soundcloud(AuthHandler):

    __controller__ = SoundcloudAuthController

    __provider__ = 'soundcloud'
    _OAUTH_AUTHORIZE_URL = 'https://soundcloud.com/connect'
    _OAUTH_USERINFO_URL = 'https://api.soundcloud.com/me'
    _OAUTH_SCOPE_LIST = []

    @property
    def _OAUTH_EXTRA_PARAMS(self):
        return {'state': self.settings['redirect_state']}


class Youtube(AuthHandler):

    __controller__ = YoutubeAuthController

    __provider__ = 'youtube'
    _OAUTH_AUTHORIZE_URL = 'https://accounts.google.com/o/oauth2/auth'
    _OAUTH_USERINFO_URL = ('https://www.googleapis.com/youtube/v3/channels'
                           '?part=snippet&mine=true')
    _OAUTH_SCOPE_LIST = [
        'profile', 'email', 'https://www.googleapis.com/auth/youtube']
    _OAUTH_EXTRA_PARAMS = {
        'approval_prompt': 'auto', 'access_type': 'offline'}
