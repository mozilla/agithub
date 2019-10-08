# The Agnostic GitHub API

> It doesn't know, and you don't care!

`agithub` is a REST API client with transparent syntax which facilitates
rapid prototyping &mdash; on *any* REST API!

Originally tailored to the GitHub REST API, AGitHub has grown up to
support many other REST APIs:

* DigitalOcean
* Facebook
* GitHub
* OpenWeatherMap
* SalesForce

Additionally, you can add *full support* for another REST API with very
little new code!  To see how, check out the [Facebook client], which has
about 30 lines of code.

This works because AGithub knows everything it needs to about protocol
(REST, HTTP, TCP), but assumes nothing about your upstream API.

[Facebook client]: agithub/Facebook.py

# Use

The most striking quality of AGitHub is how closely its syntax emulates
HTTP. In fact, you might find it even more convenient than HTTP, and
almost as general (as far as REST APIs go, anyway). The examples below
tend to use the GitHub API as a reference point, but it is no less easy to
use `agithub` with, say, the Facebook Graph.

## Create a client

```python
from agithub.GitHub import GitHub
client = GitHub()
```

## GET

Here's how to do a `GET` request, with properly-encoded url parameters:

```python
client.issues.get(filter='subscribed')
```

That is equivalent to the following:

```http
GET /issues/?filter=subscribed
```

## POST

Here's how to send a request body along with your request:

```python
some_object = {'foo': 'bar'}
client.video.upload.post(body=some_object, tags="social devcon")
```

This will send the following request, with `some_object` serialized as
the request body:<sup>*</sup>

```http
POST /video/upload?tags=social+devcon

{"foo": "bar"}
```

The `body` parameter is reserved and is used to define the request body to be
POSTed. `tags` is an example query parameter, showing that you can pass both
an object to send as the request body as well as query parameters.

<sup>*</sup> For now, the request body is limited to JSON data; but
we plan to add support for other types as well

## Parameters

### `headers`

Pass custom http headers in your ruquest with the reserved parameter `headers`.

```python
from agithub.GitHub import GitHub
g = GitHub()
headers = {'Accept': 'application/vnd.github.symmetra-preview+json'}
status, data = g.search.labels.get(headers=headers, repository_id=401025, q='¯\_(ツ)_/¯')
print(data['items'][0])
```

```text
{u'default': False, u'name': u'\xaf\\_(\u30c4)_/\xaf', u'url': u'https://api.github.com/repos/github/hub/labels/%C2%AF%5C_(%E3%83%84)_/%C2%AF', u'color': u'008672', u'node_id': u'MDU6TGFiZWwxMTcwNjYzNTM=', u'score': 43.937515, u'id': 117066353, u'description': u''}

```

### `body`

If you're using `POST`, `PUT`, or `PATCH` (`post()`, `put()`, or `patch()`), 
then you should include the body as the `body=` argument. The body is 
serialized to JSON before sending it out on the wire.

```python
from agithub.GitHub import GitHub
g = GitHub()
# This Content-Type header is only required in this example due to a GitHub 
# requirement for this specific markdown.raw API endpoint
headers={'Content-Type': 'text/plain'}  
body = '# This should be my header'
status, data = g.markdown.raw.post(body=body, headers=headers)
print(data)
```

```text
<h1>
<a id="user-content-this-should-be-my-header" class="anchor" href="#this-should-be-my-header" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>This should be my header</h1>

```



## Example App

1. First, instantiate a `GitHub` object.

   ```python
   from agithub.GitHub import GitHub
   g = GitHub()
   ```

2. When you make a request, the status and response body are passed back
   as a tuple.

   ```python
   status, data = g.users.octocat.get()
   print(data['name'])
   print(status)
   ```

   ```text
   The Octocat
   200
   ```

3. If you forget the request method, `agithub` will complain that you
   haven't provided enough information to complete the request.

   ```python
   g.users
   ```
   
   ```text
   <class 'agithub.github.IncompleteRequest'>: /users
   ```

