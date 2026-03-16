import re


def extract_links(html: str) -> list[dict[str, str]]:
    """
    Extract all links from the given HTML string.

    Args:
        html (str): HTML content to analyze

    Returns:
        list[dict]: A list of dictionaries where each dictionary contains:
            - 'url': the href attribute value
            - 'title': the title attribute value (or None if not present)
            - 'text': the text between <a> and </a> tags
    """

    # TODO: Implement a regular expression pattern to extract links from HTML.
    # The pattern should capture three groups:
    # 1. The URL (href attribute value)
    # 2. The title attribute (which might not exist)
    # 3. The link text (content between <a> and </a> tags)
    pattern = r'<a\shref=\"([^\"]+)\"(?:\s+[^>]*title=\"([^\"]+)\")?>(.*?)</a>'

    links = []

    # TODO: Use re.finditer to find all matches of the pattern in the HTML
    # For each match, extract the necessary information and create a dictionary
    # Then append that dictionary to the 'links' list
    for match in re.finditer(pattern, html, re.DOTALL | re.IGNORECASE):
        url = match.group(1)
        title = match.group(2) if match.group(2) else None
        text = re.sub(r'\s+', ' ', match.group(3).strip())  # Normalize whitespace in link text

        links.append({"url": url, "title": title, "text": text})

    return links
