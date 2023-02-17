import typer

from pathlib import Path
import subprocess
import re

from .utils import get_displayed_time, create_lang_dir, get_displayed_test_case
from .types import LangSlugs

LANG = LangSlugs.RUST
COMMENT = "//"
INDENT = "    "
BOILERPLATE = f"""// %s {get_displayed_time()}

struct Solution;

%s

fn main() {{
%s
}}
"""


def create_rust_file(
    title_slug: str, code_snippet: str, example_test_cases: list[str]
) -> Path:
    try:
        parsed_example_test_cases = parse_example_test_cases(
            code_snippet, example_test_cases
        )
    except Exception as e:
        typer.echo(f"Error parsing example test cases for {title_slug}")
        typer.echo("Rolling back to default behavior...")
        parsed_example_test_cases = get_displayed_test_case(
            example_test_cases, INDENT, COMMENT
        )

    code = BOILERPLATE % (title_slug, code_snippet, parsed_example_test_cases)

    lang_dir = create_lang_dir(LANG)

    # run cargo new to create a new project
    subprocess.run(["cargo", "new", title_slug], cwd=lang_dir)

    main_file_path = lang_dir / title_slug / "src" / "main.rs"

    # write code to src/main.rs
    with open(main_file_path, "w") as f:
        f.write(code)

    return main_file_path


def parse_example_test_cases(code_snippet: str, example_test_cases: list[str]) -> str:
    # find the name and data type of each input and create a variable for it

    variable_names: list[str] = []
    variable_types: list[str] = []
    function_name = ""
    for line in code_snippet.splitlines():
        if line.strip().startswith("pub fn"):
            function_name = re.findall(r"fn (\w+)\(", line)[0]
            variables = re.findall(r"\((.*?)\)", line)[0].split(", ")
            variable_names = list(map(lambda x: x.split(": ")[0], variables))
            variable_types = list(map(lambda x: x.split(": ")[1], variables))
            break

    variable_values = list(map(lambda x: x.split("\n"), example_test_cases))

    call_function = (
        f"let result = Solution::{function_name}({', '.join(list(variable_names))});"
    )
    print_result = f'println!("{{:?}}", result);'

    lines = []
    for values in variable_values:
        for var_name, var_type, var_value in zip(
            variable_names, variable_types, values
        ):
            lines.append(f"let {var_name} = {create_variable(var_type, var_value)};")

        lines.append(call_function)
        lines.append(print_result)
        lines.append("")

    return "\n".join(map(lambda line: (INDENT if line else "") + line, lines))


def create_variable(var_type: str, var_value: str) -> str:
    number_types = [
        "i8",
        "i16",
        "i32",
        "i64",
        "i128",
        "isize",
        "u8",
        "u16",
        "u32",
        "u64",
        "u128",
        "usize",
        "f32",
        "f64",
    ]
    if var_type in number_types:
        return var_value

    if var_type == "String":
        return f"{var_value}.to_string()"

    # match for Vec<{number_type}>
    if re.match(r"Vec<\w+>", var_type):
        vec_type = re.findall(r"Vec<(\w+)>", var_type)[0]
        return f"vec!{create_variable(vec_type, var_value)}".replace(",", ", ")

    raise NotImplementedError(f"Type {var_type} not implemented")
