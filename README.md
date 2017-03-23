StackPath REST Web Services Python Client. This package is forked from https://github.com/MaxCDN/python-maxcdn/

Installation
------------

```
pip install stackpath
```

Usage
-----

```python
from stackpath import StackPath

api = StackPath("myalias", "consumer_key", "consumer_secret")

# Get Account Info
api.get("/account")

# Create Site
api.post("/sites", {'name': 'mypullzone', 'url': 'http://yourorigin.com', 'compress': '1'})

# Update Site
api.put("/sites/12345", {'url': 'http://neworigin.com'})

# Purge All Cache
api.purge(12345)

# Purge File
api.purge(12345, data={'file': '/my-file.png'})

```

Methods
-------

It has support for `GET`, `POST`, `PUT` and `DELETE` OAuth signed requests.

We now have a shortcut for Purge Calls!
--------------------------------------

```python
site_id = 12345

# Purge Zone
api.purge(site_id)

# Purge File
api.purge(site_id, '/some_file')

# Purge Files
api.purge(site_id, ['/some_file', '/another_file'])
```

Every request can take an optional debug parameter.
```python
api.get("account", debug=True)
# Will output
# Making GET request to http://rws.netdna.com/myalias/account
#{... API Returned Stuff ...}

Every request can also take an optional debug_json parameter if you don't like the exception based errors.
api.get('account', debug_json=True)
```


Initialization
--------------

For applications that don't require user authentication,
you can use the default initialization as the example above.

For applications that require user authentication, you can
initialize the API as follows.

```python
api = StackPath("myalias", "consumer_key", "consumer_secret")
```

You can also send the optional parameter header_auth, which takes a boolean
to send the OAuth header in the body or URLEncoded.

Development
-----------

```
git clone https://github.com/koty/python-stackpath.git
cd python-stackpath

make          # setup and test
make setup    # installation w/ deps
make test     # test w/ primary python
make int      # integration tests w/ primary python
make test/all # test w/ python2 python3.2 python3.3 python3.4
make int      # integration tests
make int/all  # integration w/ python2 python3.2 python3.3 python3.4
make nose     # verbose test output w/ nosetests
```

Examples
--------

Running examples:

```
git clone https://github.com/koty/python-stackpath.git
cd python-stackpath
make setup

export PYTHONPATH=./build:./stackpath

./examples/simple.py
./examples/report.py # [hourly|daily|monthly]
./examples/purge.py  # [zoneid]
```

