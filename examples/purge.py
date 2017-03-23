#!/usr/bin/env python
import pprint as pp
from os import environ as env
from sys import exit, argv
from textwrap import dedent
from stackpath import StackPath

try:
    site_id = argv[1]
except:
    site_id = None

if not "ALIAS" in env or not "KEY" in env or not "SECRET" in env:
    print(dedent("""\
        Usage: purge.py site_id

          Add credentials to your environment like so:

          $ export ALIAS=<alias>
          $ export KEY=<key>
          $ export SECRET=<secret>
        """))
    exit(1)


stackpath = StackPath(env["ALIAS"], env["KEY"], env["SECRET"])

if site_id is None:
    sites = stackpath.get("/sites")
    for site in sites["data"]["zones"]:
        print("Purging zone: %s (%s)" % (
            site["name"], site["id"]))

        pp.pprint(stackpath.purge(site["id"]))
else:
    print("Purging zone: %s" % site_id)
    res = stackpath.purge(site_id)
    try:
        if res["code"] == 200:
            print("SUCCESS!")
        else:
            print("Failed with code: " + res["code"])
            exit(res["code"])
    except KeyError:
        print("Something went terribly wrong!")
        pp.pprint(res)
        exit(1)
