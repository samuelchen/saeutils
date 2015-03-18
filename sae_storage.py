#!/usr/bin/env python
# coding: utf-8
__author__ = 'Samuel Chen <samuel.net@gmail.com>'

'''
SAE storage bridges for pyutils Wrapper

Created on 3/11/2015
'''

from sae.storage import Bucket, Connection

class SAEStorageKVDB(object):
    '''
    A bridge for pyutils kvdb wrapper to access sae storage like a kvdb.

    e.g.
    from pyutils import KVDBWrapper
    from sae_storage import SAEStorageKVDB
    kvclient = KVDBWrapper(SAEStorageKVDB, bucket='mybucket', accesskey='xxx', secretkey='yyy', account='myapp', prefix='PRE:', ...)
    kvclient.set(key,value)
    kvclient.get(key)
    '''

    def __init__(self, **kwargs):
        bucket = kwargs['bucket'] if 'bucket' in kwargs else ''
        accesskey = kwargs['accesskey'] if 'accesskey' in kwargs else ''
        secretkey = kwargs['secretkey'] if 'secretkey' in kwargs else ''
        account = kwargs['account'] if 'account' in kwargs else '' # app name
        retries = long(kwargs['retries']) if 'retries' in kwargs else 3 # app name

        self.prefix = kwargs['prefix'] if 'prefix' in kwargs else ''

        if accesskey and secretkey and account:
            conn = Connection(accesskey, secretkey, account, retries)
            self.kv = conn.get_bucket(bucket)
        else:
            self.kv = Bucket(bucket)

    def info(self):
        return self.kv.stat()

    def get(self, key, **kwargs):
        k = self.prefix + key
        return self.kv.get_object(k, **kwargs)

    def set(self, key, value, **kwargs):
        k = self.prefix + key
        return self.kv.put_object(k, value, **kwargs)

    def delete(self, key, **kwargs):
        k = self.prefix + key
        return self.kv.delete_object(k, **kwargs)

    def exist(self, key, **kwargs):
        k = self.prefix + key
        rc = False
        st = self.kv.stat_object(k)
        if st: rc = True
        return rc

    def scan(self, cursor=None, count=100, **kwargs):
        '''
        Retrieve keys by given arguments
        :param kwargs:
            'count' for retrieve count;
            'cursor' is the key for next time retrieve
        :return:
        '''
        return self.kv.c(prefix=self.prefix, marker=cursor, limit=count, **kwargs)

    def scanv(self, cursor=None, count=100, **kwargs):
        '''
        Retrieve key-values by given arguments
        :param kwargs:
            'count' for retrieve count;
            'cursor' is the key for next time retrieve
        :return:
        '''
        return self.kv.list(prefix=self.prefix, marker=cursor, limit=count, **kwargs)

    def mget(self, keys, **kwargs):
        for key in keys:
            k = self.prefix + key
            val = self.get(k, **kwargs)
            yield val