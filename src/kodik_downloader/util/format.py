from .. import api
from .ftor import decode_ftor
from tqdm import tqdm

async def format_results(results, key, link, uid, errors_out):
    urls = {}

    for result in tqdm(results, desc="Results", leave=False, mininterval=0.01):
        if key not in result: continue

        urls.setdefault(result[key], {}).setdefault(str(result["translation"]["id"]), {})

        if "seasons" not in result:
            if link == "player":
                urls[result[key]][str(result["translation"]["id"])] = result["link"]
            elif link == "download":
                movie_link_splitted = result["link"].split("/")
                for quality in (await api.ftor(uid, movie_link_splitted[3], movie_link_splitted[5], movie_link_splitted[4]))["links"].values():
                    quality_link = decode_ftor(quality[0]["src"])
                    urls[result[key]][str(result["translation"]["id"])][quality_link.split("/")[-1].split(".")[0]] = quality_link

            continue

        for season_key, season in tqdm(result["seasons"].items(), desc="Seasons", leave=False, mininterval=0.01):
            for episode_key, episode_link in tqdm(season.get("episodes", {}).items(), desc="Episodes", leave=False, mininterval=0.01):
                try:
                    if link == "player":
                        urls[result[key]][str(result["translation"]["id"])].setdefault(season_key, {})[episode_key] = episode_link
                    elif link == "download":
                        episode_link_splitted = episode_link.split("/")
                        for quality in (await api.ftor(uid, episode_link_splitted[3], episode_link_splitted[5], episode_link_splitted[4]))["links"].values():
                            quality_link = decode_ftor(quality[0]["src"])
                            urls[result[key]][str(result["translation"]["id"])].setdefault(season_key, {}).setdefault(episode_key, {})[quality_link.split("/")[-1].split(".")[0]] = quality_link
                except Exception as e:
                    log_error(f"Ftor error: {e}; kodik_id: {result['id']}; season: {season_key}; episode: {episode_key}; translation_id: {result['translation']['id']}", errors_out)
    
    return urls
