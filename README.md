# 🏗️ ShedTrace

**The paper trail behind every shed.**

ShedTrace is a NYC building-safety evidence tool built for DivHacks 2026. Enter an address, and it connects real NYC public records for that building — sidewalk shed history, DOB violations, DOB complaints, elevator safety records, and FDNY fire inspections — into one evidence timeline, joined by the building's BIN (Building Identification Number).

## The Problem

This information already exists, but it's scattered across separate NYC public datasets. Investigating one building means searching multiple systems by hand and piecing the timeline together yourself.

## The Solution

Enter an address → ShedTrace finds the building's BIN, confirms it has an active shed on file, pulls records from all five datasets, joins them by BIN, and presents one chronological building profile instead of five disconnected sources.

## Features

- **Shed Timeline** — shed installation/renewal history, merged with the building's violations and complaints, sorted chronologically
- **Elevator Safety** — real device records (type, status, last inspection, last CAT1 filing) from DOB NOW: Elevator Safety Compliance, with an expandable elevator-specific violation/complaint history
- **Fire Safety** — real FDNY inspection records, with raw status codes decoded into plain English (e.g. `NOT APPROVAL(W/REASON)` → "Failed inspection (reason noted)"), plus fire-related violation/complaint history
- **3D Map View** — the investigated building rendered as a 3D bar, height reflecting violation/complaint volume; tap/hover to see the data
- **Ask AI** — a Gemini assistant scoped to only the currently investigated building's real data, instructed to say when the data doesn't answer a question rather than guess

**Demo building:** 900 Grand Concourse — 14.8-year-old active shed, 106 violations, 215 complaints.

## Why Only Shed Buildings?

Intentional scope: the core question is "why is this specific shed still standing," not a generic citywide lookup tool. The BIN-based architecture could extend to any building later.

## Data Sources

NYC Open Data: Sidewalk Shed Permits, DOB Violations, DOB Complaints Received, DOB NOW: Elevator Safety Compliance (`e5aq-a4j2`). FDNY: Bureau of Fire Prevention Inspections (`ssq6-fkht`). Joined by BIN.

## Tech Stack

Python + pandas (pipeline), Streamlit (UI), Google Gemini (AI assistant), Docker/Docker Compose (dev environment).

## Getting Started

```bash
git clone https://github.com/sristi1125/ShedTrace.git
cd ShedTrace
```

Create a `.env` file:
```env
GEMINI_API_KEY=your_api_key_here
```

Run it:
```bash
docker compose up --build
```
Open `http://localhost:8501`.

## Known Limitations

- Data is a snapshot downloaded during development, not a live feed
- Only works for buildings with an active shed on file (intentional)
- Elevator dataset gives current status only, no history of status changes over time

## Future Work

- Live data refresh from NYC Open Data API
- Citywide building lookup
- 3D map showing multiple buildings at once
- Historical elevator status tracking

---

Built using the help of Grok, Cursor, and the Gemini API.
