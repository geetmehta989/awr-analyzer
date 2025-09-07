import streamlit as st
from bs4 import BeautifulSoup

st.set_page_config(page_title="AWR Analyzer", layout="wide")
st.title("📊 Oracle AWR Report Analyzer")

# Upload file
uploaded_file = st.file_uploader("Upload your AWR HTML report", type=["html"])

if uploaded_file is not None:
    if st.button("Analyse"):
        soup = BeautifulSoup(uploaded_file, "html.parser")

        # Look for the Database Info table
        db_info = {}
        tables = soup.find_all("table")
        if tables:
            # Assuming the first table has DB info
            first_table = tables[0]
            rows = first_table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True)
                    value = cols[1].get_text(strip=True)
                    db_info[key] = value

        # Display simplified output
        st.subheader("🔎 Simplified Summary")
        st.write(f"**Database Name:** {db_info.get('DB Name', 'Not found')}")
        st.write(f"**Instance Name:** {db_info.get('Instance', 'Not found')}")
        st.write(f"**Elapsed Time:** {db_info.get('Elapsed Time', 'Not found')}")
        st.write(f"**DB Time:** {db_info.get('DB Time', 'Not found')}")

        st.success("✅ Analysis complete!")
else:
    st.info("👆 First upload an AWR HTML report to enable analysis.")
