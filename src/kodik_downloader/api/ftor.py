from .client import client

async def ftor(uid, type, hash, id, parameters={}):
    r = await client.post(
        f"https://kodik.biz/ftor", timeout=60,
        params=dict({"uid": uid, "type": type, "hash": hash, "id": id}, **parameters)
    )
    if "application/json" not in r.headers.get("Content-Type", ""):
        return {"links": {}}

    return r.json()
