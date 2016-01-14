About this Document
===================

This serves as both the change-log and TODO list for the project. It
serves to clarify what is in an (anticipated) release, as well as to
direct project momentum. If you find something in here you want to do,
by all means, please do. 

At the top, you willll see project milestones (upcoming releases) and
their associated TODOs. After that, you will see a release version
history in reverse chronological order. (The latest release comes
[first](#release).)

Also note that the latest stable branch (the tip of [maint][maint]) is
usually in an as-yet *unreleased* status. This avoids a proliferation of
single-commit patch-level version changes in the `maint` branch, whilst
still providing access to the very latest bug-fixes


Upcoming
========

Unscheduled
-----------

* Support encoding/serialization request bodies, analogous to the
  decoding/de-serialization for response bodies which is done in the
  ResponseBody class

    - This probably means reorganizing the ResponseBody class, perhaps
      adding another level of structure
    - Find a convenient way for the user to specify request-body
      content-type. Maybe add a `content_type=` parameter to `put()` et
      al?

    - Does GitHub support this? It should. And if so, we should use it
      by default

* Create a script to pack the basic module and any given set of
  service-specific classes as one file

    - Separate GitHub class into a separate module

* Rename the project, and migrate it to a new project url. At the same
  time, the original [link][link] should point to a stripped down
  version that

    a) Works perfectly for GitHub's API, unchanged

    b) Mentions the new project in the README

    c) Is updated jointly (at release milestones) by uploading the
    result of `pack-script GitHub` (The `pack-script` is described above.)

  #### Motivation
  The [project][link] is referenced from GitHub's official list of API
  clients. Ergo, anything not pertaining to GitHub's API doesn't really
  belong at that URL&nbsp;&mdash; it's distracting. Users should be made
  aware of the generic version without being forced to migrate.

  Besides, the updates could easily be automated via a post-push hook
  that walks the `master`/`maint` history in the main project; and
  thereby be supported indefinitely without fuss

[link]: https://github.com/jpaugh/agithub

* Actually support OAuth

* TODO: Use a real, venerable test framework&nbsp;&mdash; maybe unittest

* Support Request/Response compression. Here's a great [tutorial][sftut]

[sftut]: http://www.salesforce.com/us/developer/docs/api_rest/index_Left.htm#CSHID=intro_rest_compression.htm|StartTopic=Content%2Fintro_rest_compression.htm|SkinName=webhelp


v2.0
----

* Refactor code-base

    - In particular, we need to spell "GitHub" correctly:
        `Github` -> `GitHub`
    - Convert most identifiers from `under_scores` to `camelCase` (An
      exception will be the media-type converters in Content (e.g.
      application_json))
    - Fix anything else that makes me squeamish

* Support XML de-serialization. Python has (I think) built-in support
  for this

Release
=======

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
  the external API (i.e. via the Github class) is entirely unchanged

* New test-suite. It is ad-hoc and primitive, but effective

* Generic support for other REST web services

    - New top-level class (API)
    - Github is now a subclass of the API class, and is the model for
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
