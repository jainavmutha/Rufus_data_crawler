import re

def extract_info_from_prompt(instructions):
    """
    Extract relevant information from the instructions to decide what to scrape.
    This could include extracting the domain and relevant sections (like HR, FAQ, etc.).
    """
    domain = "https://www.sfgov.com"  # Default domain (can be customized or extended)
    sections = []

    # Example: Look for HR, benefits, employment, etc., in the prompt
    if re.search(r"\bHR\b", instructions, re.IGNORECASE):
        sections.append("hr")
    if re.search(r"\bbenefits\b", instructions, re.IGNORECASE):
        sections.append("benefits")
    if re.search(r"\bemployment\b", instructions, re.IGNORECASE):
        sections.append("employment")
    if re.search(r"\bfaq\b", instructions, re.IGNORECASE):
        sections.append("faq")
    if re.search(r"\bcontact\b", instructions, re.IGNORECASE):
        sections.append("contact")

    # Return the domain and the list of relevant sections
    return domain, sections
