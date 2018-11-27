from io import StringIO

from OpenSSL.crypto import PKey, TYPE_RSA, FILETYPE_PEM, X509Req
from OpenSSL import crypto

CRITICAL = "critical"


# Generate private key
def generate_pkey():
    pkey = PKey()
    pkey.generate_key(type=TYPE_RSA, bits=2048)
    return pkey


def get_pkey(pk: PKey):
    return crypto.dump_privatekey(FILETYPE_PEM, pk).decode("utf-8")


def generate_req(pkey: PKey, common_name: str):
    req = X509Req()
    subj = req.get_subject()
    setattr(subj, "CN", common_name)
    setattr(subj, "C", "RU")
    setattr(subj, "O", "T2 Mobile")
    setattr(subj, "OU", "IT")
    setattr(subj, "ST", "Moscow")
    setattr(subj, "L", "Moscow")
    setattr(subj, "emailAddress", "admin@tele2.ru")
    req.set_pubkey(pkey)
    req.sign(pkey, "sha256")
    req.verify(pkey)

    return req


def get_req(req):
    return crypto.dump_certificate_request(FILETYPE_PEM, req).decode("utf-8")
