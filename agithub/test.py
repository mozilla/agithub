#!/usr/bin/env python
# Copyright 2012-2016 Jonathan Paugh and contributors
# See COPYING for license details
from __future__ import print_function
from agithub.GitHub import GitHub

##
# Test harness
###

# Test results
Pass = 'Pass'
Fail = 'Fail'
Skip = 'Skip'


class Test(object):
    _the_label = 'test'
    _the_testno = 0
    tests = {}

    def gatherTests(self, testObj):
        for test in dir(self):
            if test.startswith('test_'):
                self.tests[test] = getattr(testObj, test)
        print(self.tests)

    def doTestsFor(self, api):
        """Run all tests over the given API session"""
        results = []
        for name, test in self.tests.items():
            self._the_label = name
            results.append(self.runTest(test, api))

        fails = skips = passes = 0
        for res in results:
            if res == Pass:
                passes += 1
            elif res == Fail:
                fails += 1
            elif res == Skip:
                skips += 1
            else:
                raise ValueError('Bad test result ' + (res))

        print(
                '\n'
                ' Results\n'
                '--------------------------------------\n'
                'Tests Run:     ', len(results), '\n'
                '      Passed:  ', passes, '\n'
                '      Failed:  ', fails, '\n'
                '      Skipped: ', skips
            )

    def runTest(self, test, api):
        """Run a single test with the given API session"""
        self._the_testno += 1
        (stat, _) = test(api)

        global Pass, Skip, Fail

        if stat in [Pass, Fail, Skip]:
            return stat
        elif stat < 400:
            result = Pass
        elif stat >= 500:
            result = Skip
        else:
            result = Fail

        self.label(result)
        return result

    def setlabel(self, lbl):
        """Set the global field _the_label, which is used by runTest"""
        self._the_label += ' ' + lbl

    def label(self, result):
        """Print out a test label showing the result"""
        print(result + ':', self._the_testno, self._the_label)

    def haveAuth(self, api):
        username = getattr(api.client, 'username', NotImplemented)
        if username == NotImplemented or username is None:
            return False
        else:
            return True


##
# Tests
###
class Basic (Test):
    def __init__(self):
        self.gatherTests(self)

    def test_zen(self, api):
        self.setlabel('Zen')
        return api.zen.get()

    def test_head(self, api):
        self.setlabel('HEAD')
        return api.head()

    def test_userRepos(self, api):
        if not self.haveAuth(api):
            return (Skip, ())

        return api.user.repos.head()

##
# Utility
###


# Session initializers
def initAnonymousSession(klass):
    return klass()


def initAuthenticatedSession(klass, **kwargs):
    for k in kwargs:
        if k not in ['username', 'password', 'token']:
            raise ValueError('Invalid test parameter: ' + str(k))

    return klass(**kwargs)


# UI
def yesno(ans):
    """Convert user input (Yes or No) to a boolean"""
    ans = ans.lower()
    if ans == 'y' or ans == 'yes':
        return True
    else:
        return False


##
# Main
###

if __name__ == '__main__':
    anonSession = initAnonymousSession(GitHub)
    authSession = None

    ans = input(
        'Some of the tests require an authenticated session. '
        'Do you want to provide a username and password [y/N]? '
    )

    if yesno(ans):
        username = input('Username: ')
        password = input('Password (plain text): ')
        authSession = initAuthenticatedSession(
            GitHub,
            username=username,
            password=password,
        )

    tests = filter(lambda var: var.startswith('test_'), globals().copy())
    tester = Basic()

    print('Unauthenticated tests')
    tester.doTestsFor(anonSession)

    print()
    if authSession is None:
        print('Skipping Authenticated tests')
    else:
        print('Authenticated tests')
        tester.doTestsFor(authSession)
