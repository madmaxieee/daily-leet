from pathlib import Path

import subprocess
import webbrowser
from rich.progress import Progress, SpinnerColumn, TextColumn

from .languages import LangSlugs

def BasicSpinner(transient=True):
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=transient,
    )

def open_in_browser(url: str) -> None:
    webbrowser.open(url)

def open_in_editor(lang_slug: LangSlugs, main_file_path: Path) -> None:
    subprocess.run(["code", lang_slug.value])
    subprocess.run(["code", "-a", main_file_path])
