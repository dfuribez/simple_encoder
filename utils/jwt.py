from . import base

def process(token):
    splited = token.split(".")
    if len(splited) != 3:
        return "Error", "Error", "Error"
    header, payload, signature = splited

    header_decoded = base.decode(header)
    payload_decoded = base.decode(payload)

    return header_decoded, payload_decoded, signature