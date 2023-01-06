import logging
from typing import Callable

from common_protocol import Responder
from utils import Fr, get_random_g1, jload, jstore

HOSTNAME = "172.20.10.3"
PORT = 667

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prover")


class Prover(Responder):
    def __init__(self, ip: str, port: int, callback: Callable = None) -> None:
        super().__init__(ip, port, callback)
        self.a = Fr()
        self.x = Fr()
        self.s = Fr()
        self.c = Fr()
        self.G = get_random_g1()
        self.a.setByCSPRNG()
        self.x.setByCSPRNG()

    def send_params(self) -> None:
        A = self.G * self.a
        X = self.G * self.x
        message = jstore({"A": A, "X": X, "G": self.G})

        self.send_message(message=message)

    def get_challange(self) -> None:
        challange = self.receive_message()
        logger.info("Prover: challange received")

        self.c = jload({"c": Fr}, challange)[0]

    def send_signature(self) -> None:
        self.s = self.x + self.a * self.c

        message = jstore({"s": self.s})
        self.send_message(message=message)


def main():
    logger.info("Staring prover...")
    prover = Prover(ip=HOSTNAME, port=PORT)
    prover.send_params()

    prover.get_challange()
    prover.send_signature()


if __name__ == "__main__":
    main()
