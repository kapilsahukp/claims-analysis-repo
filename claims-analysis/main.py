from claims_analysis.claims_processing import process_claims
from claims_analysis.constants import ExtendedCoverage

if __name__ == "__main__":
    process_claims(
        is_cloud_run=False,
        config_data_parameters={
            "OPENAI_API_KEY": "",      # Will be set during cloud run
            "CLAIMS_DIR": "claims/",   # Will be set during cloud run
            "LOGS_DIR": "logs/",       # Will be set during cloud run
            "OUTPUTS_DIR": "outputs/"  # Will be set during cloud run
        },
        run_id="initial_test",
        claim_paths=[
            "claims/2_958940_Doc1.pdf",  # Expect to see secondary property on page 2 and RCV on page 3
            "claims/4_956635_Doc1.pdf",  # Expect to see patio mention on page 11
            # "claims/7_955932_Doc1.pdf",  # Expect to see pool issue on page 140
            # "claims/8_956437_Doc1.pdf",  # Expect to see pool mention on page 38
            # "claims/9_958681_Doc1.pdf",  # Expect to see upper cabinets mention on page 6
            # "claims/10_957336_Doc1.pdf",  # Expect to see upper cabinets mention on page 10
            # "claims/14_954806_Doc1.pdf",  # Expect to see shed with non-zero RCV on page 18
            # "claims/18_956566_Doc1.pdf",  # Expect to see nothing since the claim is compliant
            # "claims/20_958744_Doc1.pdf",  # Expect to see nothing since the claim is compliant
        ],
        # TODO (wliao): this info plus property / occupancy type should come directly from policyDB.
        extended_coverage_dict={
            "claims/4_956635_Doc1.pdf": [
                ExtendedCoverage.CoverageH,
                ExtendedCoverage.CoverageI,
            ]
        },
    )
