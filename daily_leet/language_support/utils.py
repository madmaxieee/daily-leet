import typer

from pathlib import Path
import datetime

from .types import LangSlugs

def get_displayed_test_case(example_test_cases: list[str], indent: str, comment: str) -> str:
    example_test_case_list = [case.replace("\n", " ") for case in example_test_cases]
    example_test_case_display = "\n".join([f"{indent}{comment} {case}" for case in example_test_case_list])

    return example_test_case_display

def get_displayed_time() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d")

def create_lang_dir(lang_slug: LangSlugs) -> Path:
    lang_dir = Path.cwd() / lang_slug.value
    if not lang_dir.exists():
        typer.confirm(f"{lang_dir} does not exist, create it?", abort=True, default=True)

    lang_dir.mkdir(parents=True, exist_ok=True)
    return lang_dir
