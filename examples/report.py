#!/usr/bin/env python
import pprint as pp
from sys import argv
from textwrap import dedent
from os import environ as env
from stackpath   import StackPath

try:
    report = "/" + argv[1]
except:
    report = ""


if not "ALIAS" in env or not "KEY" in env or not "SECRET" in env:
    print(dedent("""\
        Usage: report.py [monthly|daily|hourly]

          Add credentials to your environment like so:

          $ export ALIAS=<alias>
          $ export KEY=<key>
          $ export SECRET=<secret>
        """))
    exit(1)


stackpath = StackPath(env["ALIAS"], env["KEY"], env["SECRET"])

sites = stackpath.get("/sites")
for site in sites["data"]["zones"]:
    print("Zone report for: %s (%s)" % (
        site["name"], site["tmp_url"]))

    # summary
    fetch = stackpath.get("/reports/%s/stats%s" % (site["id"], report))
    for key, val in fetch["data"]["summary"].items():
        print(" - %s: %s" % (key, val))

    # popularfiles
    print(" ")
    print("Popular Files:")

    fetch = stackpath.get("/reports/%s/popularfiles?size=10" % (site["id"]))
    for file in fetch["data"]["popularfiles"]:
        print(" - url: " + file["uri"])
        print("   - hits: " + file["hit"])
        print("   - size: " + file["size"])

    print(" ")

