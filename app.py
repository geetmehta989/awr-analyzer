import streamlit as st
from bs4 import BeautifulSoup

st.set_page_config(page_title="AWR Analyzer", layout="wide")

st.title("📊 Oracle AWR Report Analyzer")

# Step 1: Upload file
uploaded_file = st.file_uploader("Upload your AWR HTML report", type=["html"])

# Step 2: Analyse button
if uploaded_file is not None:
    if st.button("Analyse"):
        # Parse HTML
        soup = BeautifulSoup(uploaded_file, "html.parser")

        # Extract some basic details (example)
        db_name = None
        instance_name = None
        elapsed_time = None
        db_time = None

        # Try to extract values from the HTML (depends on report structure)
        tables = soup.find_all("table")
        if tables:
            text = soup.get_text()
            for line in text.splitlines():
                if "DB Name" in line and db_name is None:
                    db_name = line.split()[-1]
                if "Instance" in line and instance_name is None:
                    instance_name = line.split()[-1]
                if "Elapsed" in line and elapsed_time is None:
                    elapsed_time = line.split()[-1]
                if "DB Time" in line and db_time is None:
                    db_time = line.split()[-1]

        # Display simplified output
        st.subheader("🔎 Simplified Summary")
        st.write(f"**Database Name:** {db_name or 'Not found'}")
        st.write(f"**Instance Name:** {instance_name or 'Not found'}")
        st.write(f"**Elapsed Time:** {elapsed_time or 'Not found'}")
        st.write(f"**DB Time:** {db_time or 'Not found'}")

        st.success("✅ Analysis complete!")

else:
    st.info("👆 First upload an AWR HTML report to enable analysis.")
