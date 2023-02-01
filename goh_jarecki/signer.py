import random
from common_protocol import Initiator, jstore
from utils import Fr, G2, get_G2, get_Fr, std_concat_method


class Signer(Initiator):
    def __init__(self, ip: str, port: int, g: G2) -> None:
        super().__init__(ip, port)
        self.g = g
        self.x = get_Fr()

        self.h = None
        self.z = None
        self.s = None
        self.rn = get_Fr(value=random.randbytes(111))

        self._public_key = self.g * self.x

    @property
    def public_key(self):
        return self._public_key

    def sign(self, m: str):
        # h = H(m, r)
        self.h = get_G2(value=(m + str(self.rn)).encode())
        self.z = self.h * self.x
        k = get_Fr()

        u = self.g * k
        v = self.h * k

        self.c = get_Fr(
            value=std_concat_method(  # concat and encode as bytes
                self.g, self.h, self._public_key, self.z, u, v
            )
        )
        self.s = k + self.x * self.c
        return self.rn, self.z, self.s, self.c


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8800
    g = get_G2(value=b"seed")
    signer = Signer(HOST, PORT, g)

    Y = signer.public_key  # Y = g ^ x
    m = "Hello secret"
    sigma = signer.sign(m)
    signer.send_message(jstore({"m": m, "sigma": sigma, "A": Y}))
