Quickstart
--------------------

This document assumes you have the library installed;
if not, check out the `Installation <introduction.html#installation>`_
section of the introduction.

Example
^^^^^^^^^^^^^^^^^^^^
This is a small example program which demonstrates basic usage of the library.
In this example, the only authenticated requests are those for which it is required.
In most cases, all requests would be authenticated, since authentication raises the
request limit from 100 to 2500.

.. code-block:: python

    import flightplandb as fpdb
    import asyncio

    # obviously, substitute your own token
    API_KEY = "VtF93tXp5IUZE307kPjijoGCUtBq4INmNTS4wlRG"

    async def main():
        # list all users named lemon
        async for user in fpdb.user.search(username="lemon"):
            print(user)

        # fetch most relevant user named lemon
        print(await fpdb.user.fetch(username="lemon"))

        # fetch first 20 of lemon's plans
        lemon_plans = fpdb.user.plans(username="lemon", limit=20)
        async for plan in lemon_plans:
            print(plan)

        # define a query to search for all plans
        query = fpdb.datatypes.PlanQuery(fromICAO="EHAM",
                                        toICAO="EGLL")
        # then search for the first three results of that query, sorted by distance
        # the route is included, which requires authentication
        resp = fpdb.plan.search(
            plan_query=query,
            include_route=True,
            sort="distance",
            limit=3,
            key=API_KEY
        )
        # and print each result in the response
        async for i in resp:
            print(i)

        # fetch the weather for Schiphol Airport
        print(await fpdb.weather.fetch("EHAM"))

        # then check remaining requests by subtracting the requests made from the total limit
        print((await fpdb.api.limit_cap())-(await fpdb.api.limit_used()))
    
    asyncio.run(main())

Try saving this program in a file in your project directory and running it.
Experiment around with different commands to get a feel for the library.

For specific commands, check out the :doc:`../api/main`.
