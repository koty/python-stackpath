#!/usr/bin/env python
import pprint as pp
from os import environ as env
from stackpath  import StackPath
from textwrap import dedent

if not "ALIAS" in env or not "KEY" in env or not "SECRET" in env:
    print(dedent("""\
        Usage: simple.py

          Add credentials to your environment like so:

          $ export ALIAS=<alias>
          $ export KEY=<key>
          $ export SECRET=<secret>
    """))
    exit(1)

maxcdn = StackPath(env["ALIAS"], env["KEY"], env["SECRET"])

print("GET '/account'")
pp.pprint(maxcdn.get("/account"))

print("GET '/account.json/address'")
pp.pprint(maxcdn.get("/account/address"))

print("GET '/reports/stats/hourly'")
pp.pprint(maxcdn.get("/reports/stats/hourly"))
