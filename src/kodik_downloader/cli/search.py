import click
import kodik_downloader
import json

@click.command()
@click.option("--api", required=True, type=str, help="kodik public api token")
@click.option("--uid", required=True, type=str, help="kodik uid")
@click.option("-o", "--out", type=click.File(mode="w"), help="file for saving the result")
@click.option("-e", "--errors-out", type=click.File(mode="w"), help="error logging file")
@click.option("-l", "--limit", type=click.IntRange(1), help="maximum number of results")
@click.option("-p", "--parameter", "parameters", type=(str, str), multiple=True, help="kodik search api parameters")
@click.option("--player-link", "link", flag_value="player", default=True, help="use a player link")
@click.option("--download-link", "link", flag_value="download", help="use a video file link")
@click.option("-k", "--key", default="id", type=click.Choice([
    "title", "title_orig", "id", "player_link", "kinopoisk_id", 
    "imdb_id", "mdl_id", "worldart_animation_id", 
    "worldart_cinema_id", "worldart_link", "shikimori_id"], case_sensitive=False), help="parameter from api that is a key in result")
@kodik_downloader.util.coro
async def search(api, uid, out, errors_out, limit, link, key, parameters):
    extra_parameters = tuple()

    if key in ["kinopoisk_id", "imdb_id", "mdl_id", "worldart_link", "shikimori_id"]:
        extra_parameters += (("has_field", key),)
    if limit != None:
        extra_parameters += (("limit", limit),)

    results = await kodik_downloader.api.search(api, errors_out, dict(extra_parameters + parameters))
    urls = await kodik_downloader.util.format_results(results, key, link, uid, errors_out)

    if out == None:
        print(json.dumps(urls))
    else:
        out.write(json.dumps(urls, indent=1))


    if errors_out == None:
        print("\n".join(kodik_downloader.util.errors))
