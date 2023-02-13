import datetime

def get_displayed_test_case(example_test_case: str, indent: str, comment: str) -> str:
    example_test_case_list = [case.replace("\n", " ") for case in example_test_case]
    example_test_case_display = "\n".join([f"{indent}{comment} {case}" for case in example_test_case_list])

    return example_test_case_display

def get_displayed_time() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d")
