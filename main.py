import asyncio
import httpx
import aiofiles
from tqdm import tqdm
import base64
import json

api_token = input("Kodik public api token: ")
uid = input("Kodik account uid: ")

client = httpx.AsyncClient()

errors = []
async def log_error(error):
    errors.append(error)
    async with aiofiles.open("errors.txt", "w") as out:
        await out.write("\n".join(errors))
        await out.flush()

async def search_api(**params):
    r = (await client.get(
        f"https://kodikapi.com/search",
        params=dict({"token": api_token, "with_episodes": "true"},**params)
    )).json()
    
    if "error" in r:
        print("Error:",r)
        return []

    return r["results"]

async def list_api(**params):
    r = (await client.get(
        f"https://kodikapi.com/list",
        params=dict({"token": api_token, "with_episodes": "true", "limit": 100}, **params)
    )).json()

    pbar = tqdm(total=r["total"], initial=len(r["results"]), desc="Fetching")

    results: list[dict] = r["results"]
    while r["next_page"] != None:
        r = (await client.get(r["next_page"])).json()
        results.extend(r["results"])
        pbar.update(len(r["results"]))

    pbar.close()
    return results

async def ftor_api(link, shikimori_id, translation_id, season, episode, **params):
    splitted = link.split("/")

    try:
        r = (await client.post(
            f"https://kodik.biz/ftor", timeout=60,
            params=dict({"uid": uid, "type": splitted[3], "hash": splitted[5], "id": splitted[4]}, **params)
        ))
        try:
            return r.json()
        except Exception as e:
            await log_error(f"{e} {r.text()}; shikimori_id: {link}; translation_id: {translation_id}; season: {season}; episode: {episode}")
            return {"links": {}}
    except Exception as e:
        await log_error(f"{e} {r}; shikimori_id: {link}; translation_id: {translation_id}; season: {season}; episode: {episode}")
        return {"links": {}}

def decode_link(link): 
    decoded = base64.b64decode("".join(chr((ord(c) - 65 + 13) % 26 + 65) if c.isupper() else chr((ord(c) - 97 + 13) % 26 + 97) if c.islower() else c for c in link) + "==").decode()
    return decoded.split(":hls:")[0]

async def get_urls(is_list = False, player_url = True, **params):
    urls = {}

    if not is_list:
        results = await search_api(**params)
    else:
        results = await list_api(**params)

    for result in tqdm(results, desc="Results", mininterval=0.01):
        if "seasons" not in result:
            if player_url:
                urls.setdefault(result["id"], {})[str(result["translation"]["id"])] = result["link"]
                continue
            for quality in (await ftor_api(result["link"], result.get("shikimori_id", "null"), result["translation"]["id"], "movie", "movie"))["links"].values():
                link = decode_link(quality[0]["src"])
                urls.setdefault(result["id"], {}).setdefault(str(result["translation"]["id"]), {})[link.split("/")[-1].split(".")[0]] = link
            continue
        for season in tqdm(result.get("seasons", {}), desc="Seasons", leave=False, mininterval=0.01):
            for episode in tqdm(result["seasons"][season].get("episodes", {}), desc="Episodes", leave=False, mininterval=0.01):
                if player_url:
                    urls.setdefault(result["id"], {}).setdefault(str(result["translation"]["id"]), {})\
                        .setdefault(season, {})[episode] = result["seasons"][season]["episodes"][episode]
                    continue
                for quality in (await ftor_api(result["seasons"][season]["episodes"][episode], result.get("shikimori_id", "null"), result["translation"]["id"], season, episode))["links"].values():
                    link = decode_link(quality[0]["src"])
                    urls.setdefault(result["id"], {}).setdefault(str(result["translation"]["id"]), {})\
                        .setdefault(season, {}).setdefault(episode, {})[link.split("/")[-1].split(".")[0]] = link

    print("\n".join(errors))
    async with aiofiles.open("urls.json", "w") as out:
        await out.write(json.dumps(urls, indent=1))
        await out.flush()

# asyncio.run(get_urls(False, False, shikimori_id=1))
asyncio.run(get_urls(True, False, types="anime"))
