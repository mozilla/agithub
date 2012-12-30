# Copyright 2012 Jonathan Paugh
# See COPYING for license details
import httplib, urllib
import json
import base64

class Client(object):
  http_methods = (
      'get',
      'post',
      'delete',
      'put',
      )

  def __init__(self, username=None, password=None, token=None):
    if username is not None:
      if password is None and token is None:
        raise TypeError("You need a password to authenticate as " + username)
      if password is not None and token is not None:
        raise TypeError("You cannot use both password and oauth token authenication")

      if password is not None:
        self.auth_header = self.hash_pass(password)
      elif token is not None:
        self.auth_header = 'Token %s' % token

    self.username = username

  def get(self, url, headers={}, **params):
    url += self.urlencode(params)
    return self.request('GET', url, None, headers)

  def delete(self, url, headers={}, **params):
    url += self.urlencode(params)
    return self.request('DELETE', url, None, headers)

  def post(self, url, body=None, headers={}, **params):
    url += self.urlencode(params)
    return self.request('POST', url, json.dumps(body), headers)

  def put(self, url, body=None, headers={}, **params):
    url += self.urlencode(params)
    return self.request('PUT', url, json.dumps(body), headers)

  def request(self, method, url, body, headers):
    if self.username:
      headers['Authorization'] = self.auth_header
    print 'cli request:', method, url, body, headers
    #TODO: Context manager
    conn = self.get_connection()
    conn.request(method, url, body, headers)
    response = conn.getresponse()
    status = response.status
    body = response.read()
    try:
      pybody = json.loads(body)
    except ValueError:
      pybody = body
    print 'reponse len:', len(pybody)
    conn.close()
    return status, pybody

  def urlencode(self, params):
    if not params:
      return ''
    return '?' + urllib.urlencode(params)

  def hash_pass(self, password):
    return 'Basic ' + base64.b64encode('%s:%s' % (self.username, password)).strip()

  def get_connection(self):
    return httplib.HTTPSConnection('api.github.com')
