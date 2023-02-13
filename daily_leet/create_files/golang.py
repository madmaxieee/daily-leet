from pathlib import Path

from .utils import get_displayed_test_case, get_displayed_time

LANG = "golang"
COMMENT = "//"
INDENT = "    "
BOILERPLATE = f"""// %s {get_displayed_time}

package main

import "fmt"

%s

func main() {{
%s
}}
"""


def create_go_file(title_slug: str, code_snippet: str, example_test_case: str) -> None:
    example_test_case_display = get_displayed_test_case(example_test_case, INDENT, COMMENT)
    code = BOILERPLATE % (title_slug, code_snippet, example_test_case_display)

    lang_dir = Path(LANG)
    lang_dir.mkdir(exist_ok=True)

    (lang_dir / title_slug).mkdir(exist_ok=True)

    with open(lang_dir / title_slug / "main.go", "w") as f:
        f.write(code)
