# import configparser
import json
import logging
import os

import openai
import pandas as pd
from dotenv import load_dotenv

# from src.page_processing import Violation, process_claim_pages
# from src.summarization import ClaimSummary, summarize_results
# from src.utils import log_timer, read_claim, setup_logging

from claims_analysis_pkg.src.page_processing import Violation, process_claim_pages
from claims_analysis_pkg.src.summarization import ClaimSummary, summarize_results
from claims_analysis_pkg.src.utils import log_timer, read_claim, setup_logging

# Create a configparser object
# config = configparser.ConfigParser()

# Specify the path to the config file
# config_file_path = "../../../../../content/gdrive/MyDrive/Colab_Notebooks/config.ini"
config_file_path = "../../../../../content/gdrive/MyDrive/Colab_Notebooks/config.json"

# Read the config file
# config.read(config_file_path)
with open(config_file_path, "r") as file:
    config_data = json.load(file)

# Access the parameters
# os.environ['OPENAI_API_KEY'] = config.get("Parameters", "OPENAI_API_KEY")

# Access the parameters
parameters = config_data["Parameters"]
os.environ['OPENAI_API_KEY'] = parameters["OPENAI_API_KEY"]
print(os.environ['OPENAI_API_KEY'])

# ksahu added to make sure it sets neptune as root directory
abspath = os.path.abspath(__file__)
# dname = os.path.dirname(os.path.dirname(os.path.dirname(abspath)))
# os.chdir(dname)
print("abspath : ", abspath)

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
print("root : ", ROOT_DIR)

# from src.constants import THREADS
from claims_analysis_pkg.src.constants import THREADS

# Setup API key
# load_dotenv(env_path)
# openai.api_key = os.getenv("OPENAI_API_KEY")

@log_timer
def process_single_claim(claim_path: str) -> tuple[list[Violation], ClaimSummary]:
    """Read claim, get violations, and summarization for a single claim."""

    # Read the claim
    pages = read_claim(claim_path)
    # pages = read_claim(os.path.join('claims-analysis', claim_path))  # modified by ksahu

    # Get all violations and the page numbers queried
    entries, pages_queried = process_claim_pages(claim_path, pages, threads=THREADS)

    # Summarize the information for the claim
    summary_text = (
        summarize_results(entries) if len(entries) > 0 else "No violations found."
    )
    logging.info(f"Summary for {claim_path}:\n{summary_text}")

    claim_summary = ClaimSummary(
        filepath=claim_path,
        pages_total=len(pages),
        pages_queried=len(pages_queried),
        pages_flagged=len(entries),
        summary=summary_text,
    )

    return entries, claim_summary


@log_timer
def main(run_id: str, claim_paths: list[str] = []) -> None:
    """
    Processes a list of claims and outputs their entries and summaries to csv files.
    If none are provided then we run on all .pdf files in the claims directory.
    """

    # openai.api_key = open_api_key
    CLAIMS_DIR = config.get("Parameters", "CLAIMS_DIR")
    OUTPUTS_DIR = config.get("Parameters", "LOGS_DIR")
    LOGS_DIR = config.get("Parameters", "OUTPUTS_DIR")

    log_path = os.path.join(LOGS_DIR, run_id + ".log")
    setup_logging(log_path=log_path)
    logging.info(f"Starting run {run_id}...")

    # Get list of all claims in claims directory if paths are not explicitly provided
    if not claim_paths:
        claim_paths = ['/'.join([CLAIMS_DIR, file]) for file in os.listdir(CLAIMS_DIR) if file.endswith(".pdf")]
    logging.info(f"All claims to be processed: {claim_paths}.")

    all_violations: list[Violation] = []
    all_summaries: list[ClaimSummary] = []

    for claim_path in claim_paths:
        entries, summary = process_single_claim(claim_path)
        all_violations.extend(entries)
        all_summaries.append(summary)

    # Save the results
    output_base = os.path.join(OUTPUTS_DIR, run_id)
    pd.DataFrame(all_violations).to_csv(output_base + "_violations.csv", index=False)
    pd.DataFrame(all_summaries).to_csv(output_base + "_summary.csv", index=False)
    logging.info("Done.")


if __name__ == "__main__":
    main(
        run_id="initial_test",
        # open_api_key="",
        # claims_dir=config.get("Parameters", "CLAIMS_DIR"),
        # logs_dir=config.get("Parameters", "LOGS_DIR"),
        # outputs_dir=config.get("Parameters", "OUTPUTS_DIR"),
        # claims_dir="../../../../../content/gdrive/MyDrive/Colab_Notebooks/ksahu_claims",  # added by kapil
        # # claims_dir="ksahu_claims/",  # added by kapil
        # logs_dir="../../../../../content/gdrive/MyDrive/Colab_Notebooks/ksahu_outputs/",  # added by kapil
        # outputs_dir="../../../../../content/gdrive/MyDrive/Colab_Notebooks/ksahu_logs/",  # added by kapil
        claim_paths=[
            "../../../../../content/gdrive/MyDrive/Colab_Notebooks/ksahu_claims/4_956635_Doc1.pdf" # ../../../../../ksahu_claims
            # ,  # Expect to see patio mention on page 11
            # "claims/7_955932_Doc1.pdf",  # Expect to see pool issue on page 140
            # "claims/8_956437_Doc1.pdf",  # Expect to see pool mention on page 38
            # "claims/9_958681_Doc1.pdf",  # Expect to see upper cabinets mention on page 6
            # "claims/10_957336_Doc1.pdf",  # Expect to see upper cabinets mention on page 10
            # "claims/18_956566_Doc1.pdf",  # Expect to see nothing since the claim is compliant
            # "claims/20_958744_Doc1.pdf",  # Expect to see nothing since the claim is compliant
        ]
    )
