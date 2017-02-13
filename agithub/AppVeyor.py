# Copyright 2012-2017 Jonathan Paugh and contributors
# See COPYING for license details

# AppVeyor REST API: https://www.appveyor.com/docs/api/
# Version 1.0 (2017-02-13) by topic2k@atlogger.de

from agithub.base import API, ConnectionProperties, Client


class AppVeyor(API):
    """
    The agnostic AppVeyor API. It doesn't know, and you don't care.
    >>> from agithub.AppVeyor import AppVeyor
    >>> ci = AppVeyor('<your AppVeyor API token>')
    >>> status, data = ci.api.projects.get()
    >>> data
    ... [ list_, of, stuff ]

    >>> status, data = ci.api.projects.topic2k.eventghost.get()
    >>> data
    ... { 'project': <project data>, }

    >>> account_name = 'topic2k'
    >>> project_slug = 'eventghost'
    >>> status, data = ci.api.projects[account_name][project_slug].get()
    ... same as above

    >>> status, data = ci.api.projects.topic2k.eventghost.buildcache.delete()
    >>> status
    ... 204

    That's all there is to it. (blah.post() should work, too.)

    NOTE: It is up to you to spell things correctly. An AppVeyor object
    doesn't even try to validate the url you feed it. On the other hand,
    it automatically supports the full API--so why should you care?
    """
    def __init__(self, token, accept='application/json', *args, **kwargs):
        extra_headers = dict(
            Accept=accept,
            Authorization='Bearer {0}'.format(token)
        )
        props = ConnectionProperties(
            api_url='ci.appveyor.com',
            secure_http=True,
            extra_headers=extra_headers
        )
        self.setClient(Client(*args, **kwargs))
        self.setConnectionProperties(props)
