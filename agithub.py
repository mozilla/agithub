# Copyright 2012-2014 Jonathan Paugh
# See COPYING for license details
import json
import base64
import re
from functools import partial, update_wrapper

import sys
if sys.version_info[0:2] > (3,0):
    import http.client
    import urllib.parse
else:
    import httplib as http
    http.client = http
    import urllib as urllib
    urllib.parse = urllib

class Github(object):
    '''The agnostic Github API. It doesn't know, and you don't care.
    >>> from agithub import Github
    >>> g = Github('user', 'pass')
    >>> status, data = g.issues.get(filter='subscribed')
    >>> data
    ... [ list_, of, stuff ]

    >>> status, data = g.repos.jpaugh.repla.issues[1].get()
    >>> data
    ... { 'dict': 'my issue data', }

    >>> name, repo = 'jpaugh', 'repla'
    >>> status, data = g.repos[name][repo].issues[1].get()
    ... same thing

    >>> status, data = g.funny.I.donna.remember.that.one.get()
    >>> status
    ... 404

    That's all there is to it. (blah.post() should work, too.)

    NOTE: It is up to you to spell things correctly. A Github object
    doesn't even try to validate the url you feed it. On the other hand,
    it automatically supports the full API--so why should you care?
    '''
    def __init__(self, *args, **kwargs):
        self.client = Client(*args, **kwargs)
    def __getattr__(self, key):
        return RequestBuilder(self.client).__getattr__(key)

class RequestBuilder(object):
    '''RequestBuilders build HTTP requests via an HTTP-idiomatic notation,
    or via "normal" method calls.

    Specifically,
    >>> RequestBuilder(client).path.to.resource.METHOD(...)
    is equivalent to
    >>> RequestBuilder(client).client.METHOD('path/to/resource, ...)
    where METHOD is replaced by get, post, head, etc.

    Also, if you use an invalid path, too bad. Just be ready to catch a
    bad status from github.com. (Or maybe an httplib.error...)

    You can use item access instead of attribute access. This is
    convenient for using variables\' values and required for numbers.
    >>> Github('user','pass').whatever[1][x][y].post()

    To understand the method(...) calls, check out github.client.Client.
    '''
    def __init__(self, client):
        self.client = client
        self.url = ''

    def __getattr__(self, key):
        if key in self.client.http_methods:
            mfun = getattr(self.client, key)
            fun = partial(mfun, url=self.url)
            return update_wrapper(fun, mfun)
        else:
            self.url += '/' + str(key)
            return self

    __getitem__ = __getattr__

    def __str__(self):
        '''If you ever stringify this, you've (probably) messed up
        somewhere. So let's give a semi-helpful message.
        '''
        return "I don't know about " + self.url

    def __repr__(self):
        return '%s: %s' % (self.__class__, self.url)

class Client(object):
    http_methods = (
            'head',
            'get',
            'post',
            'put',
            'delete',
            )

    def __init__(self, username=None, password=None, token=None):
        self.username = username
        if username is not None:
            if password is None and token is None:
                raise TypeError("You need a password to authenticate as " + username)
            if password is not None and token is not None:
                raise TypeError("You cannot use both password and oauth token authenication")

            if password is not None:
                self.auth_header = self.hash_pass(password)
            elif token is not None:
                self.auth_header = 'Token %s' % token

    def head(self, url, headers={}, **params):
        url += self.urlencode(params)
        return self.request('HEAD', url, None, headers)

    def get(self, url, headers={}, **params):
        url += self.urlencode(params)
        return self.request('GET', url, None, headers)

    def post(self, url, body=None, headers={}, **params):
        url += self.urlencode(params)
        return self.request('POST', url, json.dumps(body), headers)

    def put(self, url, body=None, headers={}, **params):
        url += self.urlencode(params)
        return self.request('PUT', url, json.dumps(body), headers)

    def delete(self, url, headers={}, **params):
        url += self.urlencode(params)
        return self.request('DELETE', url, None, headers)


    def request(self, method, url, body, headers):
        '''Low-level networking. All HTTP-method methods call this'''
        if self.username:
                headers['Authorization'] = self.auth_header
        headers['User-Agent'] = 'agithub'

        #TODO: Context manager
        conn = self.get_connection()
        conn.request(method, url, body, headers)
        response = conn.getresponse()
        status = response.status
        charset = self.get_charset(response)
        body = response.read().decode(charset)

        try:
            pybody = json.loads(body)
        except ValueError:
            pybody = body

        conn.close()
        return status, pybody

    def urlencode(self, params):
        if not params:
            return ''
        return '?' + urllib.parse.urlencode(params)

    def get_charset(self, response):
        ctype = response.getheader('Content-Type')

        try:
            start = 8 + ctype.index('charset=')
            end = ctype.index(';', start)
            charset = ctype[start:end].rstrip()
        except:
            charset = 'ISO-8859-1' #TODO

        return charset

    def get_charset(self, response):
        ctype = response.getheader('Content-Type')

        try:
            start = 8 + ctype.index('charset=')
            end = ctype.index(';', start)
            charset = ctype[start:end].rstrip()
        except:
            charset = 'ISO-8859-1' #TODO

        return charset

    def hash_pass(self, password):
        return 'Basic ' + base64.b64encode('%s:%s' % (self.username, password)).strip()

    def get_connection(self):
        return http.client.HTTPSConnection('api.github.com')
