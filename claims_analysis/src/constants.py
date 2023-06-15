from dataclasses import dataclass
from enum import Enum
from typing import Optional

# Number of threads for processing pages within a single claim
THREADS = 8

# Ignore all pages that have any of these keywords since they're usually extended coverage pages
GLOBAL_EXCLUDED_KEYWORDS = ["coverage f", "coverage g", "coverage h", "coverage i"]

# Delimiter to determine if answer has a violation
YES_DELIMITER = "YES:"

# Template for agent to process single claims

# Excluded properties
EXCLUDED_ITEMS_TEMPLATE = """\
You are an expert flood insurance adjuster and can accurately detect if a page tries to \
claim items that are not covered. Your job is the look for the following excluded items:
{violation_descriptions}
Remember your job is to detect ONLY these specific items and ignore all other possible \
violations. Pages will be fed to you one at a time and you will try to determine if there \
are item(s) from the above list being claimed. This means:
    - There's usually monetary value like RCV, ACV, damages, or price associated with the item
    - Just mentioning the item isn't enough, for example statements like "the policyholder \
did not purchase coverage for pools" or "pool and patio damages are not covered" are not \
violations and should not be flagged because no items are incorrectly being claimed

After each page of the claim is fed to you, think about if there's a possible violation or if the items are \
being mentioned but not claimed (e.g. stated as not being covered). Finally, respond with \
either:
    - 'NONE', if no out-of-policy item violation is detected, which is common
    - '{yes_delimiter}', followed by a short summary (1-3 sentences) of the page and which \
of the items above are being claimed. Omit any monetary values.
"""

# Use of RCV with non-covered property types
RCV_PROPERTY_TEMPLATE = """\
You are an expert flood insurance adjuster. Your role is to identify a specific type of violation, which is when RCV is \
used to claim ineligible property types. Look for only the following ineligible property types:
{violation_descriptions}
Only flag these violations and nothing else. After each page of the claim is fed to you, you will respond with either:
    - 'NONE', if none of the above violations are detected, which is common
    - '{yes_delimiter}', followed by a short summary (1-3 sentences) of the page and how it mentions a \
violation from the above list. Omit any monetary values.
Remember your job is to detect ONLY those specific violations and nothing else.
"""

# Pair clause template
PAIR_CLAUSE_TEMPLATE = """\
You are an expert flood insurance adjuster. \
One common problem is when upper cabinets are claimed, as this may be a violation of the pair and set clause. \
Ignore mentions of lower cabinets and lower cabinetry from your analysis as this by itself is not a policy violation. \
Look for the following:
{violation_descriptions}
After each page of the claim is fed to you, you will respond with either:
    - 'NONE', if upper cabinets are not being claimed, which is common
    - '{yes_delimiter}', followed by a short summary (1-3 sentences) of the page and how it claims \
upper cabinets. Omit any monetary values.
Remember your job is to detect ONLY those specific violations and nothing else.
"""

# Prompt for summarization
SUMMARIZATION_PROMPT = """\
You are an expert flood insurance adjuster responsible for summarizing some of the possible reasons for why a claim may be \
in violation of the policy. You are given possible violations, and the associated page numbers of the violations. \
However, you are aware that sometimes the reasons are false positives. For example, an item may be mentioned in \
the policy but is not being explicitly claimed. Start your response with the sentence 'Possible violations flagged in the claim are:' \
followed by a concise summary of the key violations and their associated page numbers in bullet form. \
Base your answer only on the information that is provided and omit any dollar amounts in the summary.
"""


# Optional coverage enum. If the policyholder bought these then the associated violation types do not apply.
class ExtendedCoverage(Enum):
    CoverageF = "Basement Contents"
    CoverageG = "Pool Repair and Refill"
    CoverageH = "Unattached Structure(s)"
    CoverageI = "Temporary Living Expenses"


# Prompt descriptions and keywords for violation types
@dataclass
class ViolationType:
    name: str
    prompt_desc: str
    keywords: list[str]
    extended_coverage: Optional[ExtendedCoverage]


EXCLUDED_ITEMS_VIOLATION_TYPES = [
    ViolationType(
        name="pools",
        prompt_desc="pool and pool equipment",
        keywords=["pool", r"hot( |\n|)tub"],
        extended_coverage=ExtendedCoverage.CoverageG,
    ),
    ViolationType(
        name="patios", prompt_desc="patios", keywords=["patio"], extended_coverage=None
    ),
]

RCV_PROPERTY_VIOLATION_TYPES = [
    ViolationType(
        name="secondary_property_rcv",
        prompt_desc="when the property or risk is a secondary property",
        keywords=["secondary"],
        extended_coverage=None,
    ),
    ViolationType(
        name="shed_rcv",
        prompt_desc="when an unattached shed is being claimed with RCV",
        keywords=[r"shed.*rcv", r"rcv.*shed"],
        extended_coverage=ExtendedCoverage.CoverageH,
    ),
]

PAIR_CLAUSE_VIOLATION_TYPES = [
    ViolationType(
        name="upper_cabinets",
        prompt_desc="upper cabinets that were unaffected and is associated with monetary value. Ignore lower cabinets.",
        keywords=[
            r"(cabinets|cabinetry)[^a-zA-Z]*upper",
            r"upper[^a-zA-Z]*(cabinets|cabinetry)",
        ],
        extended_coverage=None,
    ),
]
