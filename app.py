import streamlit as st
from bs4 import BeautifulSoup

st.set_page_config(page_title="AWR Analyzer", layout="wide")
st.title("📊 Oracle AWR Report Analyzer")

# Upload file
uploaded_file = st.file_uploader("Upload your AWR HTML report", type=["html"])

if uploaded_file is not None:
    if st.button("Analyse"):
        soup = BeautifulSoup(uploaded_file, "html.parser")

        # ------------------ Database Info ------------------
        db_info = {}
        tables = soup.find_all("table")
        if tables:
            first_table = tables[0]  # Assuming first table is DB Info
            rows = first_table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True)
                    value = cols[1].get_text(strip=True)
                    db_info[key] = value

        st.subheader("🔎 Simplified Summary")
        st.write(f"**Database Name:** {db_info.get('DB Name', 'Not found')}")
        st.write(f"**Instance Name:** {db_info.get('Instance', 'Not found')}")
        st.write(f"**Elapsed Time:** {db_info.get('Elapsed Time', 'Not found')}")
        st.write(f"**DB Time:** {db_info.get('DB Time', 'Not found')}")

        # ------------------ Load Profile ------------------
        st.subheader("📈 Load Profile")
        load_profile = {}
        if len(tables) > 1:  # Assuming second table is Load Profile
            lp_table = tables[1]
            rows = lp_table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True)
                    value = cols[1].get_text(strip=True)
                    load_profile[key] = value
        if load_profile:
            for k, v in load_profile.items():
                st.write(f"**{k}:** {v}")
        else:
            st.write("No Load Profile found.")

        # ------------------ Top Timed Events ------------------
        st.subheader("⏱️ Top Timed Events")
        top_events = []
        if len(tables) > 2:  # Assuming third table is Top Timed Events
            tt_table = tables[2]
            rows = tt_table.find_all("tr")
            for row in rows[1:]:  # Skip header row
                cols = row.find_all("td")
                if len(cols) == 2:
                    event_name = cols[0].get_text(strip=True)
                    waits = cols[1].get_text(strip=True)
                    top_events.append((event_name, waits))
        if top_events:
            for event, waits in top_events:
                st.write(f"**{event}:** {waits}")
        else:
            st.write("No Top Timed Events found.")

        st.success("✅ Analysis complete!")
else:
    st.info("👆 First upload an AWR HTML report to enable analysis.")
