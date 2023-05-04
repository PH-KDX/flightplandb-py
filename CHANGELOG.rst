Changelog
--------------------

0.8.0
^^^^^^^^^^^^^^^^^^^^
This makes the entire library compatible with PEP-561, so that it can now be used with a static
type checker like mypy. The codebase has been reformatted with black and isort, and the tags
field of a PlanQuery now takes a list of strings, rather than a single string containing
the tags separated by commas and spaces. ``pdf`` is now the only return format which returns bytes;
``native`` returns a dataclass and all other formats return a UTF-8 string.

The changelog has also been updated to include the changes of version 0.5.0 and earlier.
A pre-commit file has been added to ensure all checks will pass before committing.


0.7.2
^^^^^^^^^^^^^^^^^^^^
This fixes a bug in the core API interface where HTTP headers were being passed into
requests as parameters.

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
Python 3.10 is now supported.

0.5.0
^^^^^^^^^^^^^^^^^^^^
This adds support for the OM, MM, and IM navaid types, fixing issue #14. ``include_route`` is
made into a function argument rather than a dataclass field, fixing issue #13. Parts of the
code are also refactored to use keyword arguments instead of positional arguments to help
reduce bugs.

0.4.1
^^^^^^^^^^^^^^^^^^^^
This documents the return format options for plan fetching, and differentiates between a
default ``native`` option where the returned json is unpacked into an appropriate dataclass
and a ``json`` option where it is returned as json.

0.4.0
^^^^^^^^^^^^^^^^^^^^
This adds a dark theme to the sphinx documentation. Exceeding of the API limit now raises
a dedicated TooManyRequestsException. Additionally, all ``Union[<type>, None]`` type hints have been
replaced by ``Optional[<type>]``

0.3.2
^^^^^^^^^^^^^^^^^^^^
This updates the documentation, and fixes some incorrect type hints.

0.3.1
^^^^^^^^^^^^^^^^^^^^
This splits the codebase up into separate submodules. Custom exception classes have been written to
handle different HTTP errors. Additionally, unit tests have been written, and Github workflows
have been added to run tests and lint the codebase on a push and upload to pip on a version release.

0.3.0
^^^^^^^^^^^^^^^^^^^^
This changes the wrapper file into an installable Python package, moves the documentation from the readme
to a Sphinx project on readthedocs, and adds docstrings for all functions. All data is now handled via
dataclasses. The project now uses semantic versioning.

0.2
^^^^^^^^^^^^^^^^^^^^
This adds functions for all remaining API endpoints which have not yet been wrapped. Error handling
has also been added, and the readme has been expanded.

0.1-alpha
^^^^^^^^^^^^^^^^^^^^
This is the initial, incomplete release of this wrapper. Many functions are not yet implemented, and
the wrapper is highly unstable.
