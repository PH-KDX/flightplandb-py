Changelog
--------------------

0.6.0
^^^^^^^^^^^^^^^^^^^^
This is a complete rewrite of the library, which moves functions out of classes.
This does have the side effect of requiring a key to be passed into every authenticated request,
instead of being passed into a class once on initialisation. The rewrite also incorporates
several small bugfixes, and changes the test environment from unittest to pytest.