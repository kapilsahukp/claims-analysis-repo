import logging
import re
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from typing import Optional

from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseMessage, HumanMessage, SystemMessage

from src.constants import (
    ALL_VIOLATION_TYPES,
    GLOBAL_EXCLUDED_KEYWORDS,
    PAGE_PROCESSING_TEMPLATE,
    YES_DELIMITER,
    ViolationType,
)
from src.utils import words_exist_in_text


@dataclass
class Violation:
    """For storing individual occurences of violations."""

    filepath: str
    page_no: int
    issue_desc: str


class PageProcessor:
    """General processor for catching violations within single pages."""

    def __init__(
        self,
        relevant_violation_types: list[ViolationType] = ALL_VIOLATION_TYPES,
        temperature: float = 0,
    ):
        self.chat = ChatOpenAI(
            temperature=temperature, model_name="gpt-3.5-turbo", client=None
        )

        # Construct the base system message from the relevant violation types and save the keywords
        keywords_set: set[str] = set()
        violation_prompts: list[str] = []

        for violation_type in relevant_violation_types:
            violation_prompts.append(violation_type.prompt_desc)
            keywords_set.update(violation_type.keywords)

        self.required_keywords = list(keywords_set)
        self.sys_message = SystemMessage(
            content=PAGE_PROCESSING_TEMPLATE.format(
                violation_descriptions="".join(violation_prompts),
                yes_delimiter=YES_DELIMITER,
            )
        )

    def meets_prefilter_criteria(self, page_text: str) -> bool:
        """Basic filter for ruling out pages that don't need to be queried."""

        # Terms that must be present to consider page
        if not words_exist_in_text(self.required_keywords, page_text):
            return False

        # Terms that must not be present to consider page; mostly terms in extended coverage doc
        return not words_exist_in_text(GLOBAL_EXCLUDED_KEYWORDS, page_text)

    def _process_response(self, raw_response: BaseMessage) -> Optional[str]:
        """Processes the response from LLM and returns a reason if there is one."""

        if raw_response.content.startswith(YES_DELIMITER):
            reason = raw_response.content.split(YES_DELIMITER)[-1].strip()
            return reason

        return None

    def process_page(self, page_text: str) -> Optional[str]:
        """Takes in a page and runs the LLM and returns a violation reason if there is one."""

        messages = [self.sys_message, HumanMessage(content=page_text)]
        response = self.chat(messages)

        return self._process_response(response)


def process_claim_pages(path: str, pages: list[str], threads: int = 1) -> tuple[list[Violation], list[int]]:
    """Processes pages and returns a list of violations and page numbers that were processed."""

    logging.info(f"Starting processing for claim {path} with {threads} threads...")

    processor = PageProcessor()
    pages_processed: list[int] = []
    entries: list[Violation] = []
    page_no_to_future: dict[int, Future[Optional[str]]] = {}

    # Submit the queries to processor
    with ThreadPoolExecutor(max_workers=threads) as exec:
        for page_no, page in enumerate(pages, 1):
            if processor.meets_prefilter_criteria(page):
                pages_processed.append(page_no)
                page_no_to_future[page_no] = exec.submit(processor.process_page, page)

    # Collect the results
    for page_no, future in page_no_to_future.items():
        if (reason := future.result()) is not None:
            entries.append(Violation(filepath=path, page_no=page_no, issue_desc=reason))
            logging.info(f"Found violation on page {page_no} with reason: {reason}")

    logging.info(
        f"Finished {path}. Processed {len(pages_processed)} pages out of {len(pages)}: {pages_processed}"
    )

    return entries, pages_processed
