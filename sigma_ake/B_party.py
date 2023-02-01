from common_protocol import Responder, jload, jstore
from party import G1, Party
from utils import G1, Fr, get_G1


class BParty(Responder, Party):
    def __init__(self, ip: str, port: int, g: G1) -> None:
        Responder.__init__(self, ip, port)
        Party.__init__(self, g)


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8800

    g = get_G1(value=b"seed")
    b = BParty(HOST, PORT, g)
    Y = b.create_ephemerals(False)

    m1 = b.receive_message()
    data = jload({"s": Fr, "X": G1, "A": G1}, m1, True)

    b.set_other_pk(data["A"])
    b.receive_other_eph_pk(data["X"])
    b.receive_s(data["s"])

    b.calculate_intermediate_keys()
    sign_m = str(data["s"]) + "1" + str(data["X"]) + str(Y)
    cert_b = G1.hashAndMapTo(b"certificate_b")
    sigma_b = b.sign(sign_m)
    mac_b = b.calculate_MAC(cert_b)

    b.send_message(
        jstore(
            {
                "Y": Y,
                "sigma_b": sigma_b,
                "MAC_b": mac_b,
                "cert_b": cert_b,
                "B": b.public_key,
            },
        )
    )

    m2 = b.receive_message()
    data = jload(
        {"sigma_a": (G1, Fr), "MAC_a": G1, "cert_a": G1},
        m2,
        True,
    )

    sign_X, sign_s = data["sigma_a"]
    sign_m = str(b.s) + "0" + str(b.other_eph_pk) + str(Y)

    if b.check_MAC(data["MAC_a"], data["cert_a"]):
        print("MAC correct")
    else:
        raise ValueError("Incorrect MAC")
    if b.verify_signature(sign_X, sign_m, sign_s):
        print("Signature correct")
    else:
        raise ValueError("Incorrect signature")

    print(f"Session key: {b.K0}")
