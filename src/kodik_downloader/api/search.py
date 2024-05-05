from .client import client
from ..util import log_error

async def search(api_token, errors_out, parameters={}):
    r = (await client.get(
        "https://kodikapi.com/search",
        params=dict({"token": api_token, "with_episodes": "true"}, **parameters)
    )).json()

    if "error" in r:
        log_error(f"Search error: {r}", errors_out)

    return r.get("results", [])
