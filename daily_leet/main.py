import typer

import requests
import re
from pathlib import Path

from .language_support.types import LangOptions, LangSlugs, to_lang_slug
from .fetch_data import (
    set_cookie,
    get_daily_challenge_title_slug,
    get_code_snippet,
    get_example_test_cases,
)
from .constants import LEETCODE_HOST
from .utils import BasicSpinner, open_in_browser, open_in_editor
from .language_support import create_files

app = typer.Typer()

lang_arg = typer.Argument(..., help="The language you want to use")


def fetch_data_and_create_files(
    session: requests.Session, lang_slug: LangSlugs, title_slug: str
) -> Path:
    try:
        set_cookie(session)
    except Exception as e:
        raise typer.BadParameter(f"Failed to get cookie from {LEETCODE_HOST}, {e}")

    with BasicSpinner() as progress:
        start_time = progress.get_time()
        progress.add_task(description="fetching code snippet...", total=None)
        code_snippet = get_code_snippet(session, title_slug, lang_slug)
        elapsed_time = progress.get_time() - start_time
        progress.print(
            f"[bold green]fetched code snippet in {elapsed_time:.2f}s[/bold green]"
        )

    with BasicSpinner() as progress:
        start_time = progress.get_time()
        progress.add_task(description="fetching example test cases...", total=None)
        example_test_cases = get_example_test_cases(session, title_slug)
        elapsed_time = progress.get_time() - start_time
        progress.print(
            f"[bold green]fetched example test cases in {elapsed_time:.2f}s[/bold green]"
        )

    typer.echo(f"Creating files for {title_slug} in {lang_slug.value}...")
    main_file_path = create_files(
        lang_slug, title_slug, code_snippet, example_test_cases
    )

    typer.echo(f"Created files for {title_slug} in {lang_slug.value}")

    return main_file_path


@app.command()
def daily(language: LangOptions = lang_arg):
    """
    Fetch today's daily challenge and create files for it, then open the problem page in browser and open the main file in editor
    """

    session = requests.Session()

    try:
        set_cookie(session)
    except Exception as e:
        raise typer.BadParameter(f"Failed to get cookie from {LEETCODE_HOST}, {e}")

    with BasicSpinner() as progress:
        start_time = progress.get_time()
        progress.add_task(description="fetching daily challenge...", total=None)
        title_slug = get_daily_challenge_title_slug(session)
        elapsed_time = progress.get_time() - start_time
        progress.print(
            f"[bold green]fetched daily challenge in {elapsed_time:.2f}s[/bold green]"
        )

    typer.echo(f"Today's problem is: {title_slug}")

    lang_slug = to_lang_slug(language)
    main_file_path = fetch_data_and_create_files(session, lang_slug, title_slug)

    session.close()

    open_in_browser(f"{LEETCODE_HOST}/problems/{title_slug}")
    open_in_editor(lang_slug, main_file_path)


@app.command()
def new(
    language: LangOptions = lang_arg,
    url: str = typer.Option(
        "",
        "-u",
        "--url",
        help="The url to fetch data from, usually a problem's description page. "
        + "e.g. https://leetcode.com/problems/two-sum/. "
        + "You need to provide either url or problem title.",
    ),
    problem_title: str = typer.Option(
        "",
        "-t",
        "--title",
        help="The title of the problem, separated by '-' or ' '. "
        + "e.g. two-sum. "
        + "You need to provide either url or problem title.",
    ),
):
    """
    Fetch data from a problem's description page and create files for it, then open the problem page in browser and open the main file in editor
    """

    # at least one of url or problem_name must be provided
    if not url and not problem_title:
        raise typer.BadParameter("Must provide either url or problem_name")

    title_slug = ""
    if problem_title != "":
        title_slug = problem_title.replace(" ", "-")
    elif url != "":
        # trim the trailing slash
        url = url.rstrip("/")
        pattern = f"{LEETCODE_HOST}/problems/(.*)".replace("/", "\\/")
        match = re.search(pattern, url)
        if match:
            title_slug = match.group(1)
        else:
            raise typer.BadParameter(f"Invalid url: {url}")

    session = requests.Session()

    lang_slug = to_lang_slug(language)
    main_file_path = fetch_data_and_create_files(session, lang_slug, title_slug)

    session.close()

    open_in_browser(f"{LEETCODE_HOST}/problems/{title_slug}")
    open_in_editor(lang_slug, main_file_path)


if __name__ == "__main__":
    app()
