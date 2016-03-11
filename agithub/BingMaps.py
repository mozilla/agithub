# Copyright 2012-2016 Jonathan Paugh and contributors
# See COPYING for license details
from agithub.base import API, ConnectionProperties, Client

class BingMaps(API):
    '''
    Bing REST API
    '''
    def __init__(self, *args, **kwargs):
        props = ConnectionProperties(
                      api_url = 'spatial.virtualearth.net'
                    , url_prefix = '/REST/v1'
                    , secure_http = True
                    , default_url_parameters = {
                          'key' : kwargs.pop('queryKey', None)
                        }
                    )
        self.setClient(Client(*args, **kwargs))
        self.setConnectionProperties(props)
