import logging

from common_protocol import Initiator, jload, jstore
from naxos_party import NaxosPartyA
from utils import G2, LAMBDA, get_G2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("A_party")


class AParty(Initiator, NaxosPartyA):
    def __init__(self, g: G2, _lambda: int, ip: str = None, port: int = None):
        Initiator.__init__(self, ip, port)
        NaxosPartyA.__init__(self, g=g, _lambda=_lambda)


def main():
    HOST = "localhost"
    PORT = 8800
    g = get_G2(value=b"seed")

    logger.info("Starting...")
    party = AParty(g=g, _lambda=LAMBDA, ip=HOST, port=PORT)

    party.send_message(message=jstore({"pk_A": party.pk_m}))

    pk_B_ = party.receive_message()
    pk_B = jload({"pk_B": G2}, pk_B_, True)["pk_B"]
    party.set_other_party_pk(pk_B)

    party.send_message(message=jstore({"X": party.produce_commitment()}))

    Y_ = party.receive_message()
    Y = jload({"Y": G2}, Y_, True)["Y"]
    party.set_other_party_commitment(Y)

    party.calculate_session_key()
    logger.info(f"session key: {party.session_key}")


if __name__ == "__main__":
    main()
