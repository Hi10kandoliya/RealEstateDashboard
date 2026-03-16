import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(
    page_title="TX Housing Dashboard",
    layout="wide"
)

st.title("🏠 Texas Housing Market Dashboard")
st.markdown("Dallas–Plano–Irving Market Data Explorer")

# -----------------------------------
# Load Data
# -----------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("TX-Housing-Data.csv")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        
        # Remove rows with invalid dates
        initial_rows = len(df)
        df = df.dropna(subset=["Date"])
        
        if len(df) == 0:
            st.error("No valid date data found in the CSV file. Please check your data format.")
            return pd.DataFrame()
        
        if initial_rows > len(df):
            st.warning(f"Removed {initial_rows - len(df)} rows with invalid dates.")
        
        df = df.sort_values("Date")
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

df = load_data()

# Check if data is empty
if df.empty:
    st.stop()

# -----------------------------------
# Sidebar Filters
# -----------------------------------
st.sidebar.header("Filters")

# City Filter - Check if 'City' column exists
if 'City' in df.columns:
    # Get unique cities
    cities = ['All'] + sorted(df['City'].unique().tolist())
    selected_city = st.sidebar.selectbox("Select City", cities)
else:
    st.sidebar.warning("City column not found in data")
    selected_city = 'All'

# Date Filters
min_date = df["Date"].min()
max_date = df["Date"].max()

# Convert to date objects for the date_input widget
min_date_date = min_date.date() if hasattr(min_date, 'date') else min_date
max_date_date = max_date.date() if hasattr(max_date, 'date') else max_date

start_date = st.sidebar.date_input("Start Date", min_date_date)
end_date = st.sidebar.date_input("End Date", max_date_date)

# Convert back to datetime for filtering
start_datetime = pd.to_datetime(start_date)
end_datetime = pd.to_datetime(end_date)

# Apply filters
filtered = df[(df["Date"] >= start_datetime) & (df["Date"] <= end_datetime)]

# Apply city filter if selected
if 'City' in df.columns and selected_city != 'All':
    filtered = filtered[filtered['City'] == selected_city]

# Show filter summary
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Filter Summary:**")
st.sidebar.markdown(f"- Date Range: {start_date} to {end_date}")
if 'City' in df.columns and selected_city != 'All':
    st.sidebar.markdown(f"- City: {selected_city}")
st.sidebar.markdown(f"- Records: {len(filtered):,}")

# -----------------------------------
# KPI Metrics
# -----------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"{filtered['Sales'].sum():,}" if 'Sales' in filtered.columns else "N/A")
col2.metric("Avg Price", f"${filtered['Average Price'].mean():,.0f}" if 'Average Price' in filtered.columns else "N/A")
col3.metric("Median Price", f"${filtered['Median Price'].mean():,.0f}" if 'Median Price' in filtered.columns else "N/A")
col4.metric("Months Inventory (Avg)", f"{filtered['Months Inventory'].mean():.2f}" if 'Months Inventory' in filtered.columns else "N/A")

# -----------------------------------
# City Breakdown (if city filter is 'All')
# -----------------------------------
if 'City' in df.columns and selected_city == 'All' and len(filtered) > 0:
    st.subheader("🏙️ City Breakdown")
    
    # Calculate city-level metrics
    city_metrics = filtered.groupby('City').agg({
        'Sales': 'sum',
        'Average Price': 'mean',
        'Median Price': 'mean',
        'Months Inventory': 'mean'
    }).round(2).reset_index()
    
    # Format currency columns
    city_metrics['Average Price'] = city_metrics['Average Price'].apply(lambda x: f"${x:,.0f}")
    city_metrics['Median Price'] = city_metrics['Median Price'].apply(lambda x: f"${x:,.0f}")
    city_metrics['Sales'] = city_metrics['Sales'].apply(lambda x: f"{x:,.0f}")
    city_metrics['Months Inventory'] = city_metrics['Months Inventory'].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(city_metrics, use_container_width=True)

# -----------------------------------
# Line Charts
# -----------------------------------
if len(filtered) > 0:
    st.subheader("📈 Sales Over Time")
    fig, ax = plt.subplots(figsize=(12, 5))
    
    if 'City' in df.columns and selected_city == 'All':
        # Show all cities with different colors
        for city in filtered['City'].unique():
            city_data = filtered[filtered['City'] == city]
            sns.lineplot(data=city_data, x="Date", y="Sales", label=city, ax=ax)
    else:
        # Single line for selected city or if no city column
        sns.lineplot(data=filtered, x="Date", y="Sales", ax=ax)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.subheader("💵 Average vs Median Price")
    fig, ax = plt.subplots(figsize=(12, 5))
    
    if 'City' in df.columns and selected_city == 'All':
        # Create subplots or different visualization for multiple cities
        for city in filtered['City'].unique():
            city_data = filtered[filtered['City'] == city]
            sns.lineplot(data=city_data, x="Date", y="Average Price", label=f"{city} - Avg", ax=ax, linestyle='-')
            sns.lineplot(data=city_data, x="Date", y="Median Price", label=f"{city} - Med", ax=ax, linestyle='--')
    else:
        sns.lineplot(data=filtered, x="Date", y="Average Price", label="Average Price", ax=ax)
        sns.lineplot(data=filtered, x="Date", y="Median Price", label="Median Price", ax=ax)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    
    # -----------------------------------
    # Inventory Chart
    # -----------------------------------
    st.subheader("📦 Months of Inventory")
    fig, ax = plt.subplots(figsize=(12, 5))
    
    if 'City' in df.columns and selected_city == 'All':
        for city in filtered['City'].unique():
            city_data = filtered[filtered['City'] == city]
            sns.lineplot(data=city_data, x="Date", y="Months Inventory", label=city, ax=ax)
    else:
        sns.lineplot(data=filtered, x="Date", y="Months Inventory", color="red", ax=ax)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    
    # -----------------------------------
    # Correlation Heatmap
    # -----------------------------------
    st.subheader("🔍 Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10, 6))
    numeric_df = filtered.select_dtypes(include=["float64", "int64"])
    
    # Exclude non-numeric columns that might have crept in
    exclude_cols = ['City'] if 'City' in numeric_df.columns else []
    numeric_df = numeric_df.drop(columns=exclude_cols, errors='ignore')
    
    if len(numeric_df.columns) > 1:  # Need at least 2 columns for correlation
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.info("Not enough numeric columns for correlation heatmap")
    
    # -----------------------------------
    # Scatter Plot
    # -----------------------------------
    st.subheader("📊 Price vs Sales")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if 'City' in df.columns and selected_city == 'All':
        sns.scatterplot(data=filtered, x="Average Price", y="Sales", hue="City", alpha=0.6, ax=ax)
    else:
        sns.regplot(data=filtered, x="Average Price", y="Sales", scatter_kws={"alpha":0.4}, ax=ax)
    
    plt.tight_layout()
    st.pyplot(fig)
    
else:
    st.warning("No data available for the selected filters")

st.markdown("---")
st.markdown("Dashboard built with ❤️ using Streamlit, Seaborn, and Matplotlib")
