.. currentmodule:: flightplandb

Introduction
--------------------

About
^^^^^^^^^^^^^^^^^^^^
This is a Python 3 wrapper for the `Flight Plan Database API <https://flightplandatabase.com/dev/api>`_.
Flight Plan Database is a website for creating and sharing flight plans for use in flight simulation.
For more information on Flight Plan Database, see their excellent `About page <https://flightplandatabase.com/about>`_.

Prerequisites
^^^^^^^^^^^^^^^^^^^^
FlightplanDB-py works with Python 3.7 or higher. Python 3.6 or
lower is not supported due to dataclasses, which were introduced with
`PEP 557 <https://www.python.org/dev/peps/pep-0557/>`_, being used in the library.

Installation
^^^^^^^^^^^^^^^^^^^^
The easiest way to install the library is from PyPi, by running

.. code-block:: console

  $ pip install flightplandb

Or, if you prefer, install the directly from the GitHub repo:

.. code-block:: console

  $ pip install https://github.com/PH-KDX/flightplandb-py/archive/main.zip

after which the package and its dependencies are installed.

If you've never used ``pip`` before, check out `this useful overview <https://realpython.com/what-is-pip/>`_.

Virtual Environments
""""""""""""""""""""
It is, of course, possible to install the library in a virtual environment.
Start by going to
your project's working directory.
Create a virtual environment called, for example, ``foo`` as follows:

.. code-block:: bash

  $ python3 -m venv foo

then when you want to use it, activate it on Linux or macOS with

.. code-block:: bash

  $ source foo/activate/bin

or on Windows with

.. code-block:: dosbatch

  $ foo\Scripts\activate.bat

after which you can install the library as described in `Installation <#installation>`_.


Testing
^^^^^^^^^^^^^^^^^^^^
To test if the package has correctly installed, open a Python shell
(note: if you're using a virtual environment, make sure you activate it first) and run

.. code-block:: python3

   import flightplandb
   flightplandb.api.ping()

which should return
``StatusResponse(message='OK', errors=None)``
if all has gone well.


Request Limits
^^^^^^^^^^^^^^^^^^^^
API requests are rate limited on a 24 hour rolling basis to ensure fair access to all users.
If you reach your daily limit, a
:class:`~flightplandb.exceptions.TooManyRequestsException()` will be raised on
your requests. To check your limit and used requests, look at the output of
:meth:`flightplandb.api.limit_cap()` and
:meth:`flightplandb.api.limit_used()` respectively.
These calls, together with :meth:`flightplandb.api.ping()`, will not increment your request counter.

The limit for unauthenticated users is IP-based, and is currently set to 100.
The limit for authenticated users is key-based, and is currently set to 2500.


Authentication
^^^^^^^^^^^^^^^^^^^^
Whilst many parts of the API are publicly accessible, some endpoints require
authentication with an API access key, which is an alphanumeric string such as
``VtF93tXp5IUZE307kPjijoGCUtBq4INmNTS4wlRG``. If provided, this key must be
passed into every authenticated request, using the ``key`` argument.

To get an API key, visit your Flight Plan Database
`account settings <https://flightplandatabase.com/settings>`_ page.
Your account will need a verified email address to add an API key.

Endpoints that require authentication are marked as such in the API docs. Failing to
provide valid authentication credentials on these endpoints will result in an
:class:`~flightplandb.exceptions.UnauthorizedException()` being raised. You are responsible
for maintaining the security of your private API key, which gives near full access to
your Flight Plan Database account. If your key is exposed, please use
:meth:`flightplandb.api.revoke()` to revoke your key manually.
