import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Load the datasets
df_HouseData = pd.read_csv('TX-Housing-Data.csv', parse_dates=['Date'])


# Combine datasets
df = pd.concat([df_wichita, df_waco])

# Convert date to datetime and extract year/month
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Sort by date
df = df.sort_values('Date')

# Set up the visualization
plt.style.use('ggplot')
plt.figure(figsize=(15, 20))

# 1. Median Price Trend
plt.subplot(4, 1, 1)
for city in df['City'].unique():
    city_data = df[df['City'] == city]
    plt.plot(city_data['Date'], city_data['Median Price'], label=city)
plt.title('Median Home Price Trend (1990-2026)')
plt.ylabel('Median Price ($)')
plt.legend()
plt.grid(True)

# Format x-axis
plt.gca().xaxis.set_major_locator(mdates.YearLocator(5))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# 2. Sales Volume Comparison
plt.subplot(4, 1, 2)
for city in df['City'].unique():
    city_data = df[df['City'] == city]
    plt.plot(city_data['Date'], city_data['Sales'], label=city)
plt.title('Monthly Sales Volume')
plt.ylabel('Number of Sales')
plt.legend()
plt.grid(True)

# 3. Months Inventory
plt.subplot(4, 1, 3)
for city in df['City'].unique():
    city_data = df[df['City'] == city]
    plt.plot(city_data['Date'], city_data['Months Inventory'], label=city)
plt.title('Months of Housing Inventory')
plt.ylabel('Months')
plt.legend()
plt.grid(True)

# 4. Year-over-Year Price Change
plt.subplot(4, 1, 4)
for city in df['City'].unique():
    city_data = df[df['City'] == city]
    plt.plot(city_data['Date'], city_data['Sales YoY%'], label=f'{city} Sales YoY%')
    plt.plot(city_data['Date'], city_data['Dollar Volume YoY%'], label=f'{city} Dollar Volume YoY%', linestyle='--')
plt.title('Year-over-Year Changes')
plt.ylabel('Percentage Change')
plt.legend()
plt.grid(True)

# Adjust layout and save
plt.tight_layout()
plt.savefig('texas_housing_analysis.png', dpi=300)
plt.show()

# Additional Analysis: Recent 5 Years Comparison
recent_data = df[df['Date'] >= '2021-01-01']

# Create a summary table of key metrics
summary_table = recent_data.groupby(['City', 'Year']).agg({
    'Median Price': 'mean',
    'Sales': 'sum',
    'Months Inventory': 'mean',
    'Sales YoY%': 'mean',
    'Dollar Volume YoY%': 'mean'
}).round(2)

print("
Recent 5 Years Summary Statistics:")
print(summary_table)

# Create a correlation heatmap for Wichita Falls
plt.figure(figsize=(10, 8))
corr_matrix = df_wichita[['Median Price', 'Sales', 'Active Listings EOM', 'Months Inventory']].corr()
plt.imshow(corr_matrix, cmap='coolwarm', interpolation='none')
plt.colorbar()
plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=45)
plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)
plt.title('Wichita Falls Housing Metrics Correlation')
plt.tight_layout()
plt.savefig('wichita_correlation.png', dpi=300)
plt.show()
