import logging

from common_protocol import Initiator
from utils import G1, G2, GT, gen_g_hat, get_Fr, jload, jstore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("verifier")

HOSTNAME = "127.0.0.1"
PORT = 8800


class Verifier(Initiator):
    def __init__(self, ip: str, port: int) -> None:
        super().__init__(ip, port)
        self.c = None  # random challange
        params = self.receive_message()
        logger.info("Verifier: params received")
        self.A, self.X, self.G = jload({"A": G2, "X": G2, "G": G2}, params)

    def send_challange(self) -> None:
        self.c = get_Fr()
        message = jstore({"c": self.c})
        self.send_message(message=message)

    def get_proof(self) -> None:
        signature_ = self.receive_message()
        self.s = jload({"s": G1}, signature_)[0]

    def verify(self) -> bool:
        g_hat = gen_g_hat(self.X, self.c)
        # # Accept iff e(S, g) == e(g_hat, XA^c)
        if GT.pairing(self.s, self.G) == GT.pairing(g_hat, self.X + self.A * self.c):
            logger.info("Verification correct")
            return True
        logger.info("Failed to verify")
        return False


def main():
    logger.info("Starting verifier...")
    verifier = Verifier(ip=HOSTNAME, port=PORT)
    verifier.send_challange()

    verifier.get_proof()
    verifier.verify()


if __name__ == "__main__":
    main()
