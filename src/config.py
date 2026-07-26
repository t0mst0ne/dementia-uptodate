"""Load all configuration from source/ YAML files."""

import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

SOURCE_DIR = Path(__file__).parent.parent / "source"


def _load(filename: str) -> Any:
    return yaml.safe_load((SOURCE_DIR / filename).read_text())


@lru_cache(maxsize=None)
def keywords() -> list[str]:
    data = _load("keywords.yml")
    # Keep compatibility with the original breast-cancer configuration while
    # allowing the project to use its current dementia topic.
    return data.get("dementia_keywords", data.get("breast_cancer_keywords", []))


def keyword_pattern(terms: tuple[str, ...] | None = None) -> re.Pattern:
    """Case-insensitive pattern matching whole terms only.

    Plain substring matching makes short abbreviations catastrophically broad:
    "AD" hits "r(ad)iotherapy", "tau" hits "pla(tau)", "NIA" hits "insom(nia)".
    Alphanumeric lookarounds (rather than \\b) keep hyphenated terms such as
    "p-tau217" and possessives such as "Alzheimer's disease" matchable.
    """
    return _compile_pattern(tuple(terms) if terms is not None else tuple(keywords()))


@lru_cache(maxsize=None)
def _compile_pattern(terms: tuple[str, ...]) -> re.Pattern:
    alts = "|".join(re.escape(t) for t in sorted(terms, key=len, reverse=True))
    return re.compile(rf"(?<![a-z0-9])(?:{alts})(?![a-z0-9])", re.I)


def match_keywords(text: str, terms: list[str] | None = None) -> list[str]:
    """Return configured keywords present in text, in configuration order."""
    pool = terms if terms is not None else keywords()
    pat = keyword_pattern(tuple(pool))
    found = {m.group(0).lower() for m in pat.finditer(text)}
    return [t for t in pool if t.lower() in found]


@lru_cache(maxsize=None)
def drug_groups() -> dict[str, list[str]]:
    return _load("drug_groups.yml")["drug_groups"]


@lru_cache(maxsize=None)
def conference_keywords() -> list[str]:
    return _load("drug_groups.yml")["conference_keywords"]


@lru_cache(maxsize=None)
def search_queries() -> list[str]:
    return _load("search_queries.yml")["search_queries"]


@lru_cache(maxsize=None)
def web_sources() -> list[dict]:
    return _load("web_sources.yml")["sources"]


@lru_cache(maxsize=None)
def http_headers() -> dict[str, str]:
    return _load("web_sources.yml").get("http_headers", {
        "User-Agent": "dementia-uptodate/1.0 (research report collector)",
        "Accept": "application/rss+xml, application/xml, text/xml, text/html",
    })


@lru_cache(maxsize=None)
def twitter() -> dict:
    return _load("twitter.yml")["twitter"]


@lru_cache(maxsize=None)
def journals() -> list[dict]:
    return _load("journals.yml").get("journals", [])


@lru_cache(maxsize=None)
def crossref_email() -> str:
    return _load("journals.yml").get("crossref_email", "")
