# Copyright 2012-2016 Jonathan Paugh and contributors
# See COPYING for license details
from agithub.base import API, ConnectionProperties, Client


class Bitbucket(API):
    """
    Bitbucket API

    >>> bt = Bitbucket()
    >>> bt.hook_events.get()
    """
    def __init__(self, *args, **kwargs):
        props = ConnectionProperties(
            api_url='api.bitbucket.org',
            url_prefix='/2.0',
            secure_http=True,
        )
        self.setClient(Client(*args, **kwargs))
        self.setConnectionProperties(props)
