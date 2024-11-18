import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
customers = pd.read_csv('data/customers_dataset.csv')
order_items = pd.read_csv('data/order_items_dataset.csv')
orders = pd.read_csv('data/orders_dataset.csv')
products = pd.read_csv('data/products_dataset.csv')
product_category_translation = pd.read_csv('data/product_category_name_translation.csv')

# Merge datasets
merged_data = pd.merge(order_items, orders, on='order_id', how='inner')
merged_data = pd.merge(merged_data, products, on='product_id', how='inner')
merged_data = pd.merge(merged_data, product_category_translation, on='product_category_name', how='left')

# Data cleaning
merged_data = merged_data.drop_duplicates()

# Streamlit dashboard
st.title("Interactive Data Analysis Dashboard")

# Sidebar for filtering
st.sidebar.header("Filter Options")
category_filter = st.sidebar.multiselect(
    "Select Product Categories",
    options=merged_data['product_category_name_english'].unique(),
    default=merged_data['product_category_name_english'].unique()
)

filtered_data = merged_data[merged_data['product_category_name_english'].isin(category_filter)]

# Visualization 1: Top Product Categories
st.header("Top Purchased Product Categories")
category_counts = filtered_data['product_category_name_english'].value_counts().head(10)

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x=category_counts.values, y=category_counts.index, ax=ax1, palette='viridis')
ax1.set_title('Top 10 Purchased Product Categories')
ax1.set_xlabel('Number of Purchases')
ax1.set_ylabel('Category')
st.pyplot(fig1)

# Delivery time calculation
filtered_data['delivery_time'] = (
    pd.to_datetime(filtered_data['order_delivered_customer_date']) -
    pd.to_datetime(filtered_data['order_purchase_timestamp'])
).dt.days

filtered_data['estimated_time'] = (
    pd.to_datetime(filtered_data['order_estimated_delivery_date']) -
    pd.to_datetime(filtered_data['order_purchase_timestamp'])
).dt.days

# Visualization 2: Delivery Time vs Estimated Time
st.header("Actual vs Estimated Delivery Time")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.histplot(filtered_data['delivery_time'], color='blue', kde=True, label='Actual Delivery Time', ax=ax2)
sns.histplot(filtered_data['estimated_time'], color='orange', kde=True, label='Estimated Delivery Time', ax=ax2)
ax2.legend()
ax2.set_title('Actual vs Estimated Delivery Time')
ax2.set_xlabel('Days')
ax2.set_ylabel('Frequency')
st.pyplot(fig2)

# Data Table
st.header("Filtered Data Preview")
st.dataframe(filtered_data.head(20))

st.markdown("### Conclusions")
st.markdown("- **Top Purchased Categories**: The most purchased categories include household items and health-related products.")
st.markdown("- **Delivery Analysis**: Most deliveries are faster than the estimated delivery time, although a few outliers exist.")
