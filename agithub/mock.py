# Mock objects for testing
# Copyright 2012-2016 Jonathan Paugh and contributors
# See COPYING for license details


class Client(object):
    http_methods = ('demo', 'test')

    def __init__(self, username=None, password=None, token=None,
                 connection_properties=None):
        pass

    def setConnectionProperties(self, props):
        pass

    def demo(self, *args, **params):
        return self.methodCalled('demo', *args, **params)

    def test(self, *args, **params):
        return self.methodCalled('test', *args, **params)

    def methodCalled(self, methodName, *args, **params):
        return {
            'methodName': methodName,
            'args': args,
            'params': params
        }
