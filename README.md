# ShedTrace

The paper trail behind every shed.

## Setup

1. Download 3 CSVs from NYC Open Data and put them in the `data/` folder:
   - Sidewalk shed permits → save as `data/sidewalk_sheds.csv`
   - DOB Violations → save as `data/dob_violations.csv`
   - DOB Complaints Received → save as `data/dob_complaints.csv`

2. Build and start the app:
   ```
   docker compose up --build
   ```

3. First, check your real column names by running:
   ```
   docker compose run app python pipeline.py
   ```
   Copy the printed column names into the `# VERIFY` lines at the top of `pipeline.py`.

4. Re-run `docker compose up --build` and open http://localhost:8501
