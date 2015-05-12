# Mock module for http.client

class MethodCallRecorder(object):
    method_calls = []

    def recordMethodCall(self, methodName, args, params):
        self.method_calls.append(MethodCall(methodName, args, params))

    class MethodCall(object):
        __slots__ = "method args params".split()

        def __init__(self, methodName, args, params):
            self.method = methodName
            self.args = args
            self.params = params

        def __str__(self):
            return {
                "method": self.method,
                "args" : self.args,
                "parms" : self.parms
                }.__str__()


class HTTPConnection(MethodCallRecorder):
    connType = "HTTP"
    def __init__(self, *args, **params):
        self.recordMethodCall("__init__", args, params)

    def request(self, *args, **parms):
        self.recordMethodCall("request", args, params)

    def getresponse(self, *args, **parms):
        self.recordMethodCall("getresponse", args, params)
        return Response()

    def close(self, *args, **parms):
        recordMethodCall("close", args, params)


class HTTPSConnection(HTTPConnection):
    connType = "HTTPS"


class Response(MethodCallRecorder):
    status = "status"

    # headers and body should be overridden by test code
    # if that should be tested
    headers = {
        "content-type": "text/plain"
        }
    body = "body text"

    def getheader(self, *args, **params):
        self.recordMethodCall("getheader", args, params)
        return headers[args[0].lower()]

    def getheaders(self, *args, **params):
        self.recordMethodCall("getheaders", args, params)
        return headers

    def read(self, *args, **params):
        self.recordMethodCall("read", args, params)
        return self.body
