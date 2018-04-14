# Copyright 2012-2016 Jonathan Paugh and contributors
# See COPYING for license details
from agithub.base import API, ConnectionProperties, Client


class Facebook(API):
    """
    Facebook Graph API

    The following example taken from
    https://developers.facebook.com/docs/graph-api/quickstart/v2.0

    >>> fb = Facebook()
    >>> fb.facebook.picture.get(redirect='false')
    {u'data': {u'is_silhouette': False,
       u'url':
           u'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-frc3/t1.0-1/p50x50/1377580_10152203108461729_809245696_n.png'}})
    """
    def __init__(self, *args, **kwargs):
        props = ConnectionProperties(
            api_url='graph.facebook.com',
            secure_http=True,
        )
        self.setClient(Client(*args, **kwargs))
        self.setConnectionProperties(props)