4. Sometimes, it is inconvenient (or impossible) to refer to a URL as a
   chain of attributes, so indexing syntax is provided as well. It
   behaves exactly the same. In these examples we use indexing syntax because 
   you can't have a python function name

   * starting with a digit : `1`
   * containing a dash (`-`) character : `Spoon-Knife`

   ```python
   g.repos.github.hub.issues[1].get()
   g.repos.octocat['Spoon-Knife'].branches.get()
    ```

    ```text
   (200, { 'id': '#blah', ... })
   (200, [ list, of, branches ])

    ```

5. You can also pass query parameter to the API as function parameters to the
   method function (e.g. `get`).

   ```python
   status, data = g.repos.octocat['Spoon-Knife'].issues.get(
       state='all', creator='octocat')
   print(data[0].keys())
   print(status)
   ```

   ```text
   [u'labels', u'number', … , u'assignees']
   200
   ```

   Notice the syntax here:
   `<API-object>.<URL-path>.<request-method>(<query-parameters>)`
   
   * `API-object` : `g`
   * `URL-path` : `repos.octocat['Spoon-Knife'].issues`
   * `request-method` : `get`
   * `query-parameters` : `state='all', creator='octocat'`

6. As a weird quirk of the implementation, you may build a partial call
   to the upstream API, and use it later.

   ```python
   def following(self, user):
       return self.user.following[user].get
   
   myCall = following(g, 'octocat')
   if 204 == myCall()[0]:
       print 'You are following octocat'
   ```
   
   ```text
   You are following octocat
   ```

   You may find this useful &mdash; or not.

7. Finally, `agithub` knows nothing at all about the GitHub API, and it
   won't second-guess you.

   ```python
   g.funny.I.donna.remember.that.one.head()
   ```
   
   ```text
   (404, {'message': 'Not Found'})
   ```

   The error message you get is directly from GitHub's API. This gives
   you all of the information you need to survey the situation.

7. If you need more information, the response headers of the previous
   request are available via the `getheaders()` method.

   ```python
   g.getheaders()
   ```
   
   ```text
   [('status', '404 Not Found'),
    ('x-ratelimit-remaining', '54'),
    …
    ('server', 'GitHub.com')]
   ```
   
   Note that the headers are standardized to all lower case. So though, in this
   example, GitHub returns a header of `X-RateLimit-Remaining` the header is
   returned from `getheaders` as `x-ratelimit-remaining`

## Error handling
Errors are handled in the most transparent way possible: they are passed
on to you for further scrutiny. There are two kinds of errors that can
crop up:

1. Networking Exceptions (from the `http` library). Catch these with
   `try .. catch` blocks, as you otherwise would.

2. GitHub API errors. These mean you're doing something wrong with the
   API, and they are always evident in the response's status. The API
   considerately returns a helpful error message in the JSON body.

## Specific REST APIs

`agithub` includes a handful of implementations for specific REST APIs. The
example above uses the GitHub API but only for demonstration purposes. It
doesn't include any GitHub specific functionality (for example, authentication).

Here is a summary of additional functionality available for each distinct REST
API with support included in `agithub`. Keep in mind, `agithub` is designed
to be extended to any REST API and these are just an initial collection of APIs.

### GitHub : [`agithub/GitHub.py`](agithub/GitHub.py)

#### GitHub Authentication

