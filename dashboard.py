import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, date

# --- Page Configuration ---
st.set_page_config(
    page_title="HealthKart Influencer Marketing Dashboard",
    page_icon="💪",
    layout="wide"
)

# --- Data Loading (from Part 3) ---
@st.cache_data
def load_data():
    influencers_df = pd.read_csv("data/influencers.csv")
    posts_df = pd.read_csv("data/posts.csv")
    tracking_data_df = pd.read_csv("data/tracking_data.csv")
    payouts_df = pd.read_csv("data/payouts.csv")
    
    tracking_data_df['date'] = pd.to_datetime(tracking_data_df['date'])
    posts_df['date'] = pd.to_datetime(posts_df['date'])
    
    merged_data = pd.merge(tracking_data_df, influencers_df, on='influencer_id', how='left')
    
    brand_map = {
        "Whey Protein": "MuscleBlaze", "BCAA": "MuscleBlaze", "Creatine": "MuscleBlaze", "Mass Gainer": "MuscleBlaze",
        "Biotin": "HKVitals", "Multivitamin": "HKVitals", "Omega 3": "HKVitals", "Collagen": "HKVitals",
        "SuperMilk for Kids": "Gritzo", "Protein Oats for Teens": "Gritzo", "Gummy Stars": "Gritzo"
    }
    merged_data['brand'] = merged_data['product'].map(brand_map)
    
    final_df = pd.merge(merged_data, payouts_df, on='influencer_id', how='left')
    
    influencers_with_payouts = pd.merge(influencers_df, payouts_df, on='influencer_id', how='left')
    
    return final_df, posts_df, influencers_with_payouts

df, posts_df, influencers_df = load_data()

