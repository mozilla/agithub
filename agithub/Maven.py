# Copyright 2012-2016 Jonathan Paugh and contributors
# See COPYING for license details
from agithub.base import API, Client, ConnectionProperties


class Maven(API):
    """
    Maven Search API
    """
    def __init__(self, *args, **kwargs):
        props = ConnectionProperties(
            api_url='search.maven.org',
            url_prefix='/solrsearch',
            secure_http=True,
        )
        self.setClient(Client(*args, **kwargs))
        self.setConnectionProperties(props)
