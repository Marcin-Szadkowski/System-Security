import hashlib
from abc import ABC, abstractmethod
from random import getrandbits

from utils import G2, get_Fr, std_concat_method


class NaxosParty(ABC):
    def __init__(self, g: G2, _lambda: int):
        self.g = g
        self.sk_m = get_Fr()
        self.pk_m = self.g * self.sk_m
        self.esk_m = getrandbits(_lambda)

        self.pk_y = None
        self.commitment_exp_m = None
        self.commitment_m = None
        self.commitment_y = None
        self._session_key = None

    @property
    def session_key(self):
        if self._session_key is None:
            return None
        if not hasattr(self._session_key, "hex"):
            raise RuntimeError("Session key has no attribute hex")
        return self._session_key.hex()

    def set_other_party_pk(self, pk_y):
        self.pk_y = pk_y

    def produce_commitment(self):
        self.commitment_exp_m = get_Fr(value=std_concat_method(self.esk_m, self.sk_m))
        self.commitment_m = self.g * self.commitment_exp_m
        return self.commitment_m

    def set_other_party_commitment(self, commitment_y):
        self.commitment_y = commitment_y

    def get_concat_hash(self, *args) -> bytes:
        hash_obj = hashlib.sha256()
        concat = std_concat_method(args)
        hash_obj.update(concat)
        return hash_obj.digest()

    @abstractmethod
    def calculate_session_key(self):
        pass


class NaxosPartyA(NaxosParty):
    def calculate_session_key(self):
        t1 = self.commitment_y * self.sk_m
        t2 = self.pk_y * self.commitment_exp_m
        t3 = self.commitment_y * self.commitment_exp_m
        self._session_key = self.get_concat_hash(t1, t2, t3, self.pk_m, self.pk_y)


class NaxosPartyB(NaxosParty):
    def calculate_session_key(self):
        t1 = self.pk_y * self.commitment_exp_m
        t2 = self.commitment_y * self.sk_m
        t3 = self.commitment_y * self.commitment_exp_m
        self._session_key = self.get_concat_hash(t1, t2, t3, self.pk_y, self.pk_m)
