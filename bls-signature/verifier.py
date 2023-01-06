import logging

from common_protocol import Responder, jload
from utils import G1, G2, GT, get_G1, get_G2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("verifier")


class Verifier(Responder):
    def __init__(self, g2: G2, ip: str, port: int):
        super().__init__(ip, port)
        self.g2 = g2

    def verify(self, v, sigma, m) -> bool:
        h = get_G1(value=m.encode())

        return GT.pairing(sigma, self.g2) == GT.pairing(h, v)


def main():
    logger.info("Starting Verifier...")
    HOST = "127.0.0.1"
    PORT = 8800
    g2 = get_G2(value=b"BlsScheme")
    verifier = Verifier(g2=g2, ip=HOST, port=PORT)

    _payload = verifier.receive_message()
    payload = jload({"S": G1, "m": str, "v": G2}, _payload, True)
    sigma, m, v = (
        payload["S"],
        payload["m"],
        payload["v"],
    )

    # Verify given public key, signature, message
    verified = verifier.verify(v, sigma, m)
    logger.info(f"Verification: {'OK' if verified else 'Failed'}")


if __name__ == "__main__":
    main()
