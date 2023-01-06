import logging

from common_protocol import Responder, jload
from utils import G2, Fr, get_G2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("verifier")


class Verifier(Responder):
    def __init__(self, g: G2, ip: str, port: int):
        super().__init__(ip, port)
        self.g = g

    def verify(self, A, signature: tuple[G2, Fr], m) -> bool:
        X, s = signature
        h = Fr.setHashOf(str.encode(str(X) + str(m)))

        # # Accept iff g^s = XA^h
        return self.g * s == X + (A * h)


def main():
    logger.info("Starting Verifier...")
    HOST = "127.0.0.1"
    PORT = 8800
    g = get_G2(value=b"SchnorSign")
    verifier = Verifier(g=g, ip=HOST, port=PORT)

    _payload = verifier.receive_message()
    payload = jload({"X": G2, "s": Fr, "m": str, "A": G2}, _payload, True)

    X, s, m, A = (
        payload["X"],
        payload["s"],
        payload["m"],
        payload["A"],
    )
    signature = (X, s)

    verified = verifier.verify(A, signature, m)
    logger.info(f"Verification: {'OK' if verified else 'Failed'}")


if __name__ == "__main__":
    main()
