from common_protocol import Initiator
from utils import G1, Fr, get_Fr, get_G1, jload, jstore


class Prover(Initiator):
    def __init__(self, g1: G1, g2: G1, ip: str = None, port: int = None):
        self.g1 = g1
        self.g2 = g2
        # private values
        self.a1 = get_Fr()
        self.a2 = get_Fr()
        # x1, x2 <-$ Z_q*
        self.x1 = None
        self.x2 = None
        # commitment
        self.X = None
        self._public_key = self.g1 * self.a1 + self.g2 * self.a2  # A

    @property
    def public_key(self) -> G1:
        return self._public_key

    def get_commitment(self) -> G1:
        self.x1 = get_Fr()
        self.x2 = get_Fr()
        self.X = self.g1 * self.x1 + self.g2 * self.x2
        return self.X

    def get_proof(self, challange) -> tuple:
        s1 = self.x1 + self.a1 * challange
        s2 = self.x2 + self.a2 * challange
        return s1, s2


def main():
    HOST = "127.0.0.1"
    PORT = 8800
    g1 = get_G1(b"Scheme g1")
    g2 = get_G1(b"Scheme g2")
    prover = Prover(g1=g1, g2=g2, ip=HOST, port=PORT)

    # # Get Prover public key and send it to Verifier
    A = prover.public_key
    prover.send_message(message=jstore({"A": A}))

    # # Send Prover's commitment
    X = prover.get_commitment()
    prover.send_message(message=jstore({"X": X}))

    # # Receive challange
    _C = prover.receive_message()
    challange = jload({"c": Fr}, _C)[0]

    # # Send proof
    s1, s2 = prover.get_proof(challange)
    prover.send_message(message=jstore({"s_1": s1, "s_2": s2}))

    status = prover.receive_message()
    print(status)


if __name__ == "__main__":
    main()
