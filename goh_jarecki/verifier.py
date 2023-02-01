from common_protocol import Responder, jload
from utils import Fr, G2, get_G2, std_concat_method, get_Fr


class Verifier(Responder):
    def __init__(self, ip: str, port: int, g: G2) -> None:
        super().__init__(ip, port)
        self.g = g

    def verify(self, m: str, sigma: tuple, Y: G2) -> bool:
        rn, z, s, c = sigma
        h_prim = get_G2(value=std_concat_method(m, rn))

        u_prim = (self.g * s) - (Y * c)
        v_prim = (h_prim * s) - (z * c)

        c_prim = get_Fr(value=std_concat_method(self.g, h_prim, Y, z, u_prim, v_prim))
        return c == c_prim


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8800
    g = get_G2(value=b"seed")
    verifier = Verifier(HOST, PORT, g)

    message = verifier.receive_message()
    data = jload({"m": str, "sigma": (Fr, G2, Fr, Fr), "A": G2}, message, True)

    if verifier.verify(data["m"], data["sigma"], data["A"]):
        print("Accepted")
    else:
        print("Rejected")
