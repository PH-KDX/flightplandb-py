Changelog
--------------------

0.7.0
^^^^^^^^^^^^^^^^^^^^
This is another complete rewrite of the library, in which it is entirely converted to async.
This should mean faster execution of parallel requests, and no blocking when called from
another async library. Support for Python 3.7 has been dropped in this release.

0.6.0
^^^^^^^^^^^^^^^^^^^^
This is a complete rewrite of the library, which moves functions out of classes.
This does have the side effect of requiring a key to be passed into every authenticated request,
instead of being passed into a class once on initialisation. The rewrite also incorporates
several small bugfixes, and changes the test environment from unittest to pytest.