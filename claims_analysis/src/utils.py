import logging
import re
from time import time
from typing import Any, Callable

from pypdf import PdfReader


def setup_logging(log_path: str) -> None:
    """Setups logging to save logs in log_path."""

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.FileHandler(log_path, mode="w"), logging.StreamHandler()],
        force=True,

    )


def log_timer(func: Callable) -> Callable:
    """Decorator for logging the time it takes to run a function."""

    def wrap_func(*args: Any, **kwargs: Any) -> Any:
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        logging.info(f"Function {func.__name__!r} executed in {(t2-t1):.2f}s")
        return result

    return wrap_func


def convert_pdf_to_page_list(path: str) -> list[str]:
    """Takes in file path and returns list of string where each string is 1 page."""

    reader = PdfReader(path)
    logging.info(f"Read {path} with {len(reader.pages)} pages")
    pages = [page.extract_text() for page in reader.pages]
    return pages


def words_exist_in_text(keywords: list[str], corpus: str) -> bool:
    """Determines if at least one of the keywords exists standalone in the corpus."""

    pattern = "|".join(r"\b{}\b".format(word) for word in keywords)
    return bool(re.search(pattern, corpus, flags=re.IGNORECASE | re.DOTALL))
