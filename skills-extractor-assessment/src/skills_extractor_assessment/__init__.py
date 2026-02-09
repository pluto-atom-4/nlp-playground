from ojd_daps_skills.extract_skills.extract_skills import SkillsExtractor


# Global cache for the extractor instance
_extractor_cache = {}


def _get_extractor(taxonomy_name="toy"):
    """
    Get or initialize a SkillsExtractor instance with lazy loading and caching.

    Args:
        taxonomy_name (str): Name of taxonomy to use (default: "toy")

    Returns:
        SkillsExtractor: Initialized extractor instance

    Raises:
        Exception: If initialization fails
    """
    if taxonomy_name not in _extractor_cache:
        _extractor_cache[taxonomy_name] = SkillsExtractor(taxonomy_name=taxonomy_name)
    return _extractor_cache[taxonomy_name]


def extract(text):
    """
    Extract skills from job description text using ojd-daps-skills framework.

    Args:
        text (str or list): Job description text or list of job descriptions

    Returns:
        list: List of extracted skill strings, aligned with compare_extractors.py format

    Note:
        On first call, this may download required spaCy models and taxonomy data.
        Subsequent calls will use cached models.
    """
    try:
        # Get or initialize the extractor
        sm = _get_extractor(taxonomy_name="toy")

        # Handle both single strings and lists of strings
        if isinstance(text, str):
            job_ads = [text]
        else:
            job_ads = text if isinstance(text, list) else [str(text)]

        # Skip empty inputs
        if not job_ads or all(not ad or not str(ad).strip() for ad in job_ads):
            return []

        # Extract skills from all job ads
        job_ads_with_skills = sm(job_ads)

        # Aggregate all extracted skills
        all_skills = []
        for job_ad_doc in job_ads_with_skills:
            # Extract mapped skills (these are normalized to the toy taxonomy)
            if hasattr(job_ad_doc._, "mapped_skills") and job_ad_doc._.mapped_skills:
                mapped_skills = job_ad_doc._.mapped_skills

                # Handle different possible structures of mapped_skills
                if isinstance(mapped_skills, dict):
                    # If it's a dict, extract all skill values
                    for key, values in mapped_skills.items():
                        if isinstance(values, list):
                            all_skills.extend([str(s) for s in values if s])
                        else:
                            if values:
                                all_skills.append(str(values))
                elif isinstance(mapped_skills, list):
                    # If it's already a list, extend directly
                    all_skills.extend([str(s) for s in mapped_skills if s])
                else:
                    # If it's a single value, append it
                    if mapped_skills:
                        all_skills.append(str(mapped_skills))

            # Fallback: Extract skill spans if mapped_skills is empty
            if not all_skills and hasattr(job_ad_doc._, "skill_spans"):
                skill_spans = job_ad_doc._.skill_spans
                if skill_spans:
                    all_skills.extend([span.text for span in skill_spans if span.text])

        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in all_skills:
            if skill and skill.lower() not in seen:
                seen.add(skill.lower())
                unique_skills.append(skill)

        return unique_skills if unique_skills else []

    except Exception as e:
        # Return error message as list for consistency with compare_extractors.py

        error_msg = f"Error: {str(e)}"
        return [error_msg]
