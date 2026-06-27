import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Mutual Fund Analytics Dashboard",
    page_icon="📈",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main{
    background-color:#0e1117;
}

h1,h2,h3,h4{
    color:white;
}

[data-testid="metric-container"]{
    background:#1e293b;
    padding:18px;
    border-radius:12px;
    border:1px solid #30363d;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "bluestock_mf.db"

conn = sqlite3.connect(DB_PATH)
nav_df = pd.read_sql(
    "SELECT * FROM nav_history",
    conn
)

nav_df["date"] = pd.to_datetime(nav_df["date"])
# Load Performance Table
performance_df = pd.read_sql(
    "SELECT amfi_code, scheme_name FROM performance",
    conn
)

# Remove duplicate AMFI codes
performance_df = performance_df.drop_duplicates(subset="amfi_code")

# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------

st.title("📈 Mutual Fund Analytics Dashboard")

st.write(
    "Interactive dashboard for analysing Mutual Fund NAV data."
)

st.markdown("---")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("📊 Dashboard Filters")
st.sidebar.markdown("---")

# Merge NAV data with scheme names
fund_list = pd.merge(
    nav_df[["amfi_code"]].drop_duplicates(),
    performance_df,
    on="amfi_code",
    how="left"
)

fund_list["display"] = (
    fund_list["scheme_name"]
    .fillna(fund_list["amfi_code"].astype(str))
)

selected_display = st.sidebar.selectbox(
    "Select Mutual Fund",
    sorted(fund_list["display"])
)

selected_fund = fund_list.loc[
    fund_list["display"] == selected_display,
    "amfi_code"
].values[0]

# ---------------------------------------------------
# DATE FILTER
# ---------------------------------------------------

min_date = nav_df["date"].min().date()
max_date = nav_df["date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

filtered_df = nav_df[
    nav_df["amfi_code"] == selected_fund
]

if len(selected_dates) == 2:

    start_date, end_date = selected_dates

    filtered_df = filtered_df[
        (filtered_df["date"] >= pd.to_datetime(start_date))
        &
        (filtered_df["date"] <= pd.to_datetime(end_date))
    ]

# ---------------------------------------------------
# SIDEBAR INFO
# ---------------------------------------------------

st.sidebar.success("Dashboard Loaded Successfully ✅")

st.sidebar.info(
f"""
### Selected Fund

**{selected_display}**
Records :

**{len(filtered_df)}**
"""
)

st.markdown("---")
# ---------------------------------------------------
# DASHBOARD OVERVIEW
# ---------------------------------------------------

st.header("📊 Dashboard Overview")

total_records = len(filtered_df)
average_nav = filtered_df["nav"].mean()
maximum_nav = filtered_df["nav"].max()
minimum_nav = filtered_df["nav"].min()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📄 Total Records",
        f"{total_records:,}"
    )

with col2:
    st.metric(
        "📈 Average NAV",
        f"₹ {average_nav:.2f}"
    )

with col3:
    st.metric(
        "🚀 Maximum NAV",
        f"₹ {maximum_nav:.2f}"
    )

with col4:
    st.metric(
        "📉 Minimum NAV",
        f"₹ {minimum_nav:.2f}"
    )

st.markdown("---")
st.markdown("---")

st.subheader("📊 Average NAV Gauge")

fig_gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=average_nav,
        title={"text": "Average NAV"},
        gauge={
            "axis": {"range": [0, maximum_nav + 50]},
            "bar": {"color": "limegreen"},
            "steps": [
                {"range": [0, average_nav], "color": "lightgray"}
            ],
        },
    )
)

fig_gauge.update_layout(
    template="plotly_dark",
    height=400
)

st.plotly_chart(
    fig_gauge,
    use_container_width=True
)
# ---------------------------------------------------
# NAV TREND
# ---------------------------------------------------

st.subheader("📈 NAV Trend")

fig_nav = px.line(
    filtered_df,
    x="date",
    y="nav",
    markers=True,
    title=f"NAV Trend - Fund {selected_fund}"
)

fig_nav.update_layout(
    template="plotly_dark",
    title_x=0.5,
    height=500,
    xaxis_title="Date",
    yaxis_title="NAV"
)

fig_nav.update_traces(
    line=dict(width=3),
    marker=dict(size=5)
)

