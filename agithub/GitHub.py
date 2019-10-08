# Copyright 2012-2016 Jonathan Paugh and contributors
# See COPYING for license details
import base64
import time
import re
import logging

from agithub.base import (
    API, ConnectionProperties, Client, RequestBody, ResponseBody)

logger = logging.getLogger(__name__)


class GitHub(API):
    """
    The agnostic GitHub API. It doesn't know, and you don't care.
    >>> from agithub.GitHub import GitHub
    >>> g = GitHub('user', 'pass')
    >>> status, data = g.issues.get(filter='subscribed')
    >>> data
    [ list_, of, stuff ]

    >>> status, data = g.repos.jpaugh.repla.issues[1].get()
    >>> data
    { 'dict': 'my issue data', }

    >>> name, repo = 'jpaugh', 'repla'
    >>> status, data = g.repos[name][repo].issues[1].get()
    same thing

    >>> status, data = g.funny.I.donna.remember.that.one.get()
    >>> status
    404

    That's all there is to it. (blah.post() should work, too.)

    NOTE: It is up to you to spell things correctly. A GitHub object
    doesn't even try to validate the url you feed it. On the other hand,
    it automatically supports the full API--so why should you care?
    """
    def __init__(self, username=None, password=None, token=None,
                 *args, **kwargs):
        extraHeaders = {'accept': 'application/vnd.github.v3+json'}
        auth = self.generateAuthHeader(username, password, token)
        if auth is not None:
            extraHeaders['authorization'] = auth
        props = ConnectionProperties(
            api_url=kwargs.pop('api_url', 'api.github.com'),
            secure_http=True,
            extra_headers=extraHeaders
        )

        self.setClient(GitHubClient(*args, **kwargs))
        self.setConnectionProperties(props)

    def generateAuthHeader(self, username=None, password=None, token=None):
        if token is not None:
            if password is not None:
                raise TypeError(
                    "You cannot use both password and oauth token "
                    "authenication"
                )
            return 'Token %s' % token
        elif username is not None:
            if password is None:
                raise TypeError(
                    "You need a password to authenticate as " + username
                )
            self.username = username
            return self.hash_pass(password)

    def hash_pass(self, password):
        auth_str = ('%s:%s' % (self.username, password)).encode('utf-8')
        return 'Basic '.encode('utf-8') + base64.b64encode(auth_str).strip()


class GitHubClient(Client):
    def __init__(self, username=None, password=None, token=None,
                 connection_properties=None, paginate=False,
                 sleep_on_ratelimit=True):
        super(GitHubClient, self).__init__()
        self.paginate = paginate
        self.sleep_on_ratelimit = sleep_on_ratelimit

    def request(self, method, url, bodyData, headers):
        """Low-level networking. All HTTP-method methods call this"""

        headers = self._fix_headers(headers)
        url = self.prop.constructUrl(url)

        if bodyData is None:
            # Sending a content-type w/o the body might break some
            # servers. Maybe?
            if 'content-type' in headers:
                del headers['content-type']

        # TODO: Context manager
        requestBody = RequestBody(bodyData, headers)

        if self.sleep_on_ratelimit and self.no_ratelimit_remaining():
            self.sleep_until_more_ratelimit()

        while True:
            conn = self.get_connection()
            conn.request(method, url, requestBody.process(), headers)
            response = conn.getresponse()
            status = response.status
            content = ResponseBody(response)
            self.headers = response.getheaders()

            conn.close()
            if (status == 403 and self.sleep_on_ratelimit and
                    self.no_ratelimit_remaining()):
                self.sleep_until_more_ratelimit()
            else:
                data = content.processBody()
                if self.paginate and type(data) == list:
                    data.extend(
                        self.get_additional_pages(method, bodyData, headers))
                return status, data

    def get_additional_pages(self, method, bodyData, headers):
        data = []
        url = self.get_next_link_url()
        if not url:
            return data
        logger.debug(
            'Fetching an additional paginated GitHub response page at '
            '{}'.format(url))

        status, data = self.request(method, url, bodyData, headers)
        if type(data) == list:
            data.extend(self.get_additional_pages(method, bodyData, headers))
            return data
        elif (status == 403 and self.no_ratelimit_remaining()
              and not self.sleep_on_ratelimit):
            raise TypeError(
                'While fetching paginated GitHub response pages, the GitHub '
                'ratelimit was reached but sleep_on_ratelimit is disabled. '
                'Either enable sleep_on_ratelimit or disable paginate.')
        else:
            raise TypeError(
                'While fetching a paginated GitHub response page, a non-list '
                'was returned with status {}: {}'.format(status, data))

    def no_ratelimit_remaining(self):
        headers = dict(self.headers if self.headers is not None else [])
        ratelimit_remaining = int(
            headers.get('X-RateLimit-Remaining', 1))
        return ratelimit_remaining == 0

    def ratelimit_seconds_remaining(self):
        ratelimit_reset = int(dict(self.headers).get(
            'X-RateLimit-Reset', 0))
        return max(0, int(ratelimit_reset - time.time()) + 1)

    def sleep_until_more_ratelimit(self):
        logger.debug(
            'No GitHub ratelimit remaining. Sleeping for {} seconds until {} '
            'before trying API call again.'.format(
                self.ratelimit_seconds_remaining(),
                time.strftime(
                    "%H:%M:%S", time.localtime(
                        time.time() + self.ratelimit_seconds_remaining()))
            ))
        time.sleep(self.ratelimit_seconds_remaining())

    def get_next_link_url(self):
        """Given a set of HTTP headers find the RFC 5988 Link header field,
        determine if it contains a relation type indicating a next resource and
        if so return the URL of the next resource, otherwise return an empty
        string.

        From https://github.com/requests/requests/blob/master/requests/utils.py
        """
        for value in [x[1] for x in self.headers if x[0].lower() == 'link']:
            replace_chars = ' \'"'
            value = value.strip(replace_chars)
            if not value:
                return ''
            for val in re.split(', *<', value):
                try:
                    url, params = val.split(';', 1)
                except ValueError:
                    url, params = val, ''
                link = {'url': url.strip('<> \'"')}
                for param in params.split(';'):
                    try:
                        key, value = param.split('=')
                    except ValueError:
                        break
                    link[key.strip(replace_chars)] = value.strip(replace_chars)
                if link.get('rel') == 'next':
                    return link['url']
        return ''