# --- Sidebar for Filters ---
st.sidebar.header("Filter Your Data")
min_date, max_date = df['date'].min().date(), df['date'].max().date()
date_range = st.sidebar.date_input("Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
start_date, end_date = date_range if len(date_range) == 2 else (date_range[0], date_range[0])
start_datetime, end_datetime = pd.to_datetime(start_date), pd.to_datetime(end_date) + pd.Timedelta(days=1)

selected_brands = st.sidebar.multiselect("Select Brands", options=sorted(df['brand'].unique()), default=sorted(df['brand'].unique()))
selected_categories = st.sidebar.multiselect("Select Influencer Category", options=sorted(df['category'].unique()), default=sorted(df['category'].unique()))

# --- Apply Filters ---
filtered_df = df[
    (df['date'] >= start_datetime) & (df['date'] < end_datetime) &
    (df['brand'].isin(selected_brands)) &
    (df['category'].isin(selected_categories))
]
relevant_influencer_ids = filtered_df['influencer_id'].unique()
filtered_influencers_df = influencers_df[influencers_df['influencer_id'].isin(relevant_influencer_ids)]

# --- Main Page ---
st.title("💪 HealthKart Influencer Marketing Dashboard")

# --- KPI Section ---
st.header("Campaign Performance Overview")
total_revenue = filtered_df['revenue'].sum()
total_orders = filtered_df['orders'].sum()
total_payout = filtered_influencers_df['total_payout'].sum()
roas = total_revenue / total_payout if total_payout > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Payout", f"₹{total_payout:,.0f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Overall ROAS", f"{roas:.2f}x")

st.markdown("---")

# --- <<< NEW: INFLUENCER INSIGHTS & ROAS ANALYSIS SECTION >>> ---
st.header("Influencer Insights & ROAS Analysis")

# Check if there is data after filtering
if not filtered_df.empty:
    # 1. Calculate revenue per influencer
    influencer_revenue = filtered_df.groupby('influencer_id')['revenue'].sum().reset_index()
    
    # 2. Merge with influencer details and payout info
    influencer_summary = pd.merge(influencer_revenue, filtered_influencers_df, on='influencer_id', how='left')
    
    # 3. Calculate ROAS
    influencer_summary['roas'] = influencer_summary['revenue'] / influencer_summary['total_payout']
    influencer_summary['roas'] = influencer_summary['roas'].fillna(0) # Handle cases with 0 payout

    # --- Display Insights ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Influencers by Revenue")
        top_revenue = influencer_summary.sort_values(by='revenue', ascending=False).head(10)
        fig_top_revenue = px.bar(
            top_revenue, x='revenue', y='name', orientation='h',
            labels={'revenue': 'Total Revenue (₹)', 'name': 'Influencer'},
            text='revenue'
        )
        fig_top_revenue.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
        fig_top_revenue.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top_revenue, use_container_width=True)

    with col2:
        st.subheader("Top Influencers by ROAS")
        top_roas = influencer_summary.sort_values(by='roas', ascending=False).head(10)
        fig_top_roas = px.bar(
            top_roas, x='roas', y='name', orientation='h',
            labels={'roas': 'Return on Ad Spend (ROAS)', 'name': 'Influencer'},
            text='roas'
        )
        fig_top_roas.update_traces(texttemplate='%{text:.2f}x', textposition='outside')
        fig_top_roas.update_layout(yaxis={'categoryorder':'total ascending'})
        # Add a line for break-even point
        fig_top_roas.add_vline(x=1.0, line_width=2, line_dash="dash", line_color="red")
        st.plotly_chart(fig_top_roas, use_container_width=True)
    
    st.info("""
        **About ROAS (Return on Ad Spend):**
        - **ROAS** = Revenue / Payout. It measures the return for every rupee spent.
        - A ROAS > 1.0 means the campaign is profitable (shown by the red dashed line).
        - This is a *direct* ROAS. True *incremental* ROAS would subtract baseline sales, but this is a strong indicator of performance.
    """, icon="💡")
    
    st.subheader("Detailed Influencer Performance")
    st.dataframe(influencer_summary[[
        'name', 'category', 'follower_count', 'revenue', 'total_payout', 'roas'
    ]].sort_values(by='revenue', ascending=False).style.format({
        'revenue': '₹{:,.2f}',
        'total_payout': '₹{:,.2f}',
        'roas': '{:.2f}x'
    }))

else:
    st.warning("No data available for the selected filters. Please expand your selection.")

st.markdown("---")

# --- <<< NEW: VISUALIZATION SECTION >>> ---
st.header("Visual Insights")

# --- Chart 1: Revenue Over Time ---
st.subheader("Daily Revenue Trend")
# Resample data by day to get daily revenue. 'D' stands for daily frequency.
daily_revenue = filtered_df.set_index('date').resample('D')['revenue'].sum().reset_index()
fig_daily_revenue = px.line(
    daily_revenue,
    x='date',
    y='revenue',
    title="Daily Revenue",
    labels={'revenue': 'Total Revenue (₹)', 'date': 'Date'}
)
fig_daily_revenue.update_layout(title_x=0.5, xaxis_title=None, yaxis_title="Revenue (₹)")
st.plotly_chart(fig_daily_revenue, use_container_width=True)


# --- Chart 2 & 3: Performance by Brand and Category ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Brand")
    brand_revenue = filtered_df.groupby('brand')['revenue'].sum().sort_values(ascending=False).reset_index()
    fig_brand_revenue = px.bar(
        brand_revenue,
        x='brand',
        y='revenue',
        color='brand',
        title="Total Revenue per Brand",
        labels={'revenue': 'Total Revenue (₹)', 'brand': 'Brand'}
    )
    fig_brand_revenue.update_layout(title_x=0.5, showlegend=False)
    st.plotly_chart(fig_brand_revenue, use_container_width=True)

with col2:
    st.subheader("Revenue by Influencer Category")
    category_revenue = filtered_df.groupby('category')['revenue'].sum().sort_values(ascending=False).reset_index()
    fig_category_revenue = px.bar(
        category_revenue,
        x='category',
        y='revenue',
        color='category',
        title="Total Revenue per Influencer Category",
        labels={'revenue': 'Total Revenue (₹)', 'category': 'Category'}
    )
    fig_category_revenue.update_layout(title_x=0.5, showlegend=False)
    st.plotly_chart(fig_category_revenue, use_container_width=True)


# --- <<< NEW: PAYOUT TRACKING SECTION >>> ---
st.header("Payout Tracking")
# Use the filtered_influencers_df which already contains the relevant influencers for the period
payout_tracking_df = filtered_influencers_df[['name', 'basis', 'rate', 'total_orders_by_influencer', 'total_payout']]
st.dataframe(payout_tracking_df)