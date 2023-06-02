from dataclasses import dataclass

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from claims_analysis_pkg.src.constants import SUMMARIZATION_PROMPT
from claims_analysis_pkg.src.page_processing import Violation


@dataclass
class ClaimSummary:
    """For storing a summary of findings for a claim."""

    filepath: str
    pages_total: int
    pages_queried: int
    pages_flagged: int
    summary: str


def summarize_results(entries: list[Violation], temperature: float = 0) -> str:
    """Given page level results, create a summary of the potential reasons for policy violation."""

    # Extract only the relevant parts of the entries
    simplified_entries = [
        "(page_no={}, issue_desc='{}')".format(entry.page_no, entry.issue_desc)
        for entry in entries
    ]
    entries_str = "Potential violations: [" + ", ".join(simplified_entries) + "]"

    # Send to API for summary
    chat = ChatOpenAI(temperature=temperature, model_name="gpt-3.5-turbo", client=None)
    messages = [
        SystemMessage(content=SUMMARIZATION_PROMPT),
        HumanMessage(content=entries_str),
    ]

    return chat(messages).content
