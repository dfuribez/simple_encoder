import json

from . import base

def process(token):
    splited = token.split(".")
    if len(splited) != 3:
        return "Error", "Error", "Error"
    header, payload, signature = splited

    header_decoded = base.decode(header)
    payload_decoded = base.decode(payload)

    return header_decoded, payload_decoded, signature


def encode(header, payload, signature):
    try:
        json_header = json.loads(header)
        json_payload = json.loads(payload)
    except Exception as e:
        return "error.error.error"

    encoded_header = base.encode(json.dumps(json_header, indent=0, sort_keys=False))
    encoded_payload = base.encode(json.dumps(json_payload, indent=0, sort_keys=False))
    return f"{encoded_header}.{encoded_payload}.{signature}".replace("=", "")
