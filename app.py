import streamlit as st
import requests
import os
from dotenv import load_dotenv

# -----------------------------
# Load API Key from .env
# -----------------------------
load_dotenv()
API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_URL = "https://v6.exchangerate-api.com/v6"

# -----------------------------
# Functions
# -----------------------------
def get_exchange_rate(base, target):
    """Fetch exchange rate for base -> target"""
    url = f"{BASE_URL}/{API_KEY}/latest/{base}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["conversion_rates"].get(target)
    else:
        return None

@st.cache_data(ttl=60)
def get_currencies():
    """Fetch supported currencies from API"""
    url = f"{BASE_URL}/{API_KEY}/codes"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["supported_codes"]
    else:
        return []

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Currency Converter", page_icon="💱")
st.title("💱 Currency Converter")

# Load currency list
currencies = get_currencies()
if not currencies:
    st.error("Cannot load currency list. Check API key.")
    st.stop()

# Make dropdown dictionary
currency_dict = {f"{code} - {name}": code for code, name in currencies}

# Columns for dropdowns
col1, col2 = st.columns(2)
with col1:
    base_select = st.selectbox("From", currency_dict.keys())
with col2:
    target_select = st.selectbox("To", currency_dict.keys())

# Amount input
amount = st.number_input("Amount", min_value=0.0, step=1.0)

# Convert button
if st.button("Convert"):
    base = currency_dict[base_select]
    target = currency_dict[target_select]

    rate = get_exchange_rate(base, target)

    if rate:
        converted = amount * rate
        inverse_rate = 1 / rate

        # Show conversion
        st.markdown(f"### {amount} {base} = {converted:.2f} {target}")
        # Show current rate
        st.info(f"💱 Current rate: 1 {base} = {rate:.6f} {target}")
        # Show inverse rate
        st.info(f"🔄 Inverse rate: 1 {target} = {inverse_rate:.6f} {base}")
    else:
        st.error("Could not fetch exchange rate. Try again.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("© 2026 Managed by Tadiwa Muchuchuti")