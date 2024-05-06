import click
import kodik_downloader
import json

@click.command()
@click.option("--api", required=True, type=str, help="Kodik public api token")
@click.option("--uid", required=True, type=str, help="Kodik uid")
@click.option("-o", "--out", type=click.File(mode="w"), help="File for saving the result")
@click.option("-e", "--errors-out", type=click.File(mode="w"), help="Error logging file")
@click.option("-l", "--limit", type=click.IntRange(1), help="Maximum number of results")
@click.option("-p", "--parameter", "parameters", type=(str, str), multiple=True, help="Kodik list api parameters")
@click.option("--player-link", "link", flag_value="player", default=True, help="Use a player link")
@click.option("--download-link", "link", flag_value="download", help="Use a video file link")
@click.option("-k", "--key", default="id", type=click.Choice([
    "title", "title_orig", "id", "player_link", "kinopoisk_id", 
    "imdb_id", "mdl_id", "worldart_animation_id", 
    "worldart_cinema_id", "worldart_link", "shikimori_id"], case_sensitive=False), help="Parameter from api that is a key in result")
@kodik_downloader.util.coro
async def list(api, uid, out, errors_out, limit, link, key, parameters):
    extra_parameters = tuple()

    if key in ["kinopoisk_id", "imdb_id", "mdl_id", "worldart_link", "shikimori_id"]:
        extra_parameters += (("has_field", key),)

    results = await kodik_downloader.api.list(api, limit, errors_out, dict(extra_parameters + parameters))
    urls = await kodik_downloader.util.format_results(results, key, link, uid, errors_out)

    if out == None:
        print(json.dumps(urls))
    else:
        out.write(json.dumps(urls, indent=1))

    if errors_out == None:
        print("\n".join(kodik_downloader.util.errors))
