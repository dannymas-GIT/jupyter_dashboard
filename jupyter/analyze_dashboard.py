import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import os
import io

st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

st.title("Data Analysis Dashboard")

@st.cache_data
def load_data():
    try:
        file_path = 'MOCK_DATA.csv'
        st.write(f"Attempting to load file from: {os.path.abspath(file_path)}")
        df = pd.read_csv(file_path, delimiter=',', quotechar='"')
        st.success(f"File loaded successfully. Shape: {df.shape}")
        return df
    except pd.errors.EmptyDataError:
        st.error("Error: The CSV file is empty.")
        return None
    except FileNotFoundError:
        st.error(f"Error: The CSV file '{file_path}' was not found.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return None

df = load_data()

if df is not None:
    st.header("Data Overview")
    st.write("DataFrame info:")
    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

    st.write("First few rows of the data:")
    st.dataframe(df.head(), use_container_width=True)

    st.header("Column Information")
    st.write("Available columns in the dataset:")
    st.write(df.columns.tolist())

    st.header("Summary Statistics")
    st.dataframe(df.describe(), use_container_width=True)

    st.header("Missing Values")
    missing_data = df.isnull().sum().reset_index()
    missing_data.columns = ['Column', 'Missing Count']
    missing_data['Missing Percentage'] = (missing_data['Missing Count'] / len(df)) * 100
    st.dataframe(missing_data, use_container_width=True)

    # Select the first column for analysis
    first_column = df.columns[0]

    st.header(f"{first_column} Analysis")
    col1, col2 = st.columns(2)
    with col1:
        unique_values = df[first_column].dropna().unique()
        
        # Handle both string and numeric types
        if pd.api.types.is_numeric_dtype(df[first_column]):
            unique_values = sorted(unique_values)
        else:
            unique_values = sorted([str(value).strip() for value in unique_values if str(value).strip()])
        
        selected_value = st.selectbox(f"Select a {first_column}", unique_values)
        
        # For numeric columns, use exact matching
        if pd.api.types.is_numeric_dtype(df[first_column]):
            filtered_df = df[df[first_column] == selected_value]
        else:
            filtered_df = df[df[first_column].astype(str).str.contains(str(selected_value), case=False, na=False)]
        
        if not filtered_df.empty:
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning(f"No data found for the {first_column}: {selected_value}")

    with col2:
        top_values = df[first_column].value_counts().head(10)
        fig = px.bar(top_values, x=top_values.index, y=top_values.values, title=f"Top 10 {first_column}s")
        st.plotly_chart(fig, use_container_width=True)

    # Analyze numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_columns:
        st.header("Numeric Column Analysis")
        selected_numeric_column = st.selectbox("Select a numeric column for analysis", numeric_columns)
        
        fig = px.histogram(df, x=selected_numeric_column, title=f"Distribution of {selected_numeric_column}")
        st.plotly_chart(fig, use_container_width=True)

        if len(numeric_columns) > 1:
            st.header("Correlation Heatmap")
            corr_matrix = df[numeric_columns].corr()
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
    else:
        st.warning("No numeric columns found for analysis.")

else:
    st.error("Failed to load the data. Please check the file path and contents.")

st.header("Data Upload")
st.write("You can upload your own CSV file for analysis.")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    user_df = pd.read_csv(uploaded_file)
    st.write("Preview of uploaded data:")
    st.dataframe(user_df.head(), use_container_width=True)
    st.write(f"Uploaded data shape: {user_df.shape}")

st.header("Feedback")
feedback = st.text_area("Please provide your feedback on this dashboard:")
if st.button("Submit Feedback"):
    st.success("Thank you for your feedback!")

st.sidebar.header("About")
st.sidebar.info("This dashboard analyzes data using various Streamlit features.")
st.sidebar.header("Controls")
if st.sidebar.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(df)

