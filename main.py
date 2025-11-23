import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- CONFIGURATION ---
current_dir = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(current_dir, "data")

# Set page configuration
st.set_page_config(page_title="Banggood Data Analysis", layout="wide")
st.title("📊 Banggood Product Data Dashboard")

# --- LOAD FILES FROM FOLDER ---
if not os.path.exists(DATA_FOLDER):
    st.error(f"Folder '{DATA_FOLDER}' nahi mila! Please 'data' naam ka folder banayen aur usme CSV files rakhein.")
    st.stop()

csv_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.csv')]

if not csv_files:
    st.warning(f"'{DATA_FOLDER}' folder khali hai! Koi CSV file nazar nahi aayi.")
    st.stop()

# Sidebar Selection
st.sidebar.header("Select Category File")
selected_file = st.sidebar.radio("Choose a file to analyze:", csv_files)

# --- MAIN ANALYSIS LOGIC ---
if selected_file:
    file_path = os.path.join(DATA_FOLDER, selected_file)
    st.markdown(f"### Analysis for: `{selected_file}`")

    try:
        df = pd.read_csv(file_path)
        
        # Show Raw Data Option
        with st.expander("📂 View Raw Data"):
            st.dataframe(df.head())
            st.write(f"**Total Rows:** {df.shape[0]} | **Total Columns:** {df.shape[1]}")

        # Check Columns
        required_cols = ['Price', 'Reviews', 'Name', 'Price_Segment', 'Est_Revenue']
        missing = [c for c in required_cols if c not in df.columns]

        if missing:
            st.error(f"❌ Missing columns: {missing}. Please check if file is cleaned.")
        else:
            # --- VISUALIZATIONS ---
            
            # Row 1
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("1. Price Distribution")
                fig, ax = plt.subplots(figsize=(8, 5))
                sns.histplot(df['Price'], bins=20, kde=True, color='skyblue', ax=ax)
                ax.set_title("Price Spread")
                st.pyplot(fig)
            
            with c2:
                st.subheader("2. Price vs Reviews")
                fig, ax = plt.subplots(figsize=(8, 5))
                sns.scatterplot(x='Price', y='Reviews', data=df, color='green', alpha=0.6, ax=ax)
                ax.set_title("Are cheaper items more popular?")
                st.pyplot(fig)

            # Row 2
            st.subheader("3. Top 5 Most Reviewed Products")
            fig, ax = plt.subplots(figsize=(10, 5))
            top5 = df.nlargest(5, 'Reviews')
            sns.barplot(x='Reviews', y='Name', data=top5, palette='viridis', ax=ax)
            ax.set_xlabel("Review Count")
            st.pyplot(fig)

            # Row 3
            c3, c4 = st.columns(2)
            with c3:
                st.subheader("4. Products by Segment")
                fig, ax = plt.subplots()
                sns.countplot(x='Price_Segment', data=df, palette='pastel', 
                              order=['Low Budget', 'Mid Range', 'Premium'], ax=ax)
                st.pyplot(fig)
            
            with c4:
                st.subheader("5. Revenue by Segment")
                fig, ax = plt.subplots()
                revenue = df.groupby('Price_Segment')['Est_Revenue'].sum().reindex(['Low Budget', 'Mid Range', 'Premium'])
                sns.barplot(x=revenue.index, y=revenue.values, palette='magma', ax=ax)
                st.pyplot(fig)

    except Exception as e:
        st.error(f"Error loading file: {e}")