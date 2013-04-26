# The Agnostic Github API
"It doesn't know, and you don't care!"

`agithub` is a RESTful API for github.com with a transparent syntax that
allows rapid prototyping. It's code is very small, and easy to
change/update/fix.

For example:

```http
GET /issues/?filter=subscribed
```

becomes

```python
g.issues.get(filter='subscribed')
```

So, you can read https://developer.github.com/v3/, immediately
understand how to do it with `agithub`, and get on with your life.


## Sample App
```python
>>> from agithub import Github
>>> g = Github('user', 'pass')
>>> status, data = g.issues.get(filter='subscribed', foobar='llama')
>>> data
[ list, of, issues ]
>>> g.issues
<class 'agithub.github.RequestBuilder'>: I don't know about /issues
>>> g.repos.jpaugh64.repla.issues[1].get()
(200, { 'id': '#blah', ... })
>>> mylogin, myrepo = 'jpaugh64', 'braille-converter'
>>> g.repos[mylogin][myrepo].milestones.get(state='open', sort='completeness')
(200, [ list, of, milestones ])
>>> def following(client, user):
...   return client.user.following[user].get
...
>>> callback = following('octocat')
>>> if 204 == callback()[0]:
...   print 'You are following octocat'
You are following octocat
>>> g.funny.I.donna.remember.that.one.get()
(404, {'message': 'Not Found'})
```

### Demonstrates
- returns (status, body) tuple, where body is a Python object (JSON,
  remember?)
- Agnostic - It doesn't know what to do unless you tell it.
- parameter expansion, url-encoded for you
- how to use numbers (which can't be used as Python attribute names)
- string indicies - so you can have variable paths
- Make the API call later--reverse callbacks! :-p
- Error reporting: straight from Github

## Paths
That last example deserves some further explanation. At the moment,
agithub doesn't check that the path you specify is actually a valid
Github API call. (It also doesn't check whether the parameters are valid
for a given path.) What it does is to take the path, method, and
parameters that you specify and feed them up to Github, then read back
it's response. It's that simple.

In short, `agithub` doesn't know about the Github API. But it fully
supports it, so you don't care--usually. When you do care is when you
get an error. There are 2 kinds of errors you can get:

1. low-level http Exceptions (from `httplib`) Can Happen when, for example,
   you're not connected to the internet.  Catch these with `try..except`
blocks, as usual.

2. Github API errors (returned through http status) You'll need to check for
   these in the returned status, as you would anyway (i.e. some other way).
Often, the body contains more information on what went wrong.

## Pitfall

There's also a third, tricky situation you can run into from time to
time, which happens when you forget to append an http method to the
path, i.e. the last attribute. When this occurs, you receive a
RequestBuilder object, which doesn't do anything useful for you per se.
In this case, `agithub` tries to be as helpful as possible, by reminding
you that it doesn't know whenever you try to stringify it. (For example,
at the Python interactive prompt.)

This works out better if you don't forget the (), because then you get a
`TypeError: 'RequestBuilder' object is not callable`.

## Lies
- `agithub` is simpler than it needs to be. It doesn't handle certain
things very well, such when it receives a tarball instead of JSON. It
might also be nice if it gave you access to the mimetypes or other
headers.

- It doesn't support patch or delete.

- It isn't actively maintained. Bugfixes only, and even then I may be
  slow. However, I'm quite willing to pull any useful code you write.

- It doesn't support Python 3. This should be quite easy to fix. Likely
  only needs changing print statements, and how httplib is imported. If
  you fix this, send me a pull request.


## License
Copyright 2012 Jonathan Paugh
See [COPYING][1] for license details
[1]: https://github.com/jpaugh64/agithub/blob/master/COPYING
