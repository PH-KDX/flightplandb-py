Changelog
--------------------

0.7.1
^^^^^^^^^^^^^^^^^^^^
This is a minor update, which adds support for Python 3.11 and moves the package configuration
from setup.py to pyproject.toml. No breaking changes have been introduced. A bug has been fixed
which was causing aiohttp to crash on null parameters, and a bug in the quickstart example has
been fixed.

0.7.0
^^^^^^^^^^^^^^^^^^^^
This is another complete rewrite of the library, in which it is entirely converted to async.
This should mean faster execution of parallel requests, and no blocking when called from
another async library. Support for Python 3.7 has been dropped in this release. Python 3.11
is not yet supported as aiohttp does not yet support Python 3.11 at the time of release.

0.6.0
^^^^^^^^^^^^^^^^^^^^
This is a complete rewrite of the library, which moves functions out of classes.
This does have the side effect of requiring a key to be passed into every authenticated request,
instead of being passed into a class once on initialisation. The rewrite also incorporates
several small bugfixes, and changes the test environment from unittest to pytest.