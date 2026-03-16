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
@st.cache_data
def load_data():
    df = pd.read_csv("TX-Housing-Data.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.sort_values("Date")
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")

# --- City Filter ---
cities = df["Market Name"].unique()
selected_city = st.sidebar.selectbox("Select City / Market", cities)

df_city = df[df["Market Name"] == selected_city]

# --- Date Filters ---
start_date = st.sidebar.date_input("Start Date", df_city["Date"].min())
end_date = st.sidebar.date_input("End Date", df_city["Date"].max())

filtered = df_city[(df_city["Date"] >= pd.to_datetime(start_date)) &
                   (df_city["Date"] <= pd.to_datetime(end_date))]


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
