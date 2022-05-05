Quickstart
--------------------

This assumes you have the library installed;
if not, check out the `Installation <introduction.html#installation>`_
section of the introduction.

Example
^^^^^^^^^^^^^^^^^^^^
This is a small example program which demonstrates basic usage of the library.

.. code-block:: python

  import flightplandb as fpdb

  # obviously, substitute your own token
  api = fpdb.FlightPlanDB("VtF93tXp5IUZE307kPjijoGCUtBq4INmNTS4wlRG")

  # list all users named lemon
  for user in api.user.search("lemon"):
      print(user)

  # fetch most relevant user named lemon
  print(api.user.fetch("lemon"))

  # fetch first 20 of lemon's plans
  lemon_plans = api.user.plans(username="lemon", limit=20)
  for plan in lemon_plans:
      print(plan)

  # define a query to search for all plans
  query = fpdb.datatypes.PlanQuery(fromICAO="EHAM",
                                   toICAO="EGLL")
  # then search for the first three results of that query, sorted by distance
  resp = api.plan.search(query, limit=3, sort="distance")
  # and print each result in the response
  for i in resp:
      print(i)

  # fetch the weather for Schiphol Airport
  print(api.weather.fetch("EHAM"))

  # then check remaining requests by subtracting the requests made from the total limit
  print(api.limit_cap-api.limit_used)

Try saving it in a file called ``test.py`` in your project directory and running it.
Experiment around with different commands to get a feel for the library.

For specific commands, check out the :doc:`../api/main`.
