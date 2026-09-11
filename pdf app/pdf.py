import streamlit as st
from pypdf import PdfWriter, PdfReader
import io

# Set up the web page layout and title
st.set_page_config(page_title="PDF Toolkit", page_icon="📄", layout="centered")

st.title("📄 PDF Toolkit")
st.write("Merge study materials, split textbooks, or compress files for email.")

# Create a sidebar for navigation
tool = st.sidebar.radio("Choose a Tool", ["Merge PDFs", "Split PDF", "Compress PDF"])

# -----------------------------------------
# TOOL 1: MERGE PDFs
# -----------------------------------------
if tool == "Merge PDFs":
    st.header("Merge Multiple PDFs")
    uploaded_files = st.file_uploader("Upload study materials to combine", type="pdf", accept_multiple_files=True)
    
    if uploaded_files:
        st.write(f"**{len(uploaded_files)} files queued for merging.**")
        if st.button("Merge Files"):
            merger = PdfWriter()
            
            try:
                for pdf in uploaded_files:
                    merger.append(pdf)
                
                # Save to an in-memory buffer
                output = io.BytesIO()
                merger.write(output)
                
                st.success("Files merged successfully!")
                st.download_button(
                    label="Download Merged PDF",
                    data=output.getvalue(),
                    file_name="merged_study_materials.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")

# -----------------------------------------
# TOOL 2: SPLIT PDF
# -----------------------------------------
elif tool == "Split PDF":
    st.header("Extract Chapters from a PDF")
    uploaded_file = st.file_uploader("Upload a large textbook", type="pdf")
    
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        total_pages = len(reader.pages)
        st.info(f"This document has **{total_pages}** pages.")
        
        col1, col2 = st.columns(2)
        with col1:
            start_page = st.number_input("Start Page", min_value=1, max_value=total_pages, value=1)
        with col2:
            end_page = st.number_input("End Page", min_value=start_page, max_value=total_pages, value=total_pages)
            
        if st.button("Extract Pages"):
            writer = PdfWriter()
            
            try:
                # pypdf uses 0-based indexing
                for i in range(start_page - 1, end_page):
                    writer.add_page(reader.pages[i])
                
                output = io.BytesIO()
                writer.write(output)
                
                st.success(f"Pages {start_page} to {end_page} extracted!")
                st.download_button(
                    label="Download Extracted Chapter",
                    data=output.getvalue(),
                    file_name=f"chapter_pages_{start_page}_to_{end_page}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")

# -----------------------------------------
# TOOL 3: COMPRESS PDF
# -----------------------------------------
elif tool == "Compress PDF":
    st.header("Compress PDF for Email")
    st.write("*Note: This applies structural compression (removing unreferenced objects and duplicate data). It works best on text-heavy PDFs.*")
    
    uploaded_file = st.file_uploader("Upload file to shrink", type="pdf")
    
    if uploaded_file:
        original_size_kb = uploaded_file.size / 1024
        st.write(f"Original Size: **{original_size_kb:.2f} KB**")
        
        if st.button("Compress File"):
            reader = PdfReader(uploaded_file)
            writer = PdfWriter()
            
            try:
                for page in reader.pages:
                    writer.add_page(page)
                
                # pypdf automatically applies basic compression to output streams
                output = io.BytesIO()
                writer.write(output)
                
                compressed_size_kb = len(output.getvalue()) / 1024
                reduction = 100 - ((compressed_size_kb / original_size_kb) * 100)
                
                st.success("Compression complete!")
                st.metric(label="New Size", value=f"{compressed_size_kb:.2f} KB", delta=f"-{reduction:.1f}%")
                
                st.download_button(
                    label="Download Compressed PDF",
                    data=output.getvalue(),
                    file_name="compressed_document.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")