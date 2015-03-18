#!/usr/bin/env python
# coding: utf-8
__author__ = 'Samuel Chen <samuel.net@gmail.com>'

'''
static_handler module description

Created on 3/13/2015
'''

from tornado.web import StaticFileHandler

class TornadoStaticHandler(StaticFileHandler):
    '''
    Override default tornado.web.StaticFileHandler.
    Used to work around a bug of SAE tornado worker.

    In application settings (index.wsgi),
    1. set "static_handler_class": "StaticHandler"
    2. set "static_path": os.path.join(os.path.dirname(__file__), "static"
    3. set SAE config.yaml to bypass default static handler.
        (__SS__ or whatever. Must NOT as same as your static setting in application setting above.)
        - url: /__SS__
          static_dir: __SS__
    '''

    def get(self, path, include_body=True):
        if path.startswith('/'):
            path = path[1:]
        return StaticFileHandler.get(self, path, include_body)

    # @classmethod
    # def get_absolute_path(cls, root, path):
    #     if path.startswith('/'):
    #         path = path[1:]
    #     print '*'*80
    #     return StaticFileHandler.get_absolute_path(root, path)