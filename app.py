import pandas as pd
import streamlit as st
from pipeline import load_data, get_building_report
from ai_chat import ask_ai

st.set_page_config(page_title="ShedTrace", page_icon="🏗️")

st.title("🏗️ ShedTrace")
st.caption("The paper trail behind every shed.")

@st.cache_data
def get_data():
    return load_data()

sheds, violations, complaints, elevator, fire = get_data()

address = st.text_input("Enter a NYC address:")

if st.button("Investigate Building") and address:
    report = get_building_report(address, sheds, violations, complaints, elevator, fire)
    st.session_state["report"] = report
    st.session_state["address"] = address

report = st.session_state.get("report")
saved_address = st.session_state.get("address")

if report is None and address:
    st.warning("No sidewalk shed currently found at that address.")

if report is not None:
    shed = report["shed"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Shed active for", f"{shed['duration_years']} yrs")
    col2.metric("Open violations", report["open_violation_count"])
    col3.metric("Complaints filed", report["complaint_count"])

    st.caption(f"Permit renewals: {shed['renewal_count']}")

    tab_shed, tab_elevator, tab_fire, tab_ai = st.tabs(
        ["🏗️ Shed Timeline", "🛗 Elevator Safety", "🔥 Fire Safety", "🤖 Ask AI"]
    )

    with tab_shed:
        st.subheader("Evidence Timeline")

        timeline = report["timeline"]
        MAX_SHOWN = 15

        if len(timeline) > MAX_SHOWN:
            st.caption(
                f"Showing the {MAX_SHOWN} most recent of {len(timeline)} total events."
            )
            shown = timeline[-MAX_SHOWN:]
        else:
            shown = timeline

        for date, label in shown:
            st.write(f"**{date.date()}** — {label}")

        if len(timeline) > MAX_SHOWN:
            with st.expander(f"Show all {len(timeline)} events"):
                for date, label in timeline:
                    st.write(f"**{date.date()}** — {label}")

    with tab_elevator:
        elevator_records = report["elevator_records"]
        if not elevator_records:
            st.info("No elevator safety records found for this building.")
        else:
            st.write(f"**{len(elevator_records)} elevator device(s) on file**")
            for e in elevator_records:
                inspected = (
                    e["last_inspection"].date()
                    if pd.notnull(e["last_inspection"])
                    else "Unknown"
                )
                cat1_filed = (
                    e["last_cat1_filed"].date()
                    if pd.notnull(e["last_cat1_filed"])
                    else "Unknown"
                )
                st.write(
                    f"- **{e['device_type']}** (Device #{e['device_number']}) — "
                    f"Status: {e['status']} — Last inspected: {inspected}"
                )

                with st.expander(f"View elevator history — Device #{e['device_number']}"):
                    st.write(f"**Current status:** {e['status']}")
                    st.write(f"**Last periodic inspection:** {inspected}")
                    st.write(f"**Last CAT1 report filed:** {cat1_filed}")

                    elev_violations = report["elevator_related_violations"]
                    elev_complaints = report["elevator_related_complaints"]

                    st.write(f"**Elevator-related violations:** {len(elev_violations)}")
                    for v in elev_violations:
                        date = v["date"].date() if pd.notnull(v["date"]) else "Unknown"
                        st.write(f"  - {date}: {v['description']}")

                    st.write(f"**Elevator-related complaints:** {len(elev_complaints)}")
                    for c in elev_complaints:
                        date = c["date"].date() if pd.notnull(c["date"]) else "Unknown"
                        st.write(f"  - {date}: {c['type_label']}")

    with tab_fire:
        fire_records = report["fire_records"]
        if not fire_records:
            st.info("No fire safety inspection records found for this building.")
        else:
            st.write(f"**{len(fire_records)} fire inspection record(s) on file**")
            for f in fire_records:
                visited = (
                    f["last_visit"].date()
                    if pd.notnull(f["last_visit"])
                    else "Unknown"
                )
                st.write(
                    f"- Status: **{f['status_label']}** — Last visit: {visited}"
                )

            with st.expander("View fire safety history"):
                fire_violations = report["fire_related_violations"]
                fire_complaints = report["fire_related_complaints"]

                st.write(f"**Fire-related violations:** {len(fire_violations)}")
                for v in fire_violations:
                    date = v["date"].date() if pd.notnull(v["date"]) else "Unknown"
                    st.write(f"  - {date}: {v['description']}")

                st.write(f"**Fire-related complaints:** {len(fire_complaints)}")
                for c in fire_complaints:
                    date = c["date"].date() if pd.notnull(c["date"]) else "Unknown"
                    st.write(f"  - {date}: {c['type_label']}")

    with tab_ai:
        st.subheader(f"Ask about {saved_address}")
        st.caption("This assistant only knows the real data shown in the other tabs for this building.")

        question = st.text_input("Ask a question:", key="ai_question")
        if st.button("Ask", key="ai_ask_button") and question:
            with st.spinner("Thinking..."):
                try:
                    answer = ask_ai(saved_address, report, question)
                    st.write(answer)
                except Exception as e:
                    st.error(f"Something went wrong talking to Gemini: {e}")