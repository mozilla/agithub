# Copyright 2012-2016 Jonathan Paugh and contributors
# See COPYING for license details
from agithub.base import API, ConnectionProperties, Client


class SalesForce(API):
    """
    SalesForce.com REST API

    Example taken from
    http://www.salesforce.com/us/developer/docs/api_rest/index_Left.htm#CSHID=quickstart_code.htm|StartTopic=Content%2Fquickstart_code.htm|SkinName=webhelp

    >>> from SalesForce import SalesForce
    >>> sf = SalesForce()
    >>> sf.services.data.get()
    (200,
    [{u'label': u"Winter '11",
      u'url': u'/services/data/v20.0',
      u'version': u'20.0'},
    ...
     {u'label': u"Spring '14",
      u'url': u'/services/data/v30.0',
      u'version': u'30.0'}])

    SalseForce allows you to request either XML or JSON based on the
    URL "file extension," like so

    >>> sf.services["data.xml"].get()
    (200, '<?xml version="1.0" encoding="UTF-8"?> ....')

    NB: XML is not automically decoded or de-serialized. Patch the
    ResponseBody class to fix this.
    """
    def __init__(self, *args, **kwargs):
        props = ConnectionProperties(
            api_url='na1.salesforce.com',
            secure_http=True,
        )
        self.setClient(Client(*args, **kwargs))
        self.setConnectionProperties(props)
