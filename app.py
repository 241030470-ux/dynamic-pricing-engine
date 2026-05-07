import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import streamlit as st

st.set_page_config(
    page_title="AI Dynamic Pricing Engine",
    layout="wide"
)

st.markdown("""
<h1 style='text-align:center; color:#4CAF50;'>
💰 AI-Powered Dynamic Pricing Dashboard
</h1>
<hr>
""", unsafe_allow_html=True)

st.sidebar.title("⚙ Pricing Controls")

hour = st.sidebar.slider("Select Hour", 0, 23, 12)

day = st.sidebar.slider(
    "Select Day (0=Mon, 6=Sun)",
    0,
    6,
    3
)

min_price = st.sidebar.slider(
    "Minimum Price",
    50,
    150,
    50
)

max_price = st.sidebar.slider(
    "Maximum Price",
    100,
    300,
    200
)

np.random.seed(42)

data = []

for hour_data in range(24):
    for day_data in range(7):

        demand = 50

        if day_data >= 5:
            demand += 10

        if 18 <= hour_data <= 22:
            demand += 5

        demand += np.random.randint(-5, 5)

        data.append([hour_data, day_data, demand])

df = pd.DataFrame(
    data,
    columns=["hour", "day", "demand"]
)

X = df[["hour", "day"]]
y = df["demand"]

model = LinearRegression()
model.fit(X, y)

input_df = pd.DataFrame(
    [[hour, day]],
    columns=["hour", "day"]
)

pred_demand = model.predict(input_df)[0]

st.subheader("📢 Demand Status")

if pred_demand > 60:
    st.warning("🔥 High Demand Period Detected")
elif pred_demand < 45:
    st.info("📉 Low Demand Period")
else:
    st.success("✅ Moderate Demand")

prices = np.arange(min_price, max_price, 5)

competitor_price = 120 + np.random.randint(-15, 15)

adjusted_demand = pred_demand - 0.2 * (prices - 100)

adjusted_demand = np.maximum(adjusted_demand, 0)

revenues = prices * adjusted_demand

best_price = prices[np.argmax(revenues)]

best_revenue = max(revenues)

if pred_demand > 60:
    final_price = max(best_price, competitor_price + 5)
else:
    final_price = min(best_price, competitor_price - 5)

static_price = 100
static_revenue = static_price * pred_demand

improvement = (
    (best_revenue - static_revenue)
    / static_revenue
) * 100

st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Predicted Demand",
    f"{int(pred_demand)} units"
)

col2.metric(
    "Optimal Price",
    f"₹{int(best_price)}"
)

col3.metric(
    "Competitor Price",
    f"₹{competitor_price}"
)

col4.metric(
    "Revenue Improvement",
    f"{improvement:.2f}%"
)

st.subheader("💡 Final AI Suggested Price")

st.success(
    f"Recommended Dynamic Price: ₹{int(final_price)}"
)

st.subheader("📈 Revenue vs Price")

chart_data = pd.DataFrame({
    "Price": prices,
    "Revenue": revenues
})

st.line_chart(
    chart_data.set_index("Price")
)

st.subheader("📉 Demand vs Price")

chart_data2 = pd.DataFrame({
    "Price": prices,
    "Demand": adjusted_demand
})

st.line_chart(
    chart_data2.set_index("Price")
)

st.subheader("🗂 Sample Dataset")

st.dataframe(df.head(10))

st.info("""
This AI-powered system predicts demand using Linear Regression
and dynamically selects optimal prices using revenue optimization,
price elasticity, and competitor-aware pricing strategies.
""")