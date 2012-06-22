# Copyright 2012 Jonathan Paugh
# See COPYING for license details
import httplib, urllib
import json
import base64

class Client(object):
  def __init__(self, username=None, password=None, login=None):
    if username is None and login is not None:
      username = login
    elif username is not None and login is not None:
      raise ValueError(
'''You cannot use both login and username. (They are mnemonics, so pick one.)''')
    if password is None and username is not None:
      raise TypeError("You need a password to authenticate as " + username)
    self.username = username
    self.password = password

  def get(self, url, body=None, headers={}, **params):
    url += self.urlencode(params)
    return self.request('GET', url, body, headers)

  def post(self, url, body=None, headers={}, **params):
    url += self.urlencode(params)
    return self.request('POST', url, json.dumps(body), headers)

  def request(self, method, url, body, headers):
    if self.password:
      headers['Authorization'] = 'Basic ' + self.hash_pass()
    print 'cli request:', method, url, body, headers
    #TODO: Context manager
    conn = self.get_connection()
    conn.request(method, url, body, headers)
    response = conn.getresponse()
    status = response.status
    body = response.read()
    pybody = json.loads(body)
    print 'reponse len:', len(pybody)
    conn.close()
    return status, pybody

  def urlencode(self, params):
    if not params:
      return ''
    return '?' + urllib.urlencode(params)

  def hash_pass(self):
    return base64.b64encode('%s:%s' % (self.username, self.password)).strip()

  def get_connection(self):
    return httplib.HTTPSConnection('api.github.com')
