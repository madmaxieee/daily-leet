from pathlib import Path
import subprocess

from .utils import get_displayed_test_case, get_displayed_time

LANG = "rust"
COMMENT = "//"
INDENT = "    "
BOILERPLATE = f"""// %s {get_displayed_time}

struct Solution;

%s

fn main() {{
%s
}}
"""


def create_rust_file(title_slug: str, code_snippet: str, example_test_case: str) -> Path:
    example_test_case_display = get_displayed_test_case(example_test_case, INDENT, COMMENT)
    code = BOILERPLATE % (title_slug, code_snippet, example_test_case_display)

    lang_dir = Path(LANG)
    lang_dir.mkdir(exist_ok=True)

    # run cargo new to create a new project
    subprocess.run(["cargo", "new", title_slug], cwd=lang_dir)

    main_file_path = lang_dir / title_slug / "src" / "main.rs"

    # write code to src/main.rs
    with open(main_file_path, "w") as f:
        f.write(code)

    return main_file_path

