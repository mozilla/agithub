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


class TestIncompleteRequest(unittest.TestCase):

    def newIncompleteRequest(self):
        return agithub.IncompleteRequest(mock.Client())

    def test_pathByGetAttr(self):
        rb = self.newIncompleteRequest()
        rb.hug.an.octocat
        self.assertEqual(rb.url, "/hug/an/octocat")

    def test_callMethodDemo(self):
        rb = self.newIncompleteRequest()
        self.assertEqual(rb.path.demo(),
                { "methodName" : "demo"
                , "args" : ()
                , "params" : { "url" : "/path" }
                })
    def test_pathByGetItem(self):
        rb = self.newIncompleteRequest()
        rb["hug"][1]["octocat"]
        self.assertEqual(rb.url, "/hug/1/octocat")

    def test_callMethodDemo(self):
        rb = self.newIncompleteRequest()
        self.assertEqual(rb.path.demo(),
                { "methodName" : "demo"
                , "args" : ()
                , "params" : { "url" : "/path" }
                })

    def test_callMethodTest(self):
        rb = self.newIncompleteRequest()
        self.assertEqual(rb.path.test(),
                { "methodName" : "test"
                , "args" : ()
                , "params" : { "url" : "/path" }
                })

if __name__ == '__main__':
    unittest.main()
