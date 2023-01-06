import logging

from common_protocol import Initiator, jstore
from utils import G1, G2, get_Fr, get_G1, get_G2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("signer")


class Signer(Initiator):
    def __init__(self, g2: G2, ip: str, port: int):
        super().__init__(ip, port)
        self.g2 = g2
        self.x = get_Fr()
        self._public_key = self.g2 * self.x  # v = g2^x

    @property
    def public_key(self):
        return self._public_key

    def sign(self, m: str) -> G1:
        h = get_G1(value=m.encode())
        sigma = h * self.x  # sigma = h^x

        return sigma


def main():
    logger.info("Starting Signer...")
    HOST = "127.0.0.1"
    PORT = 8800
    g2 = get_G2(value=b"BlsScheme")
    signer = Signer(g2=g2, ip=HOST, port=PORT)

    v = signer.public_key

    m = "Hello world"
    sigma = signer.sign(m)
    signer.send_message(message=jstore({"S": sigma, "m": m, "v": v}))


if __name__ == "__main__":
    main()
