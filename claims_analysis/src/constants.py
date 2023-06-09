from dataclasses import dataclass
from enum import Enum
from typing import Optional

# Specify the path to the config file
# GDRIVE_CONFIG_FILE_PATH = "../../../../../content/gdrive/MyDrive/Claims_Analysis_Directory/config.json"
GDRIVE_CONFIG_FILE_PATH = "/MyDrive/Claims_Analysis_Directory/config.json"

# Number of threads for processing pages within a single claim
THREADS = 8

# Ignore all pages that have any of these keywords since they're usually extended coverage pages
GLOBAL_EXCLUDED_KEYWORDS = ["coverage f", "coverage g", "coverage h", "coverage i"]

# Delimiter to determine if answer has a violation
YES_DELIMITER = "YES:"

# Template for agent to process single claims

# Excluded properties
EXCLUDED_ITEMS_TEMPLATE = """\
You are an expert flood insurance adjuster and can easily detect if a page tries to \
claim items that are not covered. You know that when an item is claimed it's usually associated \
with a monetary value like RCV, ACV, damages or price. Look for only the following excluded items:
{violation_descriptions}
Only flag these out-of-policy items and nothing else. After each page is fed to you, you will respond with either:
    - 'NONE', if none of the out-of-policy items above are detected, which is common
    - '{yes_delimiter}', followed by a short summary (1-3 sentences) of the page and how it mentions an \
        out-of-policy item from the above list
Remember your job is to detect ONLY those specific items and nothing else.
"""

# Use of RCV with non-covered property types
RCV_PROPERTY_TEMPLATE = """\
You are an expert flood insurance adjuster. Your role is to identify a specific type of violation, which is when RCV is \
used to claim ineligible property types. Look for only the following ineligible property types:
{violation_descriptions}
Only flag these violations and nothing else. After each page is fed to you, you will respond with either:
    - 'NONE', if none of the above violations are detected, which is common
    - '{yes_delimiter}', followed by a short summary (1-3 sentences) of the page and how it mentions a \
        violation from the above list
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
    ViolationType(
        name="upper_cabinets",
        prompt_desc="upper cabinets and cabinetry that are associated with monetary value. Only upper cabinets and not any other type of cabinetry",
        keywords=[r"(cabinets|cabinetry).*upper", r"upper.*(cabinets|cabinetry)"],
        extended_coverage=None,
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
