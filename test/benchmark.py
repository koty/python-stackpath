import os
from stackpath import StackPath

alias = os.environ["ALIAS"]
key = os.environ["KEY"]
secret = os.environ["SECRET"]
stackpath = StackPath(alias, key, secret)


def get_logs():
    stackpath.get("/logs")


def get_users():
    stackpath.get("/users")


def get_account():
    stackpath.get("/account")


def get_pull():
    stackpath.get("/sites")


if __name__ == '__main__':
    import timeit

    for f in [ 'get_logs',
            'get_users',
            'get_account',
            'get_pullzones' ]:
        t = timeit.Timer(f + "()", setup = "from __main__ import " + f)
        print("%-20s %5.0fms" % (f + ":", (t.timeit(number=1) * 1000)))
