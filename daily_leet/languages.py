from enum import Enum

# create a enum class for languages
class LangOptions(str, Enum):
    PYTHON = "python"
    PY = "python"

    CPP = "cpp"
    C_PLUS_PLUS = "c++"

    GO = "go"
    GOLANG = "golang"

    RUST = "rust"

class LangSlugs(str, Enum):
    CPP = "cpp"
    JAVA = "java"
    PYTHON = "python"
    PYTHON3 = "python3"
    C = "c"
    CSHARP = "csharp"
    JAVASCRIPT = "javascript"
    RUBY = "ruby"
    SWIFT = "swift"
    GOLANG = "golang"
    SCALA = "scala"
    KOTLIN = "kotlin"
    RUST = "rust"
    PHP = "php"
    TYPESCRIPT = "typescript"
    RACKET = "racket"
    ERLANG = "erlang"
    ELIXIR = "elixir"
    DART = "dart"

def to_lang_slug(language: LangOptions) -> LangSlugs:
    LANG_SLUG_MAP = {
        LangOptions.PYTHON: LangSlugs.PYTHON3,
        LangOptions.PY: LangSlugs.PYTHON3,

        LangOptions.CPP: LangSlugs.CPP,
        LangOptions.C_PLUS_PLUS: LangSlugs.CPP,

        LangOptions.GO: LangSlugs.GOLANG,
        LangOptions.GOLANG: LangSlugs.GOLANG,

        LangOptions.RUST: LangSlugs.RUST,
    }

    return LANG_SLUG_MAP[language]