About this Document
===================

This serves as both the change-log and TODO list for the project. It
serves to clarify what is in an (anticipated) release, as well as to
direct project momentum. If you find something in here you want to do,
by all means, please do.

At the top, you will see project milestones (upcoming releases) and
their associated TODOs. After that, you will see a release version
history in reverse chronological order. (The latest release comes
[first](#release).)

Also note that the latest stable branch (the tip of
[maint][https://github.com/mozilla/agithub/tree/maint]) is usually in
an as-yet *unreleased* status. This avoids a proliferation of
single-commit patch-level version changes in the `maint` branch, whilst
still providing access to the very latest bug-fixes


Upcoming
========

Unscheduled
-----------

* Create a script to pack the basic module and any given set of
  service-specific classes as one file. I still like the idea that a
  given API (e.g. Facebook) could be packed into a single file, and
  dropped into another project as a unit.

* Actually support OAuth

* Use a real, venerable test framework&nbsp;&mdash; maybe unittest

* Support Request/Response compression. Here's a great [tutorial][sftut]

* Get total coverage in the test suite, with the possible exception of
  actually sending a request across the wire

* Support reusing TCP connections, and "pipelining" of requests, a la
  RFC 2068, Sect 8.1, L2377

    - The user must ask for pipelining, and supply a callback function
      to be called after a response is received.
    - Rename Client.request() -> Client.addRequest() (or such)
    - Have Client.addRequest() check whether a persistent connection is
      wanted, and save the entire request in a Client.pendingRequests
      list in that case
    - Create a new Client.sendRequests() method which the user may call
      to send all requests up the pipeline. (It should work even if the
      server does not support pipelining)
    - Call the user-supplied callback whenever a request is received.
      There are some concurrency issues here, and we may elect to call
      the callback only after *all* requests are received.

[sftut]: http://www.salesforce.com/us/developer/docs/api_rest/index_Left.htm#CSHID=intro_rest_compression.htm|StartTopic=Content%2Fintro_rest_compression.htm|SkinName=webhelp

v3.0
----
* Unbreak the test suite
* Be consistently `camelCase` (Exception: the media-type converters in
  Content (e.g.  `application_json`) should stay the same.)

Release
=======

v2.1
----
* Support XML de-serialization. (pick from [next-xml])
* Request body content-type serialization & charset encoding

[next-xml]: 3d373435c8110612cad061e9a9b31a7a1abd752c

v2.0
----
* Features:
    - Setup.py, for easy installation (Marcos Hernández)
    - Legit Python package
    - `url_prefix`: Ability to add an always-on prefix to the url for an API
* Bugfixes:
    - Use `application/octet-stream` for unknown media type
    - Spell 'GitHub' correctly

v1.3
----
A stable branch, with a lot of bug fixes! (Thanks to all who
contributed!)

* Feature: Unit tests (Uriel Corfa, Joachim Durchholz)
* Grown-up Incomplete-request error message (Joachim Durchholz)
* bug: PATCH method (ala)
* bug: Allow using auth tokens without a username (Uriel Corfa)
* bug: Set content-type to JSON when sending a JSON request
  (Jens Timmerman)

v1.2
----

* Revamp the internals, adding extensibility and flexibility. Meanwhile,
  the external API (i.e. via the GitHub class) is entirely unchanged

* New test-suite. It is ad-hoc and primitive, but effective

* Generic support for other REST web services

    - New top-level class (API)
    - GitHub is now a subclass of the API class, and is the model for
      creating new subclasses
    - Facebook and SalesForce subclasses created, allowing (basic)
      access to these web services

v1.1
----

* Includes the version in the user-agent string

v1.0
----

* Has a version number. (Yippie!)
* First more-or-less stable version
