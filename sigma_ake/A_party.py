from common_protocol import Initiator, jload, jstore
from party import G1, Party
from utils import G1, Fr, get_G1


class AParty(Initiator, Party):
    def __init__(self, ip: str, port: int, g: G1) -> None:
        Initiator.__init__(self, ip, port)
        Party.__init__(self, g)


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8800

    g = get_G1(value=b"seed")
    a = AParty(HOST, PORT, g)
    X = a.create_ephemerals(True)
    a.send_message(jstore({"s": a.s, "X": X, "A": a.public_key}))

    m1 = a.receive_message()
    data = jload(
        {
            "Y": G1,
            "sigma_b": (G1, Fr),
            "MAC_b": G1,
            "cert_b": G1,
            "B": G1,
        },
        m1,
        True,
    )

    a.set_other_pk(data["B"])
    a.receive_other_eph_pk(data["Y"])
    a.calculate_intermediate_keys()

    sign_X, sign_s = data["sigma_b"]
    sign_m = str(a.s) + "1" + str(X) + str(data["Y"])

    if a.check_MAC(data["MAC_b"], data["cert_b"]):
        print("MAC correct")
    else:
        raise ValueError("Incorrect MAC")
    if a.verify_signature(sign_X, sign_m, sign_s):
        print("Signature correct")
    else:
        raise ValueError("Incorrect signature")

    cert_a = G1.hashAndMapTo(b"certificate_a")
    sign_m = str(a.s) + "0" + str(X) + str(data["Y"])
    sigma_a = a.sign(sign_m)
    mac_a = a.calculate_MAC(cert_a)

    a.send_message(jstore({"sigma_a": sigma_a, "MAC_a": mac_a, "cert_a": cert_a}))

    print(f"Session key: {a.K0}")
