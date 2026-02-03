# Skill: pydparser-assessment Technical Extraction
- **Logic**: Uses `ResumeParser` to identify job designations and technical skills.
- **Input**: Accepts raw Job Description text via stdin.
- **Output**: Returns a JSON list containing the designation and up to 5 prioritized skills.
- **Constraint**: Optimized for standard HR entities; may require fallback if IT-specific terminology is highly non-standard.
# Skill: Standardized Job Parsing
- **Expertise**: Extracting structured metadata from IT job postings using pydparser-assessment.
- **Task**: Identify core entities: Job Title, Location, and Salary Range.
- **Goal**: Convert unstructured text into consistent JSON objects for downstream comparison.
- **Constraint**: Prioritize built-in pydparser-assessment extraction patterns over custom regex.
