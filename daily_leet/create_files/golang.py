from pathlib import Path

from .utils import get_displayed_test_case, get_displayed_time, create_lang_dir
from ..languages import LangSlugs

LANG = LangSlugs.GOLANG
COMMENT = "//"
INDENT = "    "
BOILERPLATE = f"""// %s {get_displayed_time()}

package main

import "fmt"

%s

func main() {{
%s
}}
"""


def create_go_file(title_slug: str, code_snippet: str, example_test_case: str) -> Path:
    example_test_case_display = get_displayed_test_case(example_test_case, INDENT, COMMENT)
    code = BOILERPLATE % (title_slug, code_snippet, example_test_case_display)

    lang_dir = create_lang_dir(LANG)

    project_dir = lang_dir / title_slug
    project_dir.mkdir(exist_ok=True)

    main_file_path = project_dir / "main.go"

    with open(main_file_path, "w") as f:
        f.write(code)

    return main_file_path
