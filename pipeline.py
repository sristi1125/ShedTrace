"""
ShedTrace data pipeline.
"""

import pandas as pd
from datetime import datetime
from complaint_codes import describe_complaint_category

DATA_DIR = "data/"

SHED_FILE = DATA_DIR + "sidewalk_sheds.csv"
SHED_BIN_COL = "BIN Number"
SHED_ISSUE_COL = "First Permit Date"
SHED_EXPIRY_COL = "Permit Expiration Date"
SHED_HOUSE_COL = "House Number"
SHED_STREET_COL = "Street Name"

VIOLATIONS_FILE = DATA_DIR + "dob_violations.csv"
VIOL_BIN_COL = "BIN"
VIOL_DATE_COL = "Violation Issue Date"
VIOL_STATUS_COL = "Violation Status"
VIOL_DESC_COL = "Violation Remarks"

COMPLAINTS_FILE = DATA_DIR + "dob_complaints.csv"
COMP_BIN_COL = "BIN"
COMP_DATE_COL = "Date Entered"
COMP_TYPE_COL = "Complaint Category"


def load_data():
    sheds = pd.read_csv(SHED_FILE, low_memory=False)
    violations = pd.read_csv(VIOLATIONS_FILE, low_memory=False)
    complaints = pd.read_csv(COMPLAINTS_FILE, low_memory=False)

    sheds[SHED_BIN_COL] = sheds[SHED_BIN_COL].astype(str)
    violations[VIOL_BIN_COL] = violations[VIOL_BIN_COL].astype(str)
    complaints[COMP_BIN_COL] = complaints[COMP_BIN_COL].astype(str)

    return sheds, violations, complaints


def find_bin_for_address(sheds_df, address: str):
    address_norm = address.strip().lower()
    combined = (
        sheds_df[SHED_HOUSE_COL].astype(str) + " " + sheds_df[SHED_STREET_COL].astype(str)
    ).str.lower()
    matches = sheds_df[combined.str.contains(address_norm, na=False)]
    if matches.empty:
        return None
    return matches.iloc[0][SHED_BIN_COL]


def get_shed_history(sheds_df, bin_number):
    rows = sheds_df[sheds_df[SHED_BIN_COL] == bin_number]
    if rows.empty:
        return None

    events = []
    for _, row in rows.iterrows():
        issue = pd.to_datetime(row[SHED_ISSUE_COL], errors="coerce")
        if pd.notnull(issue):
            events.append({"date": issue, "type": "shed_installed_or_renewed"})

    if not events:
        return None

    earliest = min(e["date"] for e in events)
    duration_days = (datetime.now() - earliest).days

    return {
        "first_permit_date": earliest,
        "duration_days": duration_days,
        "duration_years": round(duration_days / 365, 1),
        "renewal_count": len(events),
        "events": events,
    }


def get_violations(violations_df, bin_number):
    rows = violations_df[violations_df[VIOL_BIN_COL] == bin_number]
    result = []
    for _, row in rows.iterrows():
        result.append({
            "date": pd.to_datetime(row[VIOL_DATE_COL], errors="coerce"),
            "status": row.get(VIOL_STATUS_COL),
            "description": row.get(VIOL_DESC_COL),
        })
    return result


def get_complaints(complaints_df, bin_number):
    rows = complaints_df[complaints_df[COMP_BIN_COL] == bin_number]
    result = []
    for _, row in rows.iterrows():
        result.append({
            "date": pd.to_datetime(row[COMP_DATE_COL], errors="coerce"),
            "type": row.get(COMP_TYPE_COL),
            "type_label": describe_complaint_category(row.get(COMP_TYPE_COL)),
        })
    return result


def build_timeline(shed_history, violations, complaints):
    timeline = []

    for e in shed_history["events"]:
        timeline.append((e["date"], "Shed installed/renewed"))

    for v in violations:
        if pd.notnull(v["date"]):
            label = f"Violation: {v['description']}"
            if v["status"] and "open" in str(v["status"]).lower():
                label += " (still open)"
            timeline.append((v["date"], label))

    for c in complaints:
        if pd.notnull(c["date"]):
            timeline.append((c["date"], f"Complaint: {c['type_label']}"))

    timeline.sort(key=lambda x: x[0])
    return timeline


def get_building_report(address: str, sheds_df, violations_df, complaints_df):
    bin_number = find_bin_for_address(sheds_df, address)
    if bin_number is None:
        return None

    shed_history = get_shed_history(sheds_df, bin_number)
    if shed_history is None:
        return None

    violations = get_violations(violations_df, bin_number)
    complaints = get_complaints(complaints_df, bin_number)
    timeline = build_timeline(shed_history, violations, complaints)

    open_violations = [
        v for v in violations
        if v["status"] and "open" in str(v["status"]).lower()
    ]

    return {
        "bin": bin_number,
        "shed": shed_history,
        "violations": violations,
        "open_violation_count": len(open_violations),
        "complaint_count": len(complaints),
        "timeline": timeline,
    }


if __name__ == "__main__":
    sheds, violations, complaints = load_data()
    print("Loaded", len(sheds), "sheds,", len(violations), "violations,", len(complaints), "complaints")

    sample_address = sheds.iloc[0][SHED_HOUSE_COL] + " " + str(sheds.iloc[0][SHED_STREET_COL])
    print("Testing with address:", sample_address)

    report = get_building_report(sample_address, sheds, violations, complaints)
    print(report)