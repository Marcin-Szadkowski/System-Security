import logging

from common_protocol import Responder, jload, jstore
from naxos_party import NaxosPartyB
from utils import G2, LAMBDA, get_G2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("B_party")


class BParty(Responder, NaxosPartyB):
    def __init__(self, g: G2, _lambda: int, ip: str = None, port: int = None):
        Responder.__init__(self, ip, port)
        NaxosPartyB.__init__(self, g=g, _lambda=_lambda)


def main():
    HOST = "localhost"
    PORT = 8800
    g = get_G2(value=b"seed")

    logger.info("Starting...")
    party = BParty(g=g, _lambda=LAMBDA, ip=HOST, port=PORT)

    pk_A_ = party.receive_message()
    pk_A = jload({"pk_A": G2}, pk_A_, True)["pk_A"]
    party.set_other_party_pk(pk_A)

    party.send_message(message=jstore({"pk_B": party.pk_m}))

    X_ = party.receive_message()
    X = jload({"X": G2}, X_, True)["X"]
    party.set_other_party_commitment(X)

    party.send_message(message=jstore({"Y": party.produce_commitment()}))

    party.calculate_session_key()
    logger.info(f"session key: {party.session_key}")


if __name__ == "__main__":
    main()
