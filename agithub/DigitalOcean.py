# Copyright 2012-2016 Jonathan Paugh and contributors
# See COPYING for license details
from agithub.base import API, ConnectionProperties, Client


class DigitalOcean(API):
    """
    Digital Ocean API
    """
    def __init__(self, token=None, *args, **kwargs):
        props = ConnectionProperties(
            api_url='api.digitalocean.com',
            url_prefix='/v2',
            secure_http=True,
            extra_headers={
                'authorization': self.generateAuthHeader(token)
            },
        )
        self.setClient(Client(*args, **kwargs))
        self.setConnectionProperties(props)

    def generateAuthHeader(self, token):
        if token is not None:
            return "Bearer " + token
        return None
