import logging

from common_protocol import Initiator
from utils import G1, Fr, get_fr, jload, jstore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("verifier")

HOSTNAME = "172.20.10.1"
PORT = 666


class Verifier(Initiator):
    def __init__(self, ip: str, port: int) -> None:
        super().__init__(ip, port)
        self.c = None  # random challange
        params = self.receive_message()
        logger.info("Verifier: params received")
        self.A, self.X, self.G = jload({"A": G1, "X": G1, "G": G1}, params)

    def send_challange(self) -> None:
        self.c = get_fr()
        message = jstore({"c": self.c})
        self.send_message(message=message)

    def get_signature(self) -> None:
        signature_ = self.receive_message()
        self.s = jload({"s": Fr}, signature_)[0]

    def verify(self) -> bool:
        S = self.G * self.s
        cA = self.A * self.c
        XcA = self.X + cA
        is_ok = S == XcA
        logger.info(f"Verification: {'correct' if is_ok else 'not correct'}")

        return is_ok


def main():
    logger.info("Starting verifier...")
    verifier = Verifier(ip=HOSTNAME, port=PORT)
    verifier.send_challange()

    verifier.get_signature()
    verifier.verify()


if __name__ == "__main__":
    main()