st.plotly_chart(
    fig_nav,
    use_container_width=True,
    key="nav_trend"
)

st.markdown("---")

# ---------------------------------------------------
# 30-DAY MOVING AVERAGE
# ---------------------------------------------------

st.subheader("📉 30-Day Moving Average")

ma_df = filtered_df.copy()

ma_df["30 Day MA"] = (
    ma_df["nav"]
    .rolling(window=30)
    .mean()
)

fig_ma = go.Figure()

fig_ma.add_trace(
    go.Scatter(
        x=ma_df["date"],
        y=ma_df["nav"],
        mode="lines",
        name="NAV"
    )
)

fig_ma.add_trace(
    go.Scatter(
        x=ma_df["date"],
        y=ma_df["30 Day MA"],
        mode="lines",
        name="30-Day MA"
    )
)

fig_ma.update_layout(
    template="plotly_dark",
    title="NAV vs 30-Day Moving Average",
    title_x=0.5,
    height=500,
    xaxis_title="Date",
    yaxis_title="NAV"
)

st.plotly_chart(
    fig_ma,
    use_container_width=True,
    key="moving_average"
)

st.markdown("---")
# ---------------------------------------------------
# MONTHLY AVERAGE NAV
# ---------------------------------------------------

st.subheader("📅 Monthly Average NAV")

monthly_df = (
    filtered_df
    .set_index("date")
    .resample("ME")["nav"]
    .mean()
    .reset_index()
)

fig_month = px.bar(
    monthly_df,
    x="date",
    y="nav",
    title="Monthly Average NAV"
)

fig_month.update_layout(
    template="plotly_dark",
    title_x=0.5,
    height=500,
    xaxis_title="Month",
    yaxis_title="Average NAV"
)

st.plotly_chart(
    fig_month,
    use_container_width=True,
    key="monthly_average_nav"
)

st.markdown("---")

# ---------------------------------------------------
# NAV DISTRIBUTION
# ---------------------------------------------------

st.subheader("📊 NAV Distribution")

fig_hist = px.histogram(
    filtered_df,
    x="nav",
    nbins=30,
    title="Distribution of NAV Values"
)

fig_hist.update_layout(
    template="plotly_dark",
    title_x=0.5,
    height=500,
    xaxis_title="NAV",
    yaxis_title="Count"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True,
    key="nav_distribution_histogram"
)

st.markdown("---")

# ---------------------------------------------------
# BOX PLOT
# ---------------------------------------------------

st.subheader("📦 NAV Box Plot")

fig_box = px.box(
    filtered_df,
    y="nav",
    title="NAV Spread and Outliers"
)

fig_box.update_layout(
    template="plotly_dark",
    title_x=0.5,
    height=500
)

st.plotly_chart(
    fig_box,
    use_container_width=True,
    key="nav_box_plot"
)

st.markdown("---")
st.markdown("---")

st.subheader("📍 NAV Scatter Plot")

fig_scatter = px.scatter(
    filtered_df,
    x="date",
    y="nav",
    color="nav",
    title="NAV Scatter Plot"
)

fig_scatter.update_layout(
    template="plotly_dark",
    title_x=0.5,
    height=500
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)
# ---------------------------------------------------
# SUMMARY STATISTICS
# ---------------------------------------------------

st.subheader("📋 Summary Statistics")

summary_df = filtered_df["nav"].describe().reset_index()
summary_df.columns = ["Statistic", "Value"]

st.dataframe(
    summary_df,
    use_container_width=True
)

st.markdown("---")
# ---------------------------------------------------
# DOWNLOAD FILTERED DATA
# ---------------------------------------------------

st.subheader("📥 Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name=f"mutual_fund_{selected_fund}.csv",
    mime="text/csv"
)

st.markdown("---")

# ---------------------------------------------------
# COMPLETE DATA TABLE
# ---------------------------------------------------

st.subheader("📋 Complete Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)

st.markdown("---")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown(
    """
    <hr>

    <div style='text-align:center; color:gray;'>

    <h3>📈 Mutual Fund Analytics Dashboard</h3>

    <p>
    Built with ❤️ using <b>Python</b>, <b>Streamlit</b>,
    <b>Plotly</b> and <b>SQLite</b>
    </p>

    <p>
    Internship Project 2026
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# CLOSE DATABASE
# ---------------------------------------------------

conn.close()