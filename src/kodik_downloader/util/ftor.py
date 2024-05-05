import base64

def decode_ftor(src): 
    decoded = base64.b64decode(
        "".join(
            chr((ord(c) - 65 + 13) % 26 + 65) if c.isupper() else chr(
            (ord(c) - 97 + 13) % 26 + 97) if c.islower()
            else c for c in src
        ) + "=="
    ).decode()
    return decoded.split(":hls:")[0]
