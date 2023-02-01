import json
import sys

sys.path.insert(1, "/home/marcin/mcl-python")
import os

from mcl import G1, G2, GT, Fr  # type: ignore


def get_Fr(value=None):
    fr = Fr()
    if value is None:
        fr.setByCSPRNG()
    elif isinstance(value, str):
        fr = Fr.setHashOf(value.encode())
    elif isinstance(value, bytes):
        fr = Fr.setHashOf(value)
    else:
        fr.setInt(value)
    return fr


def get_G1(value=None):
    if value is None:
        rnd_bytes = os.urandom(16)
        g = G1.hashAndMapTo(rnd_bytes)
    else:
        g = G1.hashAndMapTo(value)
    return g


def get_G2(value=None):
    if value is None:
        rnd_bytes = os.urandom(16)
        g = G2.hashAndMapTo(rnd_bytes)
    else:
        g = G2.hashAndMapTo(value)
    return g


def gen_g_hat(X, c):
    value = str.encode(str(X) + str(c))

    return get_G1(value=value)


def jstore(d):
    return json.dumps(
        {k: v.getStr().decode() if type(v) != bytes else v.hex() for k, v in d.items()}
    )


def jload(d, j):
    j = json.loads(j)
    r = []
    for k, t in d.items():
        if t != bytes:
            v = t()
            v.setStr(j[k].encode())
        else:
            v = t.fromhex(j[k])
        r.append(v)
    return r


def std_concat_method(*args):
    con = ""
    for arg in args:
        if isinstance(arg, str):
            con += arg
        else:
            con += str(arg)

    return con.encode()
