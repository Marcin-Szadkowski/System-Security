import json
import sys

sys.path.insert(1, "/home/marcin/mcl-python")
import os

from mcl import G1, Fr


def get_fr():
    fr = Fr()
    fr.setByCSPRNG()
    return fr


def get_random_g1():
    rnd_bytes = os.urandom(16)
    g = G1.hashAndMapTo(rnd_bytes)
    return g


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
