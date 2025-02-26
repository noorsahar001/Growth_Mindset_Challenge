#import
import streamlit as st
import pandas as pd
import os
from io import BytesIO


#Set up our App
st.set_page_config(page_title="💿 Data sweeper", layout='wide')
st.title("💿 Data sweeper by NoorSahar")
st.write("Transfrom your files between CSV and Excel formats with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for files in uploaded_files:
        file_ext = os.path.splitext(files.name)[-1].lower()


        if file_ext == ".csv":
            df = pd.read_csv(files)
        elif file_ext == ".xlsx":
            df = pd.read_excel(files)
        else:
            st.error("Unsupported file type: {file_ext}")
            continue

        #Display info about the file
        st.write(f"**File Name:** {files.name}")
        st.write(f"**File Size:** {files.size/1024}")

        #Show 5 rows of our df
        st.write("🔍 Preview the Head of the Dataframe")
        st.dataframe(df.head())

        #Options for data cleaning
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean Data for {files.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {files.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missings values for {files.name}"):
                    numeric_cols = df.select_dtypes(include={'number'}).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values have been Filled!")


        #Choose Specific Columns to keep or Convert
        st.subheader("🎯 Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {files.name}", df.columns, default=df.columns)
        df = df[columns]


        #Create some Visualizations
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {files.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])


        #Convert to File Csv to Excel
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {files.name} to:", ["CSV","Excel"], key=files.name)
        if st.button(f"Convert {files.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer,index=False)
                file_name = files.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer,index=False)
                file_name = files.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            #Download Button
            st.download_button(
                label=f"⬇️ Download {files.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
st.success("🎉 All files processed Successfully!")

                


 
