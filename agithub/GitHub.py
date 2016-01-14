from base import *

class Github(API):
    '''The agnostic Github API. It doesn't know, and you don't care.
    >>> from agithub import Github
    >>> g = Github('user', 'pass')
    >>> status, data = g.issues.get(filter='subscribed')
    >>> data
    ... [ list_, of, stuff ]

    >>> status, data = g.repos.jpaugh.repla.issues[1].get()
    >>> data
    ... { 'dict': 'my issue data', }

    >>> name, repo = 'jpaugh', 'repla'
    >>> status, data = g.repos[name][repo].issues[1].get()
    ... same thing

    >>> status, data = g.funny.I.donna.remember.that.one.get()
    >>> status
    ... 404

    That's all there is to it. (blah.post() should work, too.)

    NOTE: It is up to you to spell things correctly. A Github object
    doesn't even try to validate the url you feed it. On the other hand,
    it automatically supports the full API--so why should you care?
    '''
    def __init__(self, *args, **kwargs):
        props = ConnectionProperties(
                    api_url = 'api.github.com',
                    secure_http = True,
                    extra_headers = {
                        'accept' :    'application/vnd.github.v3+json'
                        }
                    )

        self.setClient(Client(*args, **kwargs))
        self.setConnectionProperties(props)

