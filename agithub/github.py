# Copyright 2012 Jonathan Paugh
# See COPYING for license details
import re
from client import Client

class Github(object):
  '''The agnostic Github API. It doesn't know, and you don't care.
  >>> from agithub import Github
  >>> g = Github('user', 'pass')
  >>> status, data = g.issues.get(filter='subscribed')
  >>> data
  ... [ list_, of, stuff ]
  >>> status, data = g.repos.jpaugh64.repla.issues[1].get()
  >>> data
  ... { 'dict': 'my issue data', }
  >>> name, repo = 'jpaugh64', 'repla'
  >>> status, data = g.repos[name][repo].issues[1].get()
  ... same thing
  >>> status, data = g.funny.I.donna.remember.that.one.get()
  >>> status
  ... 404

  That's all there is to it. (blah.post() should work, too.)

  NOTE: It is up to you to spell things correctly. Github doesn't even
  try to validate the url you feed it. On the other hand, it
  automatically supports the full API--so why should you care?
  '''
  def __init__(self, *args, **kwargs):
    self.client = Client(*args, **kwargs)
  def __getattr__(self, key):
    return RequestBuilder(self.client).__getattr__(key)

class RequestBuilder(object):
  '''RequestBuilder(client).path.to.resource.method(...)
      stands for
  RequestBuilder(client).client.method('path/to/resource, ...)

  Also, if you use an invalid path, too bad. Just be ready to catch a
  You can use item access instead of attribute access. This is
  convenient for using variables' values and required for numbers.
  bad status from github.com. (Or maybe an httplib.error...)

  To understand the method(...) calls, check out github.client.Client.
  '''
  def __init__(self, client):
    self.client = client
    self.url = ''

  def __getattr__(self, key):
    if key in ('get', 'post'):
      return self.curry(getattr(self.client, key), self.url)
    self.url += '/' + str(key)
    return self

  __getitem__ = __getattr__

  def curry(self, fun, url):
    def f(*args, **kwargs):
      try:
        return fun(url, *args, **kwargs)
      except Exception as e:
        raise

    return f

  def __str__(self):
    '''If you ever stringify this, you've (probably) messed up
    somewhere. So let's give a semi-helpful message.
    '''
    return "I don't know about " + self.url

  def __repr__(self):
    return '<%s: %s>' % (self.__class__, self.__str__)
