from common_protocol import Responder
from utils import G1, Fr, get_Fr, get_G1, jload, jstore


class Verifier(Responder):
    def __init__(self, g1: G1, g2: G1, ip: str = None, port: int = None):
        super().__init__(ip, port)
        self.g1 = g1
        self.g2 = g2
        self.public_key = None  # Prover's public key to be set
        self.c = None  # Challange to be generated
        self.X = None  # Commitment to be received

    def get_challange(self):
        self.c = get_Fr()
        return self.c

    def set_public_key(self, A):
        self.public_key = A

    def set_commitment(self, X):
        self.X = X

    def verify_proof(self, s1, s2) -> bool:
        if self.g1 * s1 + self.g2 * s2 == self.X + (self.public_key * self.c):
            return True
        else:
            return False


def main():
    HOST = "127.0.0.1"
    PORT = 8800
    g1 = get_G1(b"Scheme g1")
    g2 = get_G1(b"Scheme g2")
    verifier = Verifier(g1=g1, g2=g2, ip=HOST, port=PORT)

    # # Get Prover's public key
    _A = verifier.receive_message()
    A = jload({"A": G1}, _A)[0]
    verifier.set_public_key(A=A)

    # # Get commitment
    _X = verifier.receive_message()
    X = jload({"X": G1}, _X)[0]
    verifier.set_commitment(X)

    # # Send challange
    c = verifier.get_challange()
    verifier.send_message(message=jstore({"c": c}))

    # # Get proof
    _proof = verifier.receive_message()
    s1, s2 = jload({"s_1": Fr, "s_2": Fr}, _proof)

    # # Verify proof
    verified = verifier.verify_proof(s1, s2)
    ver_msg = f"{'Verified' if verified else 'Not verified'}"
    print(ver_msg)
    verifier.send_message(ver_msg)


if __name__ == "__main__":
    main()
