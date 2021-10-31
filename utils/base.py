import base64


def encode(string: str) -> str:
    try:
        encoded = base64.b64encode(string.encode("utf8")).decode("utf8")
    except Exception as e:
        encoded = str(e)
    
    return encoded


def decode(string: str) -> str:
    try:
        string += "=="
        decoded = base64.b64decode(string.encode("utf8")).decode("utf8")
    except Exception as e:
        decoded = str(e)
    
    return decoded
