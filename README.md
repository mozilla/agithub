# The Agnostic GitHub API
*It doesn't know, and you don't care!*

`agithub` is a REST API client with transparent syntax which facilitates
rapid prototyping&nbsp;&mdash; on *any* REST API!

Originally tailored to the GitHub REST API, AGitHub has grown up to
support many other REST APIs:

* DigitalOcean
* Facebook
* GitHub
* OpenWeatherMap
* SalesForce

Additionally, you can add *full support* for another REST API with very
little new code! To see how, check out the [GitHub client], which has
about 30 lines of code.

[GitHub client]: https://github.com/jpaugh/agithub/blob/master/agithub/GitHub.py

# Use

The most striking quality of AGitHub is how closely its syntax emulates
HTTP. In fact, you might find it even more convenient that HTTP, and
almost as general (as far as REST APIs go, anyway).

To put in another way, `agithub` knows everything it needs to about
protocol (REST, HTTP, TCP), but assumes nothing about your upstream API.
The examples below tend to use the GitHub API as a refence point, but it
is no less easy to use `agithub` with, say, the Facebook Graph.

## Get

Here's how to do a `GET` request, with proprely-encoded url parameters:

```python
client.issues.get(filter='subscribed')
```

That is equivalent to the following:

```http
GET /issues/?filter=subscribed
```

## Post

Here's how to send a request body along with your request:

```python
client.video.upload.post(body=someObject, tags="social devcon")
```

This will send the following request, with `someObject` serialized as
the request body:<sup>*</sup>

```http
POST /video/upload?tags=social+devcon

<serialized request body>
```

<sup>*</sup>&nbsp;For now, the request body is limited to JSON data; but
we plan to add support for other types as well


## Example App

1. First, instantiate a `GitHub` object, passing it your username and
   password or a token if an authenticated session is desired.

   ```python
   >>> from agithub.GitHub import GitHub
   >>> g = GitHub('user', 'pass')
   ```

   ```python
   >>> from agithub import GitHub
   >>> g = GitHub(token='token')
   ```

2. When you make a request, the status and response body are passed back
   as a tuple.

   ```python
   >>> status, data = g.issues.get(filter='subscribed', foobar='llama')
   >>> data
   [ list, of, issues ]
   ```

   Notice the syntax here:
   `<API-object>.<URL-path>.<request-method>(<GET-parameters>)`

3. If you forget the request method, `agithub` will complain that you
   haven't provided enough information to complete the request.

   ```python
   >>> g.issues
   <class 'agithub.github.IncompleteRequest'>: /issues
   ```

4. Sometimes, it is inconvenient (or impossible) to refer to a URL as a
   chain of attributes, so indexing syntax is provided as well. It
   behaves exactly the same.

   ```python
   >>> g.repos.jpaugh.repla.issues[1].get()
   (200, { 'id': '#blah', ... })
   >>> mylogin, myrepo = 'jpaugh', 'braille-converter'
   >>> g.repos[mylogin][myrepo].milestones.get(state='open', sort='completeness')
   (200, [ list, of, milestones ])
   ```

5. As a weird quirk of the implementation, you may build a partial call
   to the upstream API, and use it later.

   ```python
   >>> def following(self, user):
   ...   return self.user.following[user].get
   ...
   >>> myCall = following(g, 'octocat')
   >>> if 204 == myCall()[0]:
   ...   print 'You are following octocat'
   You are following octocat
   ```

   You may find this useful&nbsp;&mdash; or not.

6. Finally, `agithub` knows nothing at all about the GitHub API, and it
   won't second-guess you.

   ```python
   >>> g.funny.I.donna.remember.that.one.head()
   (404, {'message': 'Not Found'})
   ```

   The error message you get is directly from GitHub's API. This gives
   you all of the information you need to survey the situation.

7. If you need more information, the response headers of the previous
   request are available via the `getheaders()` method.

   ```python
   >>> g.getheaders()
   [('status', '404 Not Found'),
    ('x-ratelimit-remaining', '54'),
    ...
    ('server', 'GitHub.com')]
   ```

## Error handling
Errors are handled in the most transparent way possible: they are passed
on to you for further scrutiny. There are two kinds of errors that can
crop up:

1. Networking Exceptions (from the `http` library). Catch these with
   `try .. catch` blocks, as you otherwise would.

2. GitHub API errors. These means you're doing something wrong with the
   API, and they are always evident in the response's status. The API
   considerately returns a helpful error message in the JSON body.


## Semantics
Here's how `agithub` works, under the hood:

1. It translates a sequence of attribute look-ups into a URL; The
   Python method you call at the end of the chain determines the
   HTTP method to use for the request.

2. The Python method also receives `name=value` arguments, which it
   interprets as follows:

##### `header=`

You can include custom headers as a dictionary supplied to the
`headers=` argument. Some headers are provided by default (such as
User-Agent). If these occur in the supplied dictionary, the default
value will be overridden.


##### `body=`

If you're using `POST`, `PUT`, or `PATCH` (`post()`, `put()`, and
`patch()`), then you should include the body as the `body=` argument.
The body is serialized to JSON before sending it out on the wire.

##### GET Parameters

Any other arguments to the Python method become GET parameters, and are
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
  `'-'` and `'/'` with `'_'` in the name. That method will then be
  responsible for converting the response body to a usable
  form&nbsp;&mdash; and for calling `decode_body` to do char-set
  conversion, if required.

And if all else fails, you can strap in, and take 15 minutes to read and
become an expert on the code. From there, anything's possible.

[1]: https://github.com/jpaugh/agithub/blob/master/agithub.py#L105
[2]: https://github.com/jpaugh/agithub/blob/master/agithub.py#L24
[3]: https://github.com/jpaugh/agithub/blob/master/agithub.py#L255

## License
Copyright 2012&ndash;2016 Jonathan Paugh and contributors
See [COPYING][LIC] for license details
[LIC]: https://github.com/jpaugh/agithub/blob/master/COPYING
