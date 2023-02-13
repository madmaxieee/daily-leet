from pathlib import Path

from ..languages import LangSlugs
from .rust import create_rust_file
from .cpp import create_cpp_file
from .python3 import create_python3_file
from .golang import create_go_file

def create_files(lang_slug: LangSlugs, title_slug: str, code_snippet: str, example_test_case: str) -> Path:
    file_creator_map = {
        LangSlugs.RUST: create_rust_file,
        LangSlugs.CPP: create_cpp_file,
        LangSlugs.PYTHON3: create_python3_file,
        LangSlugs.GOLANG: create_go_file,
    }

    main_file_path = file_creator_map[lang_slug](title_slug, code_snippet, example_test_case)

    return main_file_path