To initiate an authenticated `GitHub` object, pass it your username and password
or a [token](https://github.com/settings/tokens).

```python
from agithub.GitHub import GitHub
g = GitHub('user', 'pass')
```

```python
from agithub.GitHub import GitHub
g = GitHub(token='token')
```

#### GitHub Pagination

When calling the GitHub API with a query that returns many results, GitHub will
[paginate](https://developer.github.com/v3/#pagination) the response, requiring
you to request each page of results with separate API calls. If you'd like to
automatically fetch all pages, you can enable pagination in the `GitHub` object
by setting `paginate` to `True`.

```python
from agithub.GitHub import GitHub
g = GitHub(paginate=True)
status, data = g.repos.octocat['Spoon-Knife'].issues.get()

status, data = g.users.octocat.repos.get(per_page=1)
print(len(data))
```

```text
8
```

(added in v2.2.0)

#### GitHub Rate Limiting

By default, if GitHub returns a response indicating that a request was refused
due to [rate limiting](https://developer.github.com/v3/#rate-limiting), agithub
will wait until the point in time when the rate limit is lifted and attempt
the call again.

If you'd like to disable this behavior and instead just return the error
response from GitHub set `sleep_on_ratelimit` to `False`.

```python
from agithub.GitHub import GitHub
g = GitHub(sleep_on_ratelimit=False)
status, data = g.repos.octocat['Spoon-Knife'].issues.get()
print(status)
print(data['message'])
```

```text
403
API rate limit exceeded for 203.0.113.2. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)
```

(added in v2.2.0)

#### GitHub Logging

To see log messages related to GitHub specific features like pagination and
rate limiting, you can use a root logger from the Python logging module.

```python
import logging
logging.basicConfig()
logger = logging.getLogger()  # The root logger
logger.setLevel(logging.DEBUG)
from agithub.GitHub import GitHub
g = GitHub(paginate=True)
status, data = g.repos.octocat['Spoon-Knife'].issues.get()
```

```text
DEBUG:agithub.GitHub:No GitHub ratelimit remaining. Sleeping for 676 seconds until 14:22:43 before trying API call again.
DEBUG:agithub.GitHub:Fetching an additional paginated GitHub response page at https://api.github.com/repositories/1300192/issues?page=2
DEBUG:agithub.GitHub:Fetching an additional paginated GitHub response page at https://api.github.com/repositories/1300192/issues?page=3
…
```

## Semantics

Here's how `agithub` works, under the hood:

1. It translates a sequence of attribute look-ups into a URL; The
   Python method you call at the end of the chain determines the
   HTTP method to use for the request.
2. The Python method also receives `name=value` arguments, which it
   interprets as follows:
   * `headers=`
     * You can include custom headers as a dictionary supplied to the
     `headers=` argument. Some headers are provided by default (such as
     User-Agent). If these occur in the supplied dictionary, the default
     value will be overridden.
 
       ```python
       headers = {'Accept': 'application/vnd.github.loki-preview+json'}
       ```
   * `body=`
     * If you're using `POST`, `PUT`, or `PATCH` (`post()`, `put()`, and
     `patch()`), then you should include the body as the `body=` argument.
     The body is serialized to JSON before sending it out on the wire.
   * GET Parameters
     * Any other arguments to the Python method become GET parameters, and are
     tacked onto the end of the URL. They are, of course, url-encoded for
     you.
3. When the response is received, `agithub` looks at its content
   type to determine how to handle it, possibly decoding it from the
   given char-set to Python's Unicode representation, then converting to
   an appropriate form, then passed to you along with the response
   status code. (A JSON object is de-serialized into a Python object.)

## Extensibility
`agithub` has been written in an extensible way. You can easily:

* Add new HTTP methods by extending the `Client` class with
  new Python methods of the same name (and adding them to the
  [`http_methods` list][1]).

* Add new default headers to the [`_default_headers` dictionary][2].
  Just make sure that the header names are lower case.

* Add a new media-type (a.k.a. content-type a.k.a mime-type) by
  inserting a new method into the [`ResponseBody` class][3], replacing
  `'-'` and `'/'` with `'_'` in the method name. That method will then be
  responsible for converting the response body to a usable
  form &mdash; and for calling `decode_body` to do char-set
  conversion, if required. For example to create a handler for the content-type
  `application/xml` you'd extend `ResponseBody` and create a new method like this
  
  ```python
  import xml.etree.ElementTree as ET

  class CustomResponseBody(ResponseBody):
      def __init__(self):
          super(ChildB, self).__init__()
      
      def application_xml(self):
          # Handles Content-Type of "application/xml"
          return ET.fromstring(self.body)
  ```

And if all else fails, you can strap in, and take 15 minutes to read and
become an expert on the code. From there, anything's possible.

[1]: https://github.com/mozilla/agithub/blob/b47661df9e62224a69216a2f11dbe574990349d2/agithub/base.py#L103-L110
[2]: https://github.com/mozilla/agithub/blob/b47661df9e62224a69216a2f11dbe574990349d2/agithub/base.py#L22-L28
[3]: https://github.com/mozilla/agithub/blob/b47661df9e62224a69216a2f11dbe574990349d2/agithub/base.py#L309-L332

## License
Copyright 2012&ndash;2016 Jonathan Paugh and contributors
See [COPYING](COPYING) for license details
