import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

# Sidebar Filters
st.sidebar.header("Filters")

# Get min and max dates safely
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

filtered = df[(df["Date"] >= start_datetime) & (df["Date"] <= end_datetime)]

# Rest of your code continues here...
# [Keep all your existing visualization code]

# -----------------------------------
# KPI Metrics
# -----------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"{filtered['Sales'].sum():,}")
col2.metric("Avg Price", f"${filtered['Average Price'].mean():,.0f}")
col3.metric("Median Price", f"${filtered['Median Price'].mean():,.0f}")
col4.metric("Months Inventory (Avg)", f"{filtered['Months Inventory'].mean():.2f}")

# -----------------------------------
# Line Charts
# -----------------------------------
st.subheader("📈 Sales Over Time")
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=filtered, x="Date", y="Sales", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("💵 Average vs Median Price")
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=filtered, x="Date", y="Average Price", label="Average Price", ax=ax)
sns.lineplot(data=filtered, x="Date", y="Median Price", label="Median Price", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# -----------------------------------
# Inventory Chart
# -----------------------------------
st.subheader("📦 Months of Inventory")
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=filtered, x="Date", y="Months Inventory", color="red", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# -----------------------------------
# Correlation Heatmap
# -----------------------------------
st.subheader("🔍 Correlation Heatmap")
fig, ax = plt.subplots(figsize=(10, 6))
numeric_df = filtered.select_dtypes(include=["float64", "int64"])
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# -----------------------------------
# Scatter Plot
# -----------------------------------
st.subheader("📊 Price vs Sales")
fig, ax = plt.subplots(figsize=(10, 6))
sns.regplot(data=filtered, x="Average Price", y="Sales", scatter_kws={"alpha":0.4}, ax=ax)
st.pyplot(fig)

st.markdown("---")
st.markdown("Dashboard built with ❤️ using Streamlit, Seaborn, and Matplotlib.")
