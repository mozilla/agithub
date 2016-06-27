# Copyright 2012-2016 Jonathan Paugh and contributors
# See COPYING for license details
from agithub.base import API, ConnectionProperties, Client


class OpenWeatherMap(API):
    """
    Open Weather Map API
    """
    def __init__(self, *args, **kwargs):
        props = ConnectionProperties(
            api_url='api.openweathermap.org',
            secure_http=False,
        )
        self.setClient(Client(*args, **kwargs))
        self.setConnectionProperties(props)
