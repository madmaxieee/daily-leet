import typer

from typing import Mapping
import re
import requests
import json
import datetime

from .constants import LEETCODE_HOST
from .languages import LangSlugs


def set_cookie(session: requests.Session):
    session.get(LEETCODE_HOST)
    return


def get_code_snippets_map(
    session: requests.Session, title_slug: str
) -> Mapping[LangSlugs, str]:
    query = """
query questionEditorData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    questionFrontendId
    codeSnippets {
      lang
      langSlug
      code
    }
  }
}
    """
    variables = {"titleSlug": title_slug}
    data = {"query": query, "variables": variables}
    res = session.post(f"{LEETCODE_HOST}/graphql/", json=data)
    json = res.json()
    if "errors" in json:
        raise Exception(json["errors"])

    code_snippets = json["data"]["question"]["codeSnippets"]
    code_snippet_map = {}
    for snippet in code_snippets:
        code_snippet_map[LangSlugs(snippet["langSlug"])] = snippet["code"]

    return code_snippet_map


def get_code_snippet(session: requests.Session, title_slug: str, lang_slug: LangSlugs):
    try:
        code_snippets_map = get_code_snippets_map(session, title_slug)
    except Exception as e:
        raise typer.BadParameter(f"Failed to get code snippets for the question: {title_slug}, {e}")

    code_snippet = code_snippets_map[lang_slug.value]
    return code_snippet


def get_content(session: requests.Session, title_slug: str) -> str:
    query = """
query questionContent($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    content
  }
}
    """
    variables = {"titleSlug": title_slug}
    data = {"query": query, "variables": variables}
    res = session.post(f"{LEETCODE_HOST}/graphql/", json=data)
    json = res.json()
    if "errors" in json:
        raise Exception(json["errors"])

    return json["data"]["question"]["content"]

def get_example_test_cases(session: requests.Session, title_slug: str) -> str:
    query = """
query consolePanelConfig($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    questionFrontendId
    questionTitle
    exampleTestcaseList
  }
}
    """
    variables = {"titleSlug": title_slug}
    data = {"query": query, "variables": variables}
    res = session.post(f"{LEETCODE_HOST}/graphql/", json=data)
    json = res.json()

    if "errors" in json:
        raise Exception(json["errors"])
    
    return json["data"]["question"]["exampleTestcaseList"]

def get_daily_challenge_title_slug(session: requests.Session) -> str:
    res = session.get(f"{LEETCODE_HOST}/problemset/all/")
    html = res.text

    # match for the json data between <script id="__NEXT_DATA__" type="application/json"> and </script>
    pattern = r"<script id=\"__NEXT_DATA__\" type=\"application\/json\">(.*)<\/script>"
    match = re.search(pattern, html)
    if match:
        json_data = match.group(1)
    else:
        raise Exception("Failed to find Next.js data on page")

    # parse json data
    data = json.loads(json_data)

    queries = data["props"]["pageProps"]["dehydratedState"]["queries"]

    challenges = None
    for item in queries:
        if item["queryKey"][0] == "dailyCodingQuestionRecords":
            challenges = item["state"]["data"]["dailyCodingChallengeV2"]["challenges"]
            break

    if challenges == None:
        raise Exception("Failed to find challenges")

    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    for challenge in challenges:
        if challenge["date"] == today:
            return challenge["question"]["titleSlug"]
      
    raise Exception("Failed to find challenge for today")


