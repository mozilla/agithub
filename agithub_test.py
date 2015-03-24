#!/usr/bin/env python
import agithub
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


if __name__ == '__main__':
    unittest.main()
