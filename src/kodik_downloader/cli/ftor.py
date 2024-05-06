import click
import kodik_downloader
import json

@click.command()
@click.option("--uid", required=True, type=str, help="Kodik uid")
@click.option("-o", "--out", type=click.File(mode="w"), help="File for saving the result")
@click.option("-a", "--all-qualities", "all_qualities", flag_value=1, default=True, help="Return json with all qualities")
@click.option("-h", "--highest-quality", "all_qualities", flag_value=0, help="Return only the highest quality")
@click.option("-p", "--parameter", "parameters", type=(str, str), multiple=True, help="Kodik ftor api parameters")
@click.argument("episode-player-link", type=str)
@kodik_downloader.util.coro
async def ftor(uid, out, all_qualities, parameters, episode_player_link):
    if not episode_player_link.startswith("https://") and not episode_player_link.startswith("http://") and not episode_player_link.startswith("//"):
        episode_player_link = "//" + episode_player_link

    link_splitted = episode_player_link.split("/")
    if len(link_splitted) < 6:
        return print("Error: invalid episode player link. Example link: '//kodik.biz/seria/118112/0602482a6f1bf5ee427466525db680f3/720p'")

    qualities = (await kodik_downloader.api.ftor(uid, link_splitted[3], link_splitted[5], link_splitted[4]))["links"]

    result = dict()
    for quality in qualities.values():
        quality_link = kodik_downloader.util.decode_ftor(quality[0]["src"])
        result[quality_link.split("/")[-1].split(".")[0]] = quality_link
    
    if all_qualities == 1:
        if out == None: print(json.dumps(result))
        else: out.write(json.dumps(result, indent=1))
    else:
        if out == None: print(result[max(result)])
        else: out.write(result[max(result)])
