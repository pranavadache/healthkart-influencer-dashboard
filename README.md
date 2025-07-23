# HealthKart Influencer Marketing Dashboard

> An interactive web-based dashboard built with Streamlit to track, visualize, and analyze the performance and ROI of influencer marketing campaigns.

This project simulates real-world data for HealthKart's influencer campaigns and provides a powerful tool for marketing managers to derive insights, track payouts, and measure the financial return of their efforts.

---

## ✨ Key Features

*   **📈 Campaign Performance KPIs:** At-a-glance metrics for Total Revenue, Total Payout, Total Orders, and overall Return on Ad Spend (ROAS).
*   **🔪 Interactive Filtering:** Dynamically filter the entire dashboard by date range, brand (MuscleBlaze, HKVitals, Gritzo), and influencer category (Fitness, Wellness, etc.).
*   **📊 Rich Visualizations:**
    *   Daily revenue trend line chart.
    *   Bar charts comparing revenue by brand and influencer category.
    *   Horizontal bar charts identifying the Top 10 influencers by revenue generated and by ROAS.
*   **💰 ROAS Analysis:** Calculates and visualizes ROAS for each influencer, with a clear break-even line to instantly identify profitable partnerships.
*   **🧾 Payout Tracking:** A clear table summarizing payout details for all filtered influencers, including their payment basis (per-post or per-order) and total payout.

---

## 🛠️ Tech Stack

*   **Backend & Dashboard:** Python, Streamlit
*   **Data Manipulation:** Pandas
*   **Data Visualization:** Plotly Express
*   **Data Simulation:** Faker

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

*   Python 3.8+
*   A Git client
*   A GitHub account

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    # Replace with your repository URL
    git clone https://github.com/your-username/healthkart-influencer-dashboard.git
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd healthkart-influencer-dashboard
    ```

3.  **Install the required dependencies:**
    *(It is highly recommended to use a Python virtual environment)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Generate the simulated data:**
    This script creates the four CSV files needed to run the dashboard.
    ```bash
    python generate_data.py
    ```

5.  **Run the Streamlit application:**
    ```bash
    streamlit run dashboard.py
    ```
    Your web browser should automatically open with the dashboard running!

---

## 🗂️ Data Modeling

The dashboard is powered by four interconnected CSV files located in the `/data` directory.

1.  **`influencers.csv`**: Contains details about each influencer.
    *   `influencer_id`, `name`, `category`, `gender`, `follower_count`, `platform`

2.  **`posts.csv`**: Contains data for each post made by an influencer.
    *   `post_id`, `influencer_id`, `platform`, `date`, `url`, `caption`, `reach`, `likes`, `comments`

3.  **`tracking_data.csv`**: Simulates user transaction data attributed to influencers.
    *   `tracking_id`, `source`, `campaign`, `influencer_id`, `user_id`, `product`, `date`, `orders`, `revenue`

4.  **`payouts.csv`**: Contains payout information for each influencer.
    *   `influencer_id`, `basis` (per_post/per_order), `rate`, `total_orders_by_influencer`, `total_payout`

---

## 📝 Assumptions & Limitations

This project demonstrates strong analytical capabilities but relies on a few key assumptions:

*   **Attribution Model:** The model uses a simple "last-touch" attribution. Any sale tracked via an influencer link is 100% credited to that influencer.
*   **Incrementality:** The dashboard calculates **Direct ROAS** (`Revenue / Payout`). It does not calculate **Incremental ROAS**, which would require control groups to subtract baseline sales that would have happened anyway. Direct ROAS is a strong performance indicator but not a measure of true incrementality.
*   **Static Data:** The data is generated once and is static. In a real-world scenario, this would be connected to a live database (e.g., SQL, BigQuery) or data source (e.g., Google Analytics).

---

## 📈 Potential Future Improvements

*   **Connect to a Live Database:** Replace the CSV files with a connection to a SQL database or a data warehouse for real-time analytics.
*   **Export Functionality:** Add buttons to export filtered data tables and charts as CSV or PDF files.
*   **Advanced Attribution:** Incorporate more complex attribution models (e.g., time-decay, multi-touch) for a more nuanced view of performance.
*   **User Authentication:** Add a login system to control access to the dashboard.