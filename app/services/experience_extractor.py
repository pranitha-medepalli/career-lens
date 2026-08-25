import re
from datetime import datetime


def estimate_experience(text: str):

    text = text.lower()

    patterns = [

        r"(\d+)\+?\s+years?\s+of\s+experience",

        r"experience\s*[:\-]?\s*(\d+)\+?\s+years?"
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:

            return int(match.group(1))

    return 0