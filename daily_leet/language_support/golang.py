from pathlib import Path
import re

from .utils import get_displayed_test_case, get_displayed_time, create_lang_dir
from .types import LangSlugs

LANG = LangSlugs.GOLANG
COMMENT = "//"
INDENT = "\t"
NULL = "nil"
BOILERPLATE = f"""// %s {get_displayed_time()}

package main

import (
    "fmt"
)

%s

func main() {{
%s
}}
"""

CONSTRUCTORS = {
    "*TreeNode": {
        "input_type": "[]int",
        "function_name": "makeTree",
        "code": """
func makeTreeNode(data []int) *TreeNode {
	root := &TreeNode{Val: data[0]}
	data = data[1:]
	queue := []*TreeNode{root}

	nodes := make([]*TreeNode, len(data))
	for i, v := range data {
		if v == NIL_NODE {
			nodes[i] = nil
		} else {
			nodes[i] = &TreeNode{Val: v}
		}
	}

	var curNode, leftNode, rightNode *TreeNode

	for len(queue) > 0 && len(data) > 0 {
		curNode = shift(&queue)
		leftNode = shift(&nodes)
		rightNode = shift(&nodes)

		if leftNode != nil {
			curNode.Left = leftNode
			queue = append(queue, leftNode)
		}
		if rightNode != nil {
			curNode.Right = rightNode
			queue = append(queue, rightNode)
		}
	}

	return root
}
""",
    }
}


def create_go_file(
    title_slug: str, code_snippet: str, example_test_cases: list[str]
) -> Path:
    injected_code_snippet = inject_constructors(code_snippet)
    parsed_example_test_cases = parse_example_test_cases(
        code_snippet, example_test_cases
    )
    code = BOILERPLATE % (title_slug, injected_code_snippet, parsed_example_test_cases)
    # replace "    " with INDENT
    code = code.replace("    ", INDENT)

    lang_dir = create_lang_dir(LANG)

    project_dir = lang_dir / title_slug
    project_dir.mkdir(exist_ok=True)

    main_file_path = project_dir / "main.go"

    with open(main_file_path, "w") as f:
        f.write(code)

    return main_file_path


def parse_example_test_cases(code_snippets: str, example_test_cases: list[str]) -> str:
    # find the name and data type of each input and create a variable for it

    variable_names: list[str] = []
    variable_types: list[str] = []
    function_name = ""
    for line in code_snippets.splitlines():
        if line.strip().startswith("func"):
            function_name = line.split(" ")[1]
            variables = line.split("(")[1].split(")")[0].split(", ")
            variable_names = list(map(lambda x: x.split(" ")[0], variables))
            variable_types = list(map(lambda x: x.split(" ")[1], variables))
            break

    variable_values = list(map(lambda x: x.split("\n"), example_test_cases))

    call_function = f"result := {function_name}({', '.join(list(variable_names))})"
    print_result = "fmt.Println(result)"

    lines = []
    for values in variable_values:
        for name, type_, value in zip(variable_names, variable_types, values):
            lines.append(f"{name} := {create_variable(type_, value)}")
        lines.append(call_function)
        lines.append(print_result)
        lines.append("")

    return "\n".join(map(lambda line: (INDENT if line else "") + line, lines))


def create_variable(var_type: str, var_value: str) -> str:
    # replace "null" with NULL
    var_value = var_value.replace("null", NULL)

    simple_types = ["int", "float64", "string", "bool"]
    if var_type in simple_types:
        return var_value

    # create variable of array type
    if re.match(r"\[\](\w+)", var_type):
        # strip brackets from the value
        var_value = var_value[1:-1].replace(",", ", ")
        return f"{var_type}{{{var_value}}}"

    # create variable of special types
    if var_type in CONSTRUCTORS:
        constructor = CONSTRUCTORS[var_type]["function_name"]
        constructor_input_type = CONSTRUCTORS[var_type]["input_type"]
        constructor_input = create_variable(constructor_input_type, var_value)
        return f"{constructor}({constructor_input})"

    raise NotImplementedError(f"Type {var_type} not implemented")


def inject_constructors(code_snippet: str) -> str:
    # extract the commented code from the code snippet
    commented_code_blocks = re.findall(
        r"\/\*\*\n(.*) \*\/", code_snippet, flags=re.DOTALL
    )
    # if there is no commented code, no special constructor are needed
    if not commented_code_blocks:
        return code_snippet

    type_definition = commented_code_blocks[0]
    type_def_start = type_definition.find("type ")
    # drop everything before the type definition
    type_definition = type_definition[type_def_start:]
    # remove " * " before each line
    type_definition = "\n".join(
        map(lambda line: re.sub(r"^ \* ", "", line), type_definition.splitlines())
    )

    struct_name = re.findall(r"type (\w+) struct", type_definition)[0]

    constructor_code = CONSTRUCTORS["*" + struct_name]["code"]

    code_snippet = re.sub(r"\/\*\*.*\*\/", "", code_snippet, flags=re.DOTALL)
    code_snippet = type_definition + "\n" + constructor_code + "\n" + code_snippet

    return code_snippet
