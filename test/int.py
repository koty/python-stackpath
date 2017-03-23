#!/usr/bin/env python
import unittest
import time
import os

from stackpath import StackPath


class StackPathIntegration(unittest.TestCase):
    def setUp(self):
        self.alias = os.environ["ALIAS"]
        self.key = os.environ["KEY"]
        self.secret = os.environ["SECRET"]
        self.time = str(int(time.mktime(time.gmtime())))

        self.stackpath = StackPath(self.alias, self.key, self.secret)

    def test_get(self):
        for end_point in ["account",
                          "accountaddress",
                          "users",
                          "sites"]:
            if "/" in end_point:
                key = end_point.split("/")[1]
            else:
                key = end_point.replace(".json", "")

            rsp = self.stackpath.get(end_point)
            self.assertTrue(rsp["data"][key], "get " + key + " with data")

    def test_get_logs(self):
        rsp = self.stackpath.get("/logs")
        self.assertTrue(rsp["next_page_key"],
                        "get v3/reporting/logs.json with data")

    def test_post_and_delete(self):
        data = {"name": self.time, "url": "http://www.example.com/"}
        res = self.stackpath.post("/sites", data=data)
        zid = str(res["data"]["pullzone"]["id"])

        rsp = self.stackpath.delete("/sites/" + zid)
        self.assertTrue(zid, "post")
        self.assertEqual(200, rsp["code"], "delete")

    def test_put(self):
        street = self.time + "_put"
        rsp = self.stackpath.put("/account/address", {"street1": street})
        self.assertEqual(street, str(rsp["data"]["address"]["street1"]))

    def test_purge(self):
        rsp = self.stackpath.get("/sites")
        sites = rsp["data"]["pullzones"]
        site = sites[len(sites) - 1]["id"]

        rsp = self.stackpath.purge(site)
        self.assertEqual(200, rsp["code"])

        rsp = self.stackpath.get("/reports/popularfiles")
        popularfiles = rsp["data"]["popularfiles"]

        rsp = self.stackpath.purge(site, popularfiles[0]["uri"])
        self.assertEqual(200, rsp["code"])

        files = [popularfiles[0]["uri"], popularfiles[1]["uri"]]
        rsp = self.stackpath.purge(site, files)
        self.assertEqual(200, rsp["code"])

if __name__ == '__main__':
        unittest.main()
