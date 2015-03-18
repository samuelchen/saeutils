#!/usr/bin/env python
# coding: utf-8
__author__ = 'Samuel Chen <samuel.net@gmail.com>'

'''
SAE KVDB client bridge for pyutils wrapper

Created on 3/11/2015
'''

from sae.kvdb import KVClient

class SAEKvdb(object):
    '''
    A bridge for pyutils kvdb wrapper to access SAE KVDB.

    e.g.
    from pyutils import KVDBWrapper
    from sae_kvdb import SAEKvdb
    kvclient = KVDBWrapper(SAEKvdb, prefix='PRE:', ...)
    kvclient.set(key,value)
    kvclient.get(key)

    '''

    def __init__(self, **kwargs):
        if 'prefix' in kwargs:
            self.prefix = kwargs['prefix']
            del kwargs['prefix']
        else:
            self.prefix = ''

        self.prefix = str(self.prefix)
        self.kv = KVClient(**kwargs)

    def info(self):
        return self.kv.get_info()

    def get(self, key, **kwargs):
        k = self.gen_key(key)
        return self.kv.get(k)

    def set(self, key, value, **kwargs):
        k = self.gen_key(key)
        return self.kv.set(k, value, **kwargs)

    def delete(self, key, **kwargs):
        k = self.gen_key(key)
        return self.kv.delete(k, **kwargs)

    def exist(self, key, **kwargs):
        k = self.gen_key(key)
        existed = not self.kv.add(k, '')
        if not existed:
            self.kv.delete(k)
        return existed

    def scan(self, cursor='', count=20, **kwargs):
        '''
        Retrieve keys by given arguments
        :param kwargs:
            'count' for retrieve count;
            'cursor' is the key for next time retrieve
        :return:
        '''
        return self.kv.getkeys_by_prefix(prefix=self.prefix, marker=cursor, limit=count, **kwargs)

    def scanv(self, cursor='', count=20, **kwargs):
        '''
        Retrieve key-values by given arguments
        :param kwargs:
            'count' for retrieve count;
            'cursor' is the key for next time retrieve
        :return:
        '''
        return self.kv.get_by_prefix(prefix=self.prefix, marker=cursor, limit=count, **kwargs)

    def mget(self, keys, **kwargs):
        return self.kv.get_multi(keys, key_prefix=self.prefix)

    def gen_key(self, key):
        k = self.prefix + str(key)
        return k