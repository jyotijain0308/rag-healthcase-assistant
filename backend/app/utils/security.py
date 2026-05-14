import re

PROMPT_INJECTION_PATTERNS = [

    r"ignore previous instructions",

    r"ignore all instructions",

    r"reveal system prompt",

    r"show hidden instructions",

    r"act as",

    r"pretend to be",

    r"disable safety",

    r"bypass restrictions",

    r"jailbreak",

    r"developer instructions"
]

HEALTHCARE_UNSAFE_PATTERNS = [

    r"prescribe medication",

    r"exact dosage",

    r"replace my doctor",

    r"diagnose me",

    r"self-medicate",

    r"suicide",

    r"harm myself"
]

def detect_prompt_injection(query: str):

    for pattern in PROMPT_INJECTION_PATTERNS:

        if re.search(
            pattern,
            query,
            re.IGNORECASE
        ):
            print(
                f"[SECURITY ALERT] "
                f"Potential prompt injection: "
                f"{query}"
            )
            return True

    return False


def detect_unsafe_healthcare_query(
    query: str
):

    for pattern in HEALTHCARE_UNSAFE_PATTERNS:

        if re.search(
            pattern,
            query,
            re.IGNORECASE
        ):
            print(
                f"[SECURITY ALERT] "
                f"Potential prompt injection: "
                f"{query}"
            )
            return True

    return False

import re

def is_meaningless_query(query: str):

    if len(query.strip()) < 3:
        return True

    if re.fullmatch(
        r"[a-zA-Z0-9]+",
        query
    ) and len(query) < 5:
        return True

    return False