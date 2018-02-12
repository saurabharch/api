"""
    cloudplayer.api.controller.image
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2018 by Nicolas Drebenstedt
    :license: GPL-3.0, see LICENSE for details
"""
from cloudplayer.api.model.image import Image
import cloudplayer.api.controller


class ImageController(cloudplayer.api.controller.Controller):

    __model__ = Image
