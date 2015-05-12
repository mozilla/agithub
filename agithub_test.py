#!/usr/bin/env python
import agithub
import mock
import unittest

class TestGithubObjectCreation(unittest.TestCase):
    def test_user_pw(self):
        gh = agithub.Github('korfuri', '1234')
        self.assertTrue(gh is not None)

        gh = agithub.Github(username='korfuri', password='1234')
        self.assertTrue(gh is not None)

    def test_token(self):
        gh = agithub.Github(username='korfuri', token='deadbeef')
        self.assertTrue(gh is not None)

        gh = agithub.Github(token='deadbeef')
        self.assertTrue(gh is not None)

    def test_token_password(self):
        with self.assertRaises(TypeError):
            gh = agithub.Github(
                username='korfuri', password='1234', token='deadbeef')


class TestRequestBuilder(unittest.TestCase):

    def newRequestBuilder(self):
        return agithub.RequestBuilder(mock.Client())

    def test_pathByGetAttr(self):
        rb = self.newRequestBuilder()
        rb.hug.an.octocat
        self.assertEqual(rb.url, "/hug/an/octocat")

    def test_callMethodDemo(self):
        rb = self.newRequestBuilder()
        self.assertEqual(rb.path.demo(),
                { "methodName" : "demo"
                , "args" : ()
                , "params" : { "url" : "/path" }
                })
    def test_pathByGetItem(self):
        rb = self.newRequestBuilder()
        rb["hug"][1]["octocat"]
        self.assertEqual(rb.url, "/hug/1/octocat")

    def test_callMethodDemo(self):
        rb = self.newRequestBuilder()
        self.assertEqual(rb.path.demo(),
                { "methodName" : "demo"
                , "args" : ()
                , "params" : { "url" : "/path" }
                })

    def test_callMethodTest(self):
        rb = self.newRequestBuilder()
        self.assertEqual(rb.path.test(),
                { "methodName" : "test"
                , "args" : ()
                , "params" : { "url" : "/path" }
                })

class TestClient(unittest.TestCase):
    def newClient(self, *args, **params):
        return agithub.Client(*args, **params)

    def test_anonymousClient(self):
        client = self.newClient()

    def test_passwordClient(self):
        client = self.newClient(username="user", password="freepass")

if __name__ == '__main__':
    unittest.main()
