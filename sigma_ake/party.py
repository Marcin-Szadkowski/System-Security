from utils import G1, Fr, get_Fr, get_G1, std_concat_method


class Party:
    def __init__(self, g: G1) -> None:
        self.g = g
        self._secret_key = get_Fr()
        self._public_key = None
        self.other_pk = None

        self.s = None
        self.eph_sk = get_Fr()
        self.eph_pk = None
        self.other_eph_pk = None
        self.K = None
        self.K0 = None
        self.K1 = None

        self._public_key = self.g * self._secret_key

    @property
    def public_key(self):
        return self._public_key

    def create_ephemerals(self, is_initiator: bool):
        self.eph_pk = self.g * self.eph_sk
        if is_initiator:
            self.s = get_Fr()
        return self.eph_pk

    def set_other_pk(self, pk: G1) -> None:
        self.other_pk = pk

    def receive_other_eph_pk(self, pk: G1) -> None:
        self.other_eph_pk = pk

    def receive_s(self, s: Fr) -> None:
        self.s = s

    def calculate_intermediate_keys(self) -> None:
        self.K = self.other_pk * self._secret_key
        self.K0 = get_G1(value=std_concat_method(self.K, "0"))
        self.K1 = get_G1(value=std_concat_method(self.K, "1"))

    def sign(self, m: str):
        x = get_Fr()
        X = self.g * x
        h = get_Fr(value=std_concat_method(X, m))
        s = x + self._secret_key * h
        return X, s

    def verify_signature(self, X, m: str, s: Fr) -> bool:
        h = get_Fr(value=std_concat_method(X, m))
        return self.g * s == X + (self.other_pk * h)

    def calculate_MAC(self, cert: G1) -> G1:
        return get_G1(value=std_concat_method(self.K0, self.s, cert))

    def check_MAC(self, mac: G1, cert: G1) -> bool:
        return mac == self.calculate_MAC(cert)
