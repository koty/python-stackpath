import mock
import unittest
import requests
from stackpath import StackPath

###############################################################################
# Mock as needed.


def mock_request(method, url, *args, **kwargs):
    pass


class Response(object):
    def __init__(self, method, code=200, data={"foo": "bar"}):
        self._json = {"code": code, "method": method, "data": data}
        self.status_code = code
        self.reason = "Success"
        self.headers = ""
        self.url = "http://www.example.com/foo/bar"

    def json(self):
        return self._json


class ErrorResponse(object):
    def __init__(self, code=200, badcontent="Some bad content."):
        self._content = badcontent
        self.status_code = code
        self.reason = "Error Response"
        self.headers = ""
        self.url = "http://www.example.com/foo/bar"

    def json(self):
        raise ValueError("No JSON object could be decoded")


def response(method, **kwargs):
    return Response(method, **kwargs)


def error_response(**kwargs):
    return ErrorResponse(**kwargs)

#
###############################################################################


class StackPathCDNTests(unittest.TestCase):

    def setUp(self):
        self.alias = "test_alias"
        self.key = "test_key"
        self.secret = "test_secret"
        self.server = "rws.example.com"
        self.stackpath = StackPath(self.alias, self.key,
                                   self.secret, server=self.server)

    def test_init(self):
        self.assertTrue(self.stackpath)
        self.assertEqual(self.stackpath.url,
                         "https://rws.example.com/v1/test_alias")

    def test_get_url(self):
        self.assertEqual(self.stackpath._get_url("/foo"),
                         "https://rws.example.com/v1/test_alias/foo")

    def test_data_request(self):
        for meth in ["post", "put", "delete"]:
            requests.Session.request = mock.create_autospec(mock_request,
                                                            return_value=response(meth))

            data = {"foo": "bar"}
            rsp = self.stackpath._data_request(meth, meth + ".json", data=data)
            expected = {"code": 200, "method": meth, "data": {"foo": "bar"}}
            self.assertEqual(rsp, expected)

            requests.Session.request = mock.create_autospec(mock_request,
                                                            return_value=error_response())
        with self.assertRaises(StackPath.ServerError):
            self.stackpath._data_request(meth, meth + ".json", data={"foo": "bar"})

    def test_get(self):
        requests.Session.request = mock.create_autospec(mock_request,
                                                        return_value=response("get"))

        expected = {"code": 200, "method": "get", "data": {"foo": "bar"}}
        self.assertEqual(self.stackpath.get("/get"), expected)

        requests.Session.request = mock.create_autospec(mock_request,
                                                        return_value=error_response())
        with self.assertRaises(StackPath.ServerError):
            self.stackpath.get("/get")

    def test_post(self):
        requests.Session.request = mock.create_autospec(mock_request,
                                                        return_value=response("post"))

        rsp = self.stackpath.post("/post", data={"foo": "bar"})
        expected = {"code": 200, "method": "post", "data": {"foo": "bar"}}
        self.assertEqual(rsp, expected)

        rsp = self.stackpath.post("/post", params={"foo": "bar"})
        self.assertEqual(rsp, expected)

        rsp = self.stackpath.post("/post", params="foo=bar")
        self.assertEqual(rsp, expected)

    def test_put(self):
        requests.Session.request = mock.create_autospec(mock_request,
                                                        return_value=response("put"))

        expected = {"code": 200, "method": "put", "data": {"foo": "bar"}}
        self.assertEqual(self.stackpath.put("/put"), expected)

    def test_delete(self):
        requests.Session.request = mock.create_autospec(mock_request,
                                                        return_value=response("delete"))

        expected = {"code": 200, "method": "delete", "data": {"foo": "bar"}}
        self.assertEqual(self.stackpath.delete("/delete"), expected)

        rsp = self.stackpath.patch("/delete.json", file_or_files="/foo.css")
        self.assertEqual(rsp, expected)

        files = ["/foo.css", "/bar.css"]
        expected = {"code": 200, "method": "delete", "data": {"foo": "bar"}}
        rsp = self.stackpath.patch("/delete", file_or_files=files)
        self.assertEqual(rsp, expected)

    def test_purge(self):
        requests.Session.request = mock.create_autospec(mock_request,
                                        return_value=response("delete"))

        expected = {"code": 200, "method": "delete", "data": {"foo": "bar"}}
        self.assertEqual(self.stackpath.purge(12345), expected)

        self.assertEqual(self.stackpath.purge(12345, "/master.css"), expected)

        files = ["/master.css", "/other.css"]
        self.assertEqual(self.stackpath.purge(12345, files), expected)

if __name__ == '__main__':
        unittest.main()
