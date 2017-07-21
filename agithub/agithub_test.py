#!/usr/bin/env python
# Copyright 2012-2016 Jonathan Paugh and contributors
# See COPYING for license details
from agithub.GitHub import GitHub
from agithub.base import IncompleteRequest, ConnectionProperties
import agithub.mock as mock
import unittest


class TestGitHubObjectCreation(unittest.TestCase):
    def test_user_pw(self):
        gh = GitHub('korfuri', '1234')
        self.assertTrue(gh is not None)

        gh = GitHub(username='korfuri', password='1234')
        self.assertTrue(gh is not None)

    def test_token(self):
        gh = GitHub(username='korfuri', token='deadbeef')
        self.assertTrue(gh is not None)

        gh = GitHub(token='deadbeef')
        self.assertTrue(gh is not None)

    def test_token_password(self):
        with self.assertRaises(TypeError):
            gh = GitHub(
                username='korfuri', password='1234', token='deadbeef')


class TestIncompleteRequest(unittest.TestCase):
    def newIncompleteRequest(self):
        return IncompleteRequest(mock.Client())

    def test_pathByGetAttr(self):
        rb = self.newIncompleteRequest()
        rb.hug.an.octocat
        self.assertEqual(rb.url, "/hug/an/octocat")

    def test_callMethodDemo(self):
        rb = self.newIncompleteRequest()
        self.assertEqual(rb.path.demo(),
                         {
                             "methodName": "demo",
                             "args": (),
                             "params": {"url": "/path"}
                         })

    def test_pathByGetItem(self):
        rb = self.newIncompleteRequest()
        rb["hug"][1]["octocat"]
        self.assertEqual(rb.url, "/hug/1/octocat")

    def test_callMethodTest(self):
        rb = self.newIncompleteRequest()
        self.assertEqual(rb.path.test(),
                         {
                             "methodName": "test",
                             "args": (),
                             "params": {"url": "/path"}
                         })


class TestConnectionProperties(unittest.TestCase):
    def test_url_prefix(self):
        cp = ConnectionProperties(url_prefix='/pre/fix')

        self.assertIsNotNone(cp.url_prefix)
        self.assertIsNone(cp.url_postfix)

        url = cp.constructUrl('/find/files')
        self.assertEqual(url, '/pre/fix/find/files')

    def test_url_postfix(self):
        cp = ConnectionProperties(url_postfix='/post/fix')

        self.assertIsNone(cp.url_prefix)
        self.assertIsNotNone(cp.url_postfix)

        url = cp.constructUrl('/find/files')
        self.assertEqual(url, '/find/files/post/fix')

    def test_url_prefix_and_url_postfix(self):
        cp = ConnectionProperties(url_prefix='/pre/fix', url_postfix='/post/fix')

        self.assertIsNotNone(cp.url_prefix)
        self.assertIsNotNone(cp.url_postfix)

        url = cp.constructUrl('/find/files')
        self.assertEqual(url, '/pre/fix/find/files/post/fix')

    def test_url_postfix_with_parameters(self):
        cp = ConnectionProperties(url_postfix='/post/fix')

        url = cp.constructUrl('/find/files?key=value')
        self.assertEqual(url, '/find/files/post/fix?key=value')


if __name__ == '__main__':
    unittest.main()
