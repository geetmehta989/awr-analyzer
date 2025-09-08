import streamlit as st
from bs4 import BeautifulSoup

st.title("Oracle AWR Report Analyzer")

uploaded_file = st.file_uploader("Upload AWR HTML Report", type=["html", "htm"])

if uploaded_file is not None:
    soup = BeautifulSoup(uploaded_file, "html.parser")

    st.subheader("📊 Simplified Summary")

    # ---- Database Info ----
    db_info = {}
    db_table = soup.find("table")  # first table usually DB info
    if db_table:
        rows = db_table.find_all("tr")
        for row in rows:
            cols = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
            if len(cols) >= 2:
                db_info[cols[0]] = cols[1]
    st.write("**Database Info:**", db_info)

    # ---- Load Profile ----
    load_profile = {}
    load_table = soup.find("table", string=lambda x: x and "Load Profile" in x)
    if load_table:
        rows = load_table.find_all("tr")
        for row in rows:
            cols = [c.get_text(strip=True) for c in row.find_all("td")]
            if len(cols) >= 2:
                load_profile[cols[0]] = cols[1]
    st.write("**Load Profile:**", load_profile)

    # ---- Top Foreground Events ----
    st.write("**⏱️ Top Foreground Events:**")
    events_table = soup.find("table", string=lambda x: x and "Top 10 Foreground Events" in x)
    if events_table:
        st.table([[c.get_text(strip=True) for c in row.find_all("td")] 
                  for row in events_table.find_all("tr")[1:]])

    # ---- Instance Efficiency ----
    st.write("**⚡ Instance Efficiency Percentages:**")
    eff_table = soup.find("table", string=lambda x: x and "Instance Efficiency" in x)
    if eff_table:
        eff_data = {}
        for row in eff_table.find_all("tr"):
            cols = [c.get_text(strip=True) for c in row.find_all("td")]
            if len(cols) >= 2:
                eff_data[cols[0]] = cols[1]
        st.write(eff_data)

    # ---- Time Model Statistics ----
    st.write("**⏱️ Time Model Statistics:**")
    time_table = soup.find("table", string=lambda x: x and "Time Model Statistics" in x)
    if time_table:
        st.table([[c.get_text(strip=True) for c in row.find_all("td")] 
                  for row in time_table.find_all("tr")[1:]])
