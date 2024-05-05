from .client import client
from ..util import log_error
from tqdm import tqdm

async def list(api_token, limit, errors_out, parameters={}):
    r = (await client.get(
        "https://kodikapi.com/list",
        params=dict({"token": api_token, "with_episodes": "true", "limit": min(limit, 100) if limit != None else 100}, **parameters)
    )).json()

    if "error" in r:
        log_error(f"List error: {r}", errors_out)
    
    pbar = tqdm(total=min(limit, r.get("total", 0)), initial=len(r.get("results", [])), desc="Fetching", leave=False, unit="", unit_scale=1)

    results: list[dict] = r.get("results", [])
    while "next_page" in r and (limit == None or len(results) < limit):
        r = (await client.get(r["next_page"])).json()
        results.extend(r.get("results", []))
        pbar.update(len(results[:limit])%100 or 100)

    pbar.close()
    return results[:limit]
