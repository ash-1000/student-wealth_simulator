import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

# ---------- PAGE ----------
st.set_page_config(page_title="Wealth Simulator", layout="wide")

st.title("💰 Student Wealth Simulator")
st.write("Build a smart portfolio, understand risk, and explore real market data.")

# ---------- USER INPUT ----------
st.header("👤 Your Details")

age = st.slider("Your Age", 18, 40, 20)
monthly = st.slider("Monthly Investment (₹)", 500, 50000, 2000)
years = st.slider("Investment Duration (Years)", 1, 30, 10)

# ---------- STOCK OPTIONS ----------
stock_options = {
    "Apple (AAPL)": "AAPL",
    "Tesla (TSLA)": "TSLA",
    "Microsoft (MSFT)": "MSFT",
    "Amazon (AMZN)": "AMZN",
    "Google (GOOGL)": "GOOGL",
    "S&P 500": "^GSPC",
    "NIFTY 50": "^NSEI",
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS"
}

# ---------- PORTFOLIO ----------
st.header("📊 Build Your Portfolio (Total = 100%)")

selected = st.multiselect(
    "Choose stocks",
    list(stock_options.keys())
)

weights = {}
total = 0
valid = False

for name in selected:
    ticker = stock_options[name]
    weights[ticker] = st.slider(f"{name} (%)", 0, 100, 0)
    total += weights[ticker]

st.write(f"### Total Allocation: {total}%")

if total == 100 and len(weights) > 0:
    valid = True
    st.success("Portfolio is valid ✅")
else:
    st.warning("Total must equal 100%")

# ---------- PIE CHART ----------
if valid:
    st.subheader("📈 Portfolio Distribution")

    fig, ax = plt.subplots()
    ax.pie(weights.values(), labels=weights.keys(), autopct="%1.1f%%")
    ax.axis("equal")
    st.pyplot(fig)

# ---------- WEALTH GROWTH ----------
st.header("📊 Wealth Growth")

rate = 0.12 if age < 25 else 0.10 if age < 30 else 0.08

value = 0
values = []

for i in range(years * 12):
    value = value * (1 + rate / 12) + monthly
    values.append(value)

st.line_chart(values)
st.subheader(f"💰 Final Wealth: ₹{int(value):,}")

# ---------- ADVICE ----------
st.header("🧠 Portfolio Insight")

if valid:
    predictable = ["^GSPC", "^NSEI"]
    has_index = any(stock in predictable for stock in weights)

    if has_index:
        st.success("📊 Includes Index Funds")
        st.markdown("""
        Your portfolio includes index funds like the S&P 500 or NIFTY 50. 
        These are generally more stable and provide consistent long-term returns.
        """)

    st.warning("⚠️ Individual Stocks Included")
    st.markdown("""
    Individual stocks are unpredictable and depend on market conditions, 
    company performance, and global factors. They may provide high returns, 
    but also come with higher risk.
    """)

    st.info("📌 Important Note")
    st.markdown("""
    This tool provides estimates based on general trends. 
    Markets are uncertain, and actual returns may vary significantly.
    Always make informed decisions.
    """)

# ---------- STOCK EXPLORER ----------
st.header("📉 Explore Stock Performance")

single = st.selectbox(
    "Select a stock to view performance",
    list(stock_options.keys())
)

ticker = stock_options[single]
data = yf.download(ticker, period="1y")

if not data.empty:
    st.line_chart(data["Close"])

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Created by Aashritha G Y | Educational use only. Not financial advice.")
