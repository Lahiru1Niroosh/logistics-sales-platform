import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards

# --- 1. THE ARCHITECTURE ---
st.set_page_config(page_title="DHL | Global Intelligence", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE "GLASS" UI ENGINE (Custom CSS) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    
    /* Custom Card Containers */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }
    
    /* Header Styling */
    h1 { font-family: 'Inter', sans-serif; font-weight: 900; letter-spacing: -2px; color: #FFCC00; text-shadow: 2px 2px 10px rgba(0,0,0,0.5); }
    h3 { color: #ffffff; font-weight: 300; opacity: 0.8; }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA & SIMULATION ---
con = duckdb.connect('data/logistics_warehouse.duckdb')

with st.sidebar:
    st.markdown("## ⚙️ SIMULATION ENGINE")
    fuel_adj = st.slider("Fuel Market Volatility ($)", 0, 100, 22)
    vol_adj = st.slider("Demand Surge (%)", -30, 30, 0)
    st.divider()
    st.markdown("### 🛠️ Strategic Overrides")
    st.checkbox("Enable AI Capacity Balancing", value=True)

# Calculation Logic
sim_query = f"""
    SELECT region, 
           SUM(revenue * (1 + {vol_adj/100})) as rev, 
           SUM(profit - ({fuel_adj} * 0.12)) as prof
    FROM fact_shipments GROUP BY 1
"""
df = con.execute(sim_query).df()
df['margin'] = (df['prof'] / df['rev']) * 100

# --- 4. EXECUTIVE KPI ROW ---
st.title("📦 DHL GLOBAL COMMAND")
st.markdown("### STRATEGIC OPERATIONS DASHBOARD • 2026 Q1")

m1, m2, m3, m4 = st.columns(4)
m1.metric("EST. QUARTERLY REVENUE", f"${df['rev'].sum()/1e6:.1f}M", "+4.2%")
m2.metric("NET OPERATING PROFIT", f"${df['prof'].sum()/1e6:.2f}M", "-1.8%", delta_color="inverse")
m3.metric("SYSTEM-WIDE MARGIN", f"{df['margin'].mean():.1f}%")
m4.metric("SLA COMPLIANCE", "98.4%", "0.4%")

style_metric_cards(background_color="rgba(255,255,255,0)", border_left_color="#D40511", border_size_px=0)

st.write("") # Spacer

# --- 5. THE "NEXT LEVEL" VISUALS ---
row2_col1, row2_col2 = st.columns([1.5, 1])

with row2_col1:
    st.markdown("#### 🌍 REAL-TIME MARGIN EFFICIENCY")
    fig = px.bar(df, x='region', y='margin', color='margin',
                 color_continuous_scale=[[0, '#3e0000'], [0.5, '#FFCC00'], [1, '#00ff00']],
                 template="plotly_dark", barmode='group')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      margin=dict(l=0, r=0, t=0, b=0), height=350)
    st.plotly_chart(fig, use_container_width=True)

with row2_col2:
    st.markdown("#### 📊 GLOBAL PROFIT TARGET")
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = df['margin'].mean(),
        delta = {'reference': 45},
        gauge = {
            'axis': {'range': [None, 60]},
            'bar': {'color': "#D40511"},
            'bgcolor': "rgba(255,255,255,0.1)",
            'threshold': {'line': {'color': "white", 'width': 4}, 'value': 45}
        }
    ))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=350, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

# --- 6. PREDICTIVE LAYER ---
st.markdown("#### 🔮 30-DAY PREDICTIVE CAPACITY LOAD")
st.image('data/shipment_forecast.png', use_container_width=True)