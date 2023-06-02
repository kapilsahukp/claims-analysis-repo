from dataclasses import dataclass

# Added API key:
# OPENAI_API_KEY = "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"

# Number of threads to be used for parallel processing
THREADS = 8

# Ignore all pages that have any of these keywords since they're usually extended coverage pages
GLOBAL_EXCLUDED_KEYWORDS = ["coverage f", "coverage g", "coverage h", "coverage i"]

# Delimiter to determine if answer has a violation
YES_DELIMITER = "YES:"

# Template for agent to query single claims
PAGE_PROCESSING_TEMPLATE = """\
You are an expert flood insurance adjuster and can easily detect if a page tries to \
claim items that are not covered. You know that when an item is claimed it's usually associated \
with a monetary value like RCV, ACV, damages or price. Look for only the following excluded items:
{violation_descriptions}
After each page is fed to you, you will respond with either:
    - 'NONE', if no out of policy items are detected, which is common
    - '{yes_delimiter}', followed by a short summary (1-3 sentences) of the page and how it mentions an out-of-policy item
"""

# Prompt for summarization
SUMMARIZATION_PROMPT = """\
You are an expert flood insurance adjuster responsible for summarizing some of the possible reasons for why a claim may be \
in violation of the policy. You are given possible violations, and the associated page numbers of the violations. \
However, you are aware that sometimes the reasons are false positives. For example, an item may be mentioned in \
the policy but is not being explicitly claimed. Start your response with the sentence 'Possible violations flagged in the claim are:' \
followed by a concise summary of the key violations and their associated page numbers in bullet form. \
Base your answer only on the information that is provided.
"""


# Prompt descriptions and keywords for violation types
@dataclass
class ViolationType:
    name: str
    prompt_desc: str
    keywords: list[str]


ALL_VIOLATION_TYPES = [
    ViolationType(
        name="pools",
        prompt_desc="- pool and pool equipment\n",
        keywords=["pool", "hot tub"],
    ),
    ViolationType(name="patios", prompt_desc="- patios\n", keywords=["patio"]),
    ViolationType(
        name="upper_cabinets",
        prompt_desc="- upper cabinets that were unaffected\n",
        keywords=["cabinets", "cabinetry"],
    ),
]
