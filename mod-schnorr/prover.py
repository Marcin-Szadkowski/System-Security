import logging
from typing import Callable

from common_protocol import Responder
from utils import Fr, gen_g_hat, get_Fr, get_G2, jload, jstore

HOSTNAME = "127.0.0.1"
PORT = 8800

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prover")


class Prover(Responder):
    def __init__(self, ip: str, port: int, callback: Callable = None) -> None:
        super().__init__(ip, port, callback)
        self.a = get_Fr()
        self.x = get_Fr()
        self.s = None  # proof to be calculated
        self.c = None  # challange to be received
        self.G = get_G2()
        self.X = None

    def send_params(self) -> None:
        A = self.G * self.a  # public key G^a
        self.X = self.G * self.x  # Commitment g^x
        message = jstore({"A": A, "X": self.X, "G": self.G})

        self.send_message(message=message)

    def get_challange(self) -> None:
        challange = self.receive_message()
        logger.info("Prover: challange received")

        self.c = jload({"c": Fr}, challange)[0]

    def send_proof(self) -> None:
        g_hat = gen_g_hat(self.X, self.c)
        self.s = g_hat * (self.x + self.a * self.c)

        message = jstore({"s": self.s})
        self.send_message(message=message)


def main():
    logger.info("Staring prover...")
    prover = Prover(ip=HOSTNAME, port=PORT)
    prover.send_params()

    prover.get_challange()
    prover.send_proof()


if __name__ == "__main__":
    main()
