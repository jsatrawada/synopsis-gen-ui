import streamlit as st
import requests


# API_URL = "http://54.84.39.154:8000"
#API_URL = "http://127.0.0.1:8000"

api_url_options = ["http://54.84.39.154:8000", "http://127.0.0.1:8000"]
API_URL = st.selectbox("Select API URL", api_url_options)


st.title("Literature Retrieval Evidence Summarization, API Url : ")

with st.sidebar:
        st.title("Vector Update")
        uploaded_files = st.file_uploader("Choose PDF files", accept_multiple_files=True, type="pdf")
        if st.button("Load PDFs", key="load_pdfs_button"):    
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    response = requests.post(f"{API_URL}/ingest_pdf/", 
                        files={"file": (uploaded_file.name, uploaded_file.getvalue())})
                    if response.status_code == 200:
                        st.success("PDF processed and ingested successfully!")
                    else:
                        st.error("Error processing PDF.")
            else:
                st.error("Please upload PDF files.")
            st.success("Done")

        if st.button("Clear Vector Store", key="clear_vector_store_button"):
            response = requests.post(f"{API_URL}/clear_vector_store/")
            if response.status_code == 200:
                st.success("Vector store cleared successfully!")
            else:
                st.error("Error clearing vector store.")

question = st.text_input("Provide the parameters to generate evidence-based answers")
if st.button("Get Answer"):
    if question:
        with st.spinner("Processing..."):
            response = requests.post(f"{API_URL}/generate_evidence/", data={"question": question})
            if response.status_code == 200:
                data = response.json()
                st.write("**Answer:**")
                st.write(data["answer"])
            else:
                st.error("Error fetching answer.")
    else:
        st.warning("Please enter a question.")
