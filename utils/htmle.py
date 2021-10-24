import html


def encode(string: str) -> str:
    try:
        encoded = html.escape(string)
    except Exception as e:
        encoded = str(e)

    return encoded


def decode(string: str) -> str:
    try:
        decoded = html.unescape(string)
    except Exception as e:
        decoded = str(e)
    
    return decoded
