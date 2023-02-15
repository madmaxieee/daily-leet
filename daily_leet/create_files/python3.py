from pathlib import Path

from .utils import get_displayed_test_case, get_displayed_time

LANG = "python3"
COMMENT = "#"
INDENT = "    "
BOILERPLATE = f"""# %s {get_displayed_time()}

%s

if __name__ == "__main__":
%s
"""

def create_python3_file(title_slug: str, code_snippet: str, example_test_case: str) -> Path:
    example_test_case_display = get_displayed_test_case(example_test_case, INDENT, COMMENT)
    code = BOILERPLATE % (title_slug, code_snippet, example_test_case_display)

    lang_dir = Path(LANG)
    lang_dir.mkdir(exist_ok=True)

    main_file_path = lang_dir / f"{title_slug}.py"

    with open(main_file_path, "w") as f:
        f.write(code)

    return main_file_path
