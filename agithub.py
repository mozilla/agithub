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

VERSION = [2,0]
STR_VERSION = 'v' + '.'.join(str(v) for v in VERSION)

# These headers are implicitly included in each request; however, each
# can be explicitly overridden by the client code. (Used in Client
# objects.)
DEFAULT_HEADERS = {
      'user-agent': 'agithub/' + STR_VERSION
    }

class API(object):
    '''
    The toplevel object, and the "entry-point" into the client API.
    Subclass this to develop an application for a particular REST API.

    Model your __init__ after the GitHub example.
    '''
    def __init__(self, *args, **kwargs):
        raise Exception (
                'Please subclass API and override __init__()  to'
                'provide a ConnectionProperties object. See the GitHub'
                ' class for an example'
                )

    def setClient(self, client):
        self.client = client

    def setConnectionProperties(self, props):
        self.client.setConnectionProperties(props)

    def __getattr__(self, key):
        return RequestBuilder(self.client).__getattr__(key)
    __getitem__ = __getattr__

    def __repr__(self):
        return RequestBuilder(self.client).__repr__()

    def getheaders(self):
        return self.client.headers

class GitHub(API):
    '''The agnostic GitHub API. It doesn't know, and you don't care.
    >>> from agithub import GitHub
    >>> g = GitHub('user', 'pass')
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

    NOTE: It is up to you to spell things correctly. A GitHub object
    doesn't even try to validate the url you feed it. On the other hand,
    it automatically supports the full API--so why should you care?
    '''
    def __init__(self, *args, **kwargs):
        props = ConnectionProperties(
                    api_url = 'api.github.com',
                    secure_http = True,
                    extra_headers = {
                        'accept' :    'application/vnd.github.v3+json'
                        }
                    )

        self.setClient(Client(*args, **kwargs))
        self.setConnectionProperties(props)

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
    >>> GitHub('user','pass').whatever[1][x][y].post()

    To understand the method(...) calls, check out github.client.Client.
    '''
    def __init__(self, client):
        self.client = client
        self.url = ''

    def __getattr__(self, key):
        if key in self.client.httpMethods:
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
    httpMethods = (
            'head',
            'get',
            'post',
            'put',
            'delete',
            'patch',
            )

    defaultHeaders = {}
    headers = None

    def __init__(self, username=None,
            password=None, token=None,
            connection_properties=None
            ):

        # Set up connection properties
        if connection_properties is not None:
            self.setConnectionProperties(connection_properties)

        # Set up authentication
        self.username = username
        if username is not None:
            if password is None and token is None:
                raise TypeError("You need a password to authenticate as " + username)
            if password is not None and token is not None:
                raise TypeError("You cannot use both password and OAuth token authentication")

            self.authHeader = None
            if password is not None:
                self.authHeader = self.hashPassword(password)
            elif token is not None:
                self.authHeader = 'Token %s' % token

    def setConnectionProperties(self, props):
        '''
        Initialize the connection properties. This must be called
        (either by passing connection_properties=... to __init__ or
        directly) before any request can be sent.
        '''
        if type(props) is not ConnectionProperties:
            raise TypeError("Client.setConnectionProperties: Expected ConnectionProperties object")

        self.prop = props
        if self.prop.extra_headers is not None:
            self.defaultHeaders = DEFAULT_HEADERS.copy()
            self.defaultHeaders.update(self.prop.extra_headers)

        # Enforce case restrictions on self.defaultHeaders
        self.defaultHeaders = self.caseConvertHeaders(self.defaultHeaders)

    def head(self, url, headers={}, **params):
        url += self.urlEncode(params)
        return self.request('HEAD', url, None, headers)

    def get(self, url, headers={}, **params):
        url += self.urlEncode(params)
        return self.request('GET', url, None, headers)

    def post(self, url, body=None, headers={}, **params):
        url += self.urlEncode(params)
        return self.request('POST', url, body, headers)

    def put(self, url, body=None, headers={}, **params):
        url += self.urlEncode(params)
        return self.request('PUT', url, body, headers)

    def delete(self, url, headers={}, **params):
        url += self.urlEncode(params)
        return self.request('DELETE', url, None, headers)

    def patch(self, url, body=None, headers={}, **params):
        '''
        Do a http patch request on the given url with given body,
        headers and parameters Parameters is a dictionary that will will
        be url-encoded
        '''
        url += self.urlEncode(params)
        return self.request(self.PATCH, url, body, headers)

    def request(self, method, url, body, headers):
        '''Low-level networking. All HTTP-method methods call this'''

        headers = self.updateWithDefaultHeaders(headers)

        if self.username:
            headers['authorization'] = self.authHeader

        reqBody = RequestBody(body, headers)
        conn = self.getConnection()
        conn.request(method, url, reqBody.process(), headers)
        response = conn.getresponse()
        status = response.status
        resBody = ResponseBody(response)
        self.headers = response.getheaders()

        conn.close()
        return status, resBody.process()

    def caseConvertHeaders(self, headers):
        # Convert header names to a uniform case
        tmpDict = {}
        for k,v in headers.items():
            tmpDict[k.lower()] = v
        return tmpDict

    def updateWithDefaultHeaders(self, headers):
        # Add default headers (if absent)
        headers = self.caseConvertHeaders(headers)
        for k,v in self.defaultHeaders.items():
            if k not in headers:
                headers[k] = v
        return headers

    def urlEncode(self, params):
        if not params:
            return ''
        return '?' + urllib.parse.urlEncode(params)

    def hashPassword(self, password):
        authStr = ('%s:%s' % (self.username, password)).encode('utf-8')
        return 'Basic '.encode('utf-8') + base64.b64encode(authStr).strip()

    def getConnection(self):
        if self.prop.secure_http:
            conn = http.client.HTTPSConnection(self.prop.api_url)
        elif self.username is None:
            conn = http.client.HTTPConnection(self.prop.api_url)
        else:
            raise ConnectionError('Refusing to authenticate over'
                    ' non-secure  (HTTP) connection. To override, edit'
                    ' the source'
                    )

        return conn

class Body(object):
    '''Superclass for ResponseBody and RequestBody'''

    def parseContentType(self, ctype):
        '''
        Parse the Content-Type header, returning the media-type and any
        parameters
        '''

        if ctype is None:
            self.mediatype = 'application/octet-stream'
            self.ctypeParameters = { 'charset': 'ISO-8859-1' }
            return

        params = ctype.split(';')
        self.mediatype = params.pop(0).strip()

        # Parse parameters
        if len(params) > 0:
            params = map( lambda s : s.strip().split('=')
                        , params
                        )

            paramDict = {}
            for attribute, value in params:
                # TODO: Find out if specifying an attribute multiple
                # times is even okay, and how it should be handled
                attribute = attribute.lower()
                if attribute in paramDict:
                    if type(paramDict[attribute]) is not list:
                        # Convert singleton value to value-list
                        paramDict[attribute] = [paramDict[attribute]]
                    # Insert new value along with pre-existing ones
                    paramDict[attribute] += value
                else:
                    # Insert singleton attribute value
                    paramDict[attribute] = value
            self.ctypeParameters = paramDict

        else:
            self.ctypeParameters = {}

        if 'charset' not in self.ctypeParameters:
            self.ctypeParameters['charset'] = 'ISO-8859-1'
            # NB: ISO-8859-1 is specified (RFC 2068) as the default
            # charset in case none is provided

    def funMangledMediaType(self):
        '''
        Mangle the media type into a suitable function name
        '''
        return self.mediatype.replace('-','_').replace('/','_')


class ResponseBody(Body):
    '''
    Decode a response from the server, respecting the Content-Type field
    '''
    def __init__(self, response):
        self.response = response
        self.body = response.read()
        self.parseContentType(self.response.getheader('Content-Type'))
        self.encoding = self.ctypeParameters['charset']

    def decodeBody(self):
        '''
        Decode (and replace) self.body via the charset encoding
        specified in the content-type header
        '''
        self.body = self.body.decode(self.encoding)

    def process(self):
        '''
        Retrieve the body of the response, encoding it into a usable
        form based on the media-type (mime-type)
        '''
        handlerName = self.funMangledMediaType()
        handler = getattr(  self, handlerName,
                            self.application_octet_stream
                            )
        return handler()


    ## media-type handlers

    def application_octet_stream(self):
        '''Handler for binary data and unknown media-types. Importantly,
        it does absolutely no pre-processing of the body, which means it
        will not mess it up.
        '''
        return self.body

    def application_json(self):
        '''Handler for application/json media-type'''
        self.decodeBody()

        try:
            pybody = json.loads(self.body)
        except ValueError:
            pybody = self.body

        return pybody

    text_javascript = application_json
    # XXX: This isn't technically correct, but we'll hope for the best.
    # Patches welcome!

    # Insert new Response media-type handlers here

class RequestBody(Body):
    '''
    Encode a request body from the client, respecting the Content-Type
    field
    '''
    def __init__(self, body, headers):
        self.body = body
        self.headers = headers
        self.parseContentType(
                getattr(self.headers, 'content-type', None)
                )
        self.encoding = self.ctypeParameters['charset']

    def encodeBody(self):
        '''
        Encode (and overwrite) self.body via the charset encoding
        specified in the request headers
        '''
        self.body = self.body.encode(self.encoding)

    def process(self):
        '''
        Process the request body by applying a media-type specific
        handler to it. Some media-types need charset encoding as well,
        and it is up to the handler to do this by calling
        self.encodeBody()
        '''
        if self.body is None:
            return None

        handlerName = self.funMangledMediaType()
        handler = getattr(  self, handlerName,
                            self.application_octet_stream
                            )
        return handler()

    ## media-type handlers

    def application_octet_stream(self):
        '''Handler for binary data and unknown media-types. Importantly,
        it does absolutely no pre-processing of the body, which means it
        will not mess it up.
        '''
        return self.body

    def application_json(self):
        self.body = json.dumps(self.body)
        self.encodeBody()
        return self.body

    # Insert new Request media-type handlers here


class ConnectionProperties(object):
    __slots__ = ['api_url', 'secure_http', 'extra_headers']

    def __init__(self, **props):
        # Initialize attribute slots
        for key in self.__slots__:
            setattr(self, key, None)

        # Fill attribute slots with custom values
        for key, val in props.items():
            if key not in ConnectionProperties.__slots__:
                raise TypeError("Invalid connection property: " + str(key))
            else:
                setattr(self, key, val)
