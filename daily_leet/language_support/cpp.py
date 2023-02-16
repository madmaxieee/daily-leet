from pathlib import Path

from .utils import get_displayed_test_case, get_displayed_time, create_lang_dir
from .types import LangSlugs

LANG = LangSlugs.CPP
COMMENT = "//"
INDENT = "    "
BOILERPLATE = f"""// %s {get_displayed_time()}
#include <iostream>

using namespace std;

%s

int main() {{
%s
}}
"""

MAKEFILE = """CC = g++

all: main

main: main.cpp
    $(CC) -o main main.cpp

clean:
    rm main

run: main
    ./main
"""


def create_cpp_file(
    title_slug: str, code_snippet: str, example_test_cases: list[str]
) -> Path:
    example_test_case_display = get_displayed_test_case(
        example_test_cases, INDENT, COMMENT
    )
    code = BOILERPLATE % (title_slug, code_snippet, example_test_case_display)

    lang_dir = create_lang_dir(LANG)

    project_dir = lang_dir / title_slug
    project_dir.mkdir(exist_ok=True)

    main_file_path = project_dir / "main.cpp"

    with open(main_file_path, "w") as f:
        f.write(code)

    with open(project_dir / "makefile", "w") as f:
        f.write(MAKEFILE)

    return main_file_path
