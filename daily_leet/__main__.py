import typer

import requests
import re

from .languages import LangOptions, to_lang_slug
from .fetch_data import set_cookie, get_code_snippet, get_daily_challenge_title_slug
from .constants import LEETCODE_HOST
from .utils import BasicSpinner

app = typer.Typer()

lang_arg = typer.Argument(..., help="The language you want to use")


@app.command()
def daily(language: LangOptions = lang_arg):
    session = requests.Session()

    try:
        set_cookie(session)
    except Exception as e:
        raise typer.BadParameter(f"Failed to get cookie from {LEETCODE_HOST}, {e}")

    with BasicSpinner() as progress:
        progress.add_task(description="fetching daily challenge...", total=None)
        title_slug = get_daily_challenge_title_slug(session)
        time = progress.get_time()
        progress.print(f"[bold green]fetched daily challenge in {time:.2f}s[/bold green]")

    typer.echo(f"Today's problem is: {title_slug}")

    with BasicSpinner() as progress:
        progress.add_task(description="fetching code snippet...", total=None)
        code_snippet = get_code_snippet(session, title_slug, to_lang_slug(language))
        time = progress.get_time()
        progress.print(f"[bold green]fetched code snippet in {time:.2f}s[/bold green]")


@app.command()
def new(
    language: LangOptions = lang_arg,
    url: str = typer.Option(
        "",
        "-u",
        "--url",
        help="The url to fetch data from, usually a problem's description page",
    ),
    problem_title: str = typer.Option(
        "", "-t", "--title", help="The title of the problem, separated by '-' or ' '"
    ),
):
    # at least one of url or problem_name must be provided
    if not url and not problem_title:
        raise typer.BadParameter("Must provide either url or problem_name")

    title_slug = ""
    if problem_title != "":
        title_slug = problem_title.replace(" ", "-")
    elif url != "":
        pattern = f"{LEETCODE_HOST}/problems/(.*)/?".replace("/", "\\/")
        match = re.search(pattern, url)
        if match:
            title_slug = match.group(1)
        else:
            raise typer.BadParameter(f"Invalid url: {url}")

    session = requests.Session()

    try:
        set_cookie(session)
    except Exception as e:
        raise typer.BadParameter(f"Failed to get cookie from {LEETCODE_HOST}, {e}")

    code_snippet = get_code_snippet(session, title_slug, to_lang_slug(language))


if __name__ == "__main__":
    app()
