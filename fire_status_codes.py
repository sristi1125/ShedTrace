"""
FDNY inspection status codes -> plain English.
Based on the actual values found in fire_safety.csv (LAST_INSP_STAT).
"""

FIRE_STATUS_LABELS = {
    "APPROVAL": "Passed inspection",
    "NOT APPROVAL(W/REASON)": "Failed inspection (reason noted)",
    "NOT APPROVAL(VIO)": "Failed inspection (violation issued)",
    "NOV(HOLD)": "Violation notice issued — compliance hold in place",
    "NOV(NO HOLD)": "Violation notice issued — no hold",
    "NOV AND VIO(NOV HOLD)": "Violation notice and citation issued — compliance hold in place",
    "NOV AND VIO(NOV NO HOLD)": "Violation notice and citation issued — no hold",
}


def describe_fire_status(code) -> str:
    """Return a readable label for an FDNY inspection status, falling
    back to showing the raw text if it's not in our table."""
    if code is None:
        return "Status not recorded"
    code_str = str(code).strip()
    if code_str.lower() == "nan" or code_str == "":
        return "Status not recorded"
    return FIRE_STATUS_LABELS.get(code_str, code_str)