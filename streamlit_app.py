import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="SPY Pressure Radar",
    page_icon="📡",
    layout="centered"
)

st.title("📡 SPY Pressure Radar")
st.caption("Modelo Victoria · Research Dashboard")

# ----- DEMO DATA -----
np.random.seed(7)
n = 60

price = 550 + np.cumsum(np.random.normal(0, 0.15, n))
volume = np.random.randint(100000, 700000, n)

df = pd.DataFrame({
    "Price": price,
    "Volume": volume
})

change = df["Price"].diff().fillna(0)

buyer_move = change.clip(lower=0).sum()
seller_move = (-change.clip(upper=0)).sum()

up_volume = df.loc[change > 0, "Volume"].sum()
down_volume = df.loc[change < 0, "Volume"].sum()

buyer_eff = buyer_move / max(up_volume / 1_000_000, 0.01)
seller_eff = seller_move / max(down_volume / 1_000_000, 0.01)

buyer_votes = 0
seller_votes = 0

if buyer_eff > seller_eff:
    buyer_votes += 1
else:
    seller_votes += 1

last5 = change.tail(5).sum()

if last5 > 0:
    buyer_votes += 1
elif last5 < 0:
    seller_votes += 1

if buyer_votes > seller_votes:
    state = "BUYER evidence leads"
elif seller_votes > buyer_votes:
    state = "SELLER evidence leads"
else:
    state = "MIXED / no clear edge"

st.subheader(state)

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Buyer Efficiency",
        f"{buyer_eff:.2f}"
    )

with c2:
    st.metric(
        "Seller Efficiency",
        f"{seller_eff:.2f}"
    )

st.line_chart(df["Price"])

st.subheader("Evidence")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Buyer votes",
        buyer_votes
    )

with c2:
    st.metric(
        "Seller votes",
        seller_votes
    )

st.warning(
    "DEMO / UNCALIBRATED — todavía no genera señales CALL/PUT."
)

st.caption(
    "Siguiente fase: conectar SPY 1-minute data y validar "
    "Efficiency, Counterattack, Opportunity Failure y Time Pressure."
)
