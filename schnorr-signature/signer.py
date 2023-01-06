import logging
from dataclasses import dataclass

from common_protocol import Initiator, jstore
from utils import G2, Fr, get_Fr, get_G2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("signer")


@dataclass
class Signature:
    X: G2
    s: Fr


class Signer(Initiator):
    def __init__(self, g: G2, ip: str, port: int):
        super().__init__(ip, port)
        self.g = g
        self.a = get_Fr()  # private key
        self._public_key = self.g * self.a  # public key

    @property
    def public_key(self):
        return self._public_key

    def sign(self, m: str) -> tuple:
        x = get_Fr()
        X = self.g * x  # X = g^x
        h = Fr.setHashOf(str.encode(str(X) + str(m)))  # h = H(X, m)
        s = x + self.a * h  # s = x + ah

        # sigma = (X, s)
        return Signature(X=X, s=s)


def main():
    logger.info("Starting Signer...")
    HOST = "127.0.0.1"
    PORT = 8800
    g = get_G2(value=b"SchnorSign")
    signer = Signer(g=g, ip=HOST, port=PORT)

    public_key = signer.public_key

    message = "Hello world"
    signature = signer.sign(message)

    signer.send_message(
        message=jstore(
            {"X": signature.X, "s": signature.s, "m": message, "A": public_key}
        )
    )


if __name__ == "__main__":
    main()
