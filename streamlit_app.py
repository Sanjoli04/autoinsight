import streamlit as st
import os
import subprocess
import time

st.title("AutoInsight: Provides insights on your dataset with a single click")

uploaded_file = st.file_uploader("Upload your dataset (CSV only)", type=['csv'])

if uploaded_file:
    filename = "temp.csv"

    with open(filename, "wb") as f:
        f.write(uploaded_file.read())

    st.info("File uploaded. Processing...")

    start_time = time.time()

    result = subprocess.run(
        ["python", "main.py", filename],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        st.error("Error during processing")
        st.text(result.stderr)
        st.stop()

    folder_name = filename.split(".")[0]
    zip_path = folder_name + ".zip"

    end_time = time.time()

    if os.path.exists(zip_path):
        st.success(f"Processed in {end_time - start_time:.2f} seconds!")

        with open(zip_path, "rb") as f:
            st.download_button(
                "Download Report ZIP",
                f,
                file_name="report.zip"
            )
    else:
        st.error("ZIP file not generated.")