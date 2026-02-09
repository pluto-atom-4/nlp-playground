import json

import pytest

from skills_extractor_assessment import extract


@pytest.fixture(scope="session", autouse=True)
def setup_ojd_daps_skills():
    """
    Initialize ojd-daps-skills on first test run.

    This fixture handles:
    - Downloading required spaCy NER models
    - Initializing the SkillsExtractor with toy taxonomy
    - Caching models for subsequent test runs
    """
    try:
        # Import here to trigger model downloads
        from ojd_daps_skills.extract_skills.extract_skills import SkillsExtractor

        # Initialize with toy taxonomy to trigger model downloads
        sm = SkillsExtractor(taxonomy_name="toy")

        # Warm up with a simple test
        sm(["test skill"])

        yield
    except Exception as e:
        print(f"Warning: Model initialization had issues: {e}")
        # Continue anyway, tests will handle errors
        yield


class TestExtractContract:
    """Test suite verifying extract() function contract: returns list[str]."""

    def test_extract_returns_list_of_strings(self):
        """
        Verify that extract() returns a list of strings, matching compare_extractors.py expectations.

        The extract() function must return list[str] to be compatible with:
        - compare_extractors.py (json.loads parsing)
        - CI/CD benchmark comparison workflow
        - Multi-engine result aggregation

        Tests with both single string and list inputs to ensure consistent behavior.
        """
        # Test single string input
        job_ad = "Python developer with AWS and Kubernetes experience"
        result = extract(job_ad)

        assert isinstance(result, list), f"Expected list, got {type(result)}"
        assert all(isinstance(item, str) for item in result), (
            "All items must be strings"
        )

        # Test list input
        job_ads = [
            "Communication skills and maths skills",
            "Excel and presentation skills",
        ]
        result_batch = extract(job_ads)

        assert isinstance(result_batch, list), "Batch input should return list"
        assert all(isinstance(item, str) for item in result_batch), (
            "All items must be strings"
        )

        # Verify JSON serializable (required by compare_extractors.py)
        json_str = json.dumps(result)
        assert isinstance(json_str, str), "Result should be JSON-serializable"
