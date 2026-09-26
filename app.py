import streamlit as st
from pipeline import load_data, get_building_report

st.set_page_config(page_title="ShedTrace", page_icon="🏗️")

st.title("🏗️ ShedTrace")
st.caption("The paper trail behind every shed.")

@st.cache_data
def get_data():
    return load_data()

sheds, violations, complaints = get_data()

address = st.text_input("Enter a NYC address:")

if st.button("Investigate Building") and address:
    report = get_building_report(address, sheds, violations, complaints)

    if report is None:
        st.warning("No sidewalk shed currently found at that address.")
    else:
        shed = report["shed"]

        col1, col2, col3 = st.columns(3)
        col1.metric("Shed active for", f"{shed['duration_years']} yrs")
        col2.metric("Open violations", report["open_violation_count"])
        col3.metric("Complaints filed", report["complaint_count"])

        st.caption(f"Permit renewals: {shed['renewal_count']}")

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