import os
from datetime import datetime

import duckdb
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="DHL | Global Intelligence", layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #111315;
        --bg-2: #191b1f;
        --panel: #181b1f;
        --panel-alt: #22252b;
        --panel-soft: #202329;
        --border: rgba(231, 222, 207, 0.16);
        --border-strong: rgba(255, 177, 74, 0.34);
        --text: #f8f3ea;
        --text-soft: #d8d0c4;
        --muted: #aaa298;
        --red: #ff625f;
        --green: #42d392;
        --amber: #ffd166;
        --orange: #ff9f43;
        --blue: #5da9ff;
        --cyan: #35c9c1;
        --purple: #b18cff;
        --indigo: #8585ff;
        --shadow: rgba(0, 0, 0, 0.48);
    }

    html, body, [data-testid="stApp"] {
        background: #111315;
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        position: relative;
        isolation: isolate;
        min-height: 100vh;
        height: 100vh;
        overflow: hidden;
        background: #070a12;
    }

    [data-testid="stAppViewContainer"] {
        position: relative;
        z-index: 1;
        min-height: 100vh !important;
        height: 100vh !important;
    }

    [data-testid="stMain"] {
        min-height: 100vh !important;
    }

    .stApp::before {
        content: "";
        position: fixed;
        z-index: 0;
        inset: 0;
        pointer-events: none;
        opacity: 0.78;
        background:
            radial-gradient(ellipse at 78% 18%, rgba(124, 92, 220, 0.24), transparent 34%),
            radial-gradient(ellipse at 16% 78%, rgba(32, 119, 186, 0.2), transparent 38%),
            radial-gradient(ellipse at 52% 46%, rgba(255, 98, 95, 0.1), transparent 30%),
            conic-gradient(from 210deg at 55% 48%, rgba(255, 98, 95, 0.12), rgba(255, 159, 67, 0.1), rgba(255, 209, 102, 0.08), rgba(66, 211, 146, 0.1), rgba(93, 169, 255, 0.12), rgba(177, 140, 255, 0.13), rgba(255, 98, 95, 0.12));
        background-size: 125% 125%, 135% 135%, 115% 115%, 180% 180%;
        background-blend-mode: screen;
        animation: nebula-drift 22s ease-in-out infinite alternate;
    }

    .stApp::after {
        content: "";
        position: fixed;
        z-index: 0;
        inset: 0;
        pointer-events: none;
        opacity: 0.72;
        background-image:
            radial-gradient(circle, rgba(255, 255, 255, 0.9) 0 1px, transparent 1.5px),
            radial-gradient(circle, rgba(143, 193, 255, 0.72) 0 1px, transparent 1.5px),
            radial-gradient(circle, rgba(255, 209, 102, 0.64) 0 1px, transparent 1.5px);
        background-size: 93px 93px, 151px 151px, 197px 197px;
        background-position: 0 0, 41px 67px, 89px 17px;
        animation: star-drift 30s linear infinite;
    }

    @keyframes nebula-drift {
        0% { background-position: 0% 0%, 100% 100%, 50% 40%, 0% 50%; transform: scale(1) rotate(0deg); }
        100% { background-position: 14% 10%, 82% 88%, 42% 58%, 100% 45%; transform: scale(1.08) rotate(3deg); }
    }

    @keyframes star-drift {
        from { background-position: 0 0, 41px 67px, 89px 17px; }
        to { background-position: 93px 93px, -110px 151px, 197px -197px; }
    }

    @media (prefers-reduced-motion: reduce) {
        .stApp::before, .stApp::after { animation: none; }
    }

    .main .block-container {
        position: relative;
        z-index: 1;
        max-width: 1560px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        position: relative;
        z-index: 1;
        background: linear-gradient(135deg, rgba(24, 27, 31, 0.97), rgba(31, 32, 35, 0.97));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1rem 1.2rem;
        box-shadow: 0 14px 30px var(--shadow);
    }

    .eyebrow {
        color: var(--muted);
        font-size: 10px;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        font-weight: 700;
    }

    .title {
        margin: 0.2rem 0 0;
        font-size: clamp(1.5rem, 2.1vw, 2.25rem);
        font-weight: 800;
        letter-spacing: -0.05em;
        color: var(--text);
    }

    .subtitle {
        margin: 0.25rem 0 0;
        color: var(--text-soft);
        font-size: 0.78rem;
    }

    .header-meta {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 0.7rem;
        flex-wrap: wrap;
    }

    .meta-box {
        min-width: 120px;
        padding: 0.55rem 0.7rem;
        border: 1px solid var(--border);
        background: rgba(34, 35, 37, 0.94);
        border-radius: 10px;
    }

    .meta-label {
        display: block;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 9px;
        font-weight: 700;
    }

    .meta-value {
        display: block;
        margin-top: 0.2rem;
        color: var(--text);
        font-size: 0.8rem;
        font-weight: 700;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.45rem 0.7rem;
        border-radius: 999px;
        background: rgba(44, 212, 159, 0.12);
        border: 1px solid rgba(44, 212, 159, 0.3);
        color: var(--green);
        font-size: 10px;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-weight: 700;
    }

    .status-pill::before {
        content: "";
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--green);
        box-shadow: 0 0 0 5px rgba(44, 212, 159, 0.16);
    }

    .section-label {
        margin-bottom: 0.55rem;
        color: var(--muted);
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    [data-testid="stTabs"] {
        position: relative;
        z-index: 1;
    }

    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 0.35rem;
        border-bottom: 1px solid rgba(231, 222, 207, 0.14);
        margin-bottom: 1.1rem;
    }

    [data-testid="stTabs"] button[role="tab"] {
        min-height: 2.4rem;
        padding: 0.55rem 0.9rem;
        border-radius: 9px 9px 0 0;
        color: var(--muted);
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
    }

    [data-testid="stTabs"] button[role="tab"]:hover {
        color: var(--text);
        background: rgba(255, 255, 255, 0.05);
    }

    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: var(--amber);
        background: rgba(255, 209, 102, 0.08);
    }

    [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        height: 3px;
        border-radius: 3px 3px 0 0;
        background: linear-gradient(90deg, var(--red), var(--orange), var(--amber));
    }

    [data-testid="stPlotlyChart"] {
        position: relative;
        z-index: 1;
        overflow: hidden;
        border: 1px solid rgba(231, 222, 207, 0.12);
        border-radius: 15px;
        background: rgba(12, 15, 22, 0.72);
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.28);
    }

    [data-testid="stSlider"] label,
    [data-testid="stCheckbox"] label {
        color: var(--text-soft) !important;
        font-weight: 600 !important;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid rgba(93, 169, 255, 0.24);
        background: rgba(18, 27, 40, 0.78);
    }

    @media (max-width: 720px) {
        .main .block-container {
            padding: 1rem 0.7rem 1.5rem;
        }

        .topbar {
            padding: 0.85rem;
        }

        .header-meta {
            justify-content: flex-start;
        }

        .metric-grid {
            grid-template-columns: 1fr;
        }
    }

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.9rem;
        margin-top: 0.2rem;
    }

    .metric-card {
        position: relative;
        overflow: hidden;
        min-height: 120px;
        padding: 1rem 1rem 0.8rem;
        border-radius: 16px;
        border: 1px solid var(--border);
        box-shadow: 0 12px 28px rgba(7, 17, 29, 0.36);
    }

    .metric-card::before {
        content: "";
        position: absolute;
        inset: 0 auto 0 0;
        width: 4px;
        background: currentColor;
    }

    .metric-card.revenue { background: linear-gradient(135deg, rgba(37, 28, 27, 0.98), rgba(27, 24, 24, 0.98)); color: var(--orange); }
    .metric-card.profit { background: linear-gradient(135deg, rgba(35, 27, 25, 0.98), rgba(25, 24, 23, 0.98)); color: var(--red); }
    .metric-card.margin { background: linear-gradient(135deg, rgba(24, 37, 30, 0.98), rgba(22, 27, 25, 0.98)); color: var(--green); }
    .metric-card.sla { background: linear-gradient(135deg, rgba(24, 30, 42, 0.98), rgba(22, 24, 31, 0.98)); color: var(--blue); }

    .metric-label {
        display: block;
        color: var(--muted);
        font-size: 9px;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-weight: 700;
    }

    .metric-value {
        display: block;
        margin-top: 0.7rem;
        color: var(--text);
        font-size: clamp(1.5rem, 1.8vw, 2rem);
        font-weight: 800;
        letter-spacing: -0.05em;
    }

    .metric-delta {
        display: inline-block;
        margin-top: 0.7rem;
        padding: 0.25rem 0.5rem;
        border-radius: 999px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.05);
    }

    .metric-delta.positive { color: var(--green); }
    .metric-delta.negative { color: var(--red); }
    .metric-delta.neutral { color: var(--amber); }

    .panel {
        position: relative;
        z-index: 1;
        background: linear-gradient(180deg, rgba(28, 30, 34, 0.96), rgba(19, 21, 24, 0.98));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 12px 26px var(--shadow);
    }

    .creative-panel {
        position: relative;
        z-index: 1;
        background: linear-gradient(135deg, rgba(37, 29, 25, 0.98), rgba(24, 24, 23, 0.98));
        border: 1px solid var(--border-strong);
        border-radius: 16px;
        padding: 1rem;
    }

    .status-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        padding: 0.72rem 0.8rem;
        border-radius: 12px;
        border: 1px solid var(--border);
        background: linear-gradient(180deg, rgba(35, 35, 36, 0.92), rgba(22, 23, 24, 0.96));
    }

    .status-key {
        color: var(--text-soft);
        font-size: 10px;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-weight: 700;
    }

    .status-val {
        font-size: 11px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 700;
    }

    .healthy { color: var(--green); }
    .watch { color: var(--amber); }
    .risk { color: var(--red); }
    .info { color: var(--blue); }

    .mini-card {
        background: linear-gradient(180deg, rgba(35, 34, 33, 0.96), rgba(22, 22, 22, 0.98));
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.8rem 0.8rem 0.75rem;
        min-height: 116px;
    }

    .mini-label {
        display: block;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 9px;
        font-weight: 800;
    }

    .mini-value {
        display: block;
        margin-top: 0.4rem;
        color: var(--text);
        font-weight: 800;
        font-size: 1.18rem;
        letter-spacing: -0.04em;
    }

    .mini-sub {
        display: block;
        margin-top: 0.45rem;
        color: var(--text-soft);
        font-size: 0.72rem;
        line-height: 1.4;
    }

    .scenario-number {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 0.7rem;
        padding: 0.8rem 0.8rem;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(43, 35, 30, 0.96), rgba(24, 23, 22, 0.96));
        border: 1px solid var(--border);
    }

    .scenario-number .label {
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 9px;
        font-weight: 700;
    }

    .scenario-number .value {
        color: var(--text);
        font-size: 1.1rem;
        font-weight: 800;
        letter-spacing: -0.03em;
    }

    .alert-item {
        display: flex;
        align-items: flex-start;
        gap: 0.68rem;
        padding: 0.7rem 0.75rem;
        border-radius: 12px;
        border: 1px solid var(--border);
        background: linear-gradient(180deg, rgba(35, 32, 31, 0.96), rgba(22, 21, 21, 0.98));
    }

    .alert-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        margin-top: 0.3rem;
        flex-shrink: 0;
    }

    .alert-critical { background: var(--red); }
    .alert-warning { background: var(--amber); }
    .alert-info { background: var(--cyan); }

    .alert-text {
        color: var(--text-soft);
        font-size: 0.76rem;
        line-height: 1.4;
    }

    .alert-text strong {
        color: var(--text);
    }

    .footer {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        flex-wrap: wrap;
        color: var(--muted);
        font-size: 10px;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-top: 1.3rem;
        padding-top: 0.9rem;
        border-top: 1px solid var(--border);
    }

    div[data-testid="stSlider"] {
        padding: 0.35rem 0.2rem 0.15rem;
    }

    div[data-testid="stCheckbox"] {
        background: rgba(35, 34, 32, 0.9);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.75rem 0.8rem;
    }

    @media (max-width: 1100px) {
        .metric-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

con = duckdb.connect("data/logistics_warehouse.duckdb")

with st.container():
    left_ctrl, right_ctrl = st.columns([1.2, 0.8])

    with left_ctrl:
        st.markdown('<div class="section-label">Scenario Console</div>', unsafe_allow_html=True)
        st.markdown('<div class="creative-panel">', unsafe_allow_html=True)
        fuel_adj = st.slider("Fuel Market Volatility ($)", 0, 100, 22, key="fuel_adj")
        vol_adj = st.slider("Demand Surge (%)", -30, 30, 0, key="vol_adj")
        ai_capacity_balancing = st.checkbox("Enable AI Capacity Balancing", value=True, key="ai_capacity_balancing")
        st.markdown('</div>', unsafe_allow_html=True)

    with right_ctrl:
        st.markdown('<div class="section-label">Live Margin</div>', unsafe_allow_html=True)
        demand_factor = 1 + (vol_adj / 100.0)
        fuel_cost_factor = 1 + ((fuel_adj / 100.0) * 0.7)
        capacity_factor = 0.94 if ai_capacity_balancing else 1.0

        sim_query = f"""
            SELECT region,
                   SUM(revenue * {demand_factor}) as rev,
                   SUM((revenue * {demand_factor}) - (cost * {fuel_cost_factor} * {capacity_factor})) as prof
            FROM fact_shipments
                 WHERE region IS NOT NULL
            GROUP BY 1
        """
        df = con.execute(sim_query).df()
        df["margin"] = (df["prof"] / df["rev"]) * 100

        margin_mean = float(df["margin"].mean())
        revenue_total = float(df["rev"].sum())
        profit_total = float(df["prof"].sum())

        margin_fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=margin_mean,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "SYSTEM-WIDE MARGIN", "font": {"color": "#ffd166", "size": 16}},
            delta={"reference": 45},
            gauge={
                "axis": {"range": [0, 60], "tickwidth": 1, "tickcolor": "#9bb5d8"},
                "bar": {"color": "#ff9f43"},
                "bgcolor": "rgba(255,255,255,0.02)",
                "steps": [
                    {"range": [0, 35], "color": "rgba(255, 107, 107, 0.18)"},
                    {"range": [35, 45], "color": "rgba(251, 191, 36, 0.18)"},
                    {"range": [45, 60], "color": "rgba(44, 212, 159, 0.18)"},
                ],
                "threshold": {"line": {"color": "#edf7ff", "width": 4}, "thickness": 0.7, "value": 45},
            },
        ))
        margin_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=270,
            margin=dict(l=20, r=20, t=52, b=20),
            font=dict(color="#edf7ff"),
        )
        st.plotly_chart(margin_fig, use_container_width=True)

status_text = "Healthy"
if margin_mean < 35:
    status_text = "Risk"
elif margin_mean < 40:
    status_text = "Watch"

header = st.columns([3, 1])
with header[0]:
    st.markdown(
        """
        <div class="topbar">
            <div>
                <div class="eyebrow">Global Operations Intelligence</div>
                <h1 class="title">DHL GLOBAL COMMAND</h1>
                <p class="subtitle">Global network performance • operational command center</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with header[1]:
    meta_now = datetime.now().strftime("%d %b %Y • %H:%M")
    st.markdown(
        f"""
        <div class="topbar">
            <div class="header-meta">
                <div class="meta-box">
                    <span class="meta-label">Window</span>
                    <span class="meta-value">2026 Q1</span>
                </div>
                <div class="meta-box">
                    <span class="meta-label">Updated</span>
                    <span class="meta-value">{meta_now}</span>
                </div>
                <div class="status-pill">System online</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

st.markdown(
    f"""
    <div class="metric-grid">
        <div class="metric-card revenue">
            <span class="metric-label">Estimated Quarterly Revenue</span>
            <span class="metric-value">${revenue_total / 1e6:.1f}M</span>
            <span class="metric-delta positive">+4.2%</span>
        </div>
        <div class="metric-card profit">
            <span class="metric-label">Net Operating Profit</span>
            <span class="metric-value">${profit_total / 1e6:.2f}M</span>
            <span class="metric-delta negative">-1.8%</span>
        </div>
        <div class="metric-card margin">
            <span class="metric-label">System-wide Margin</span>
            <span class="metric-value">{margin_mean:.1f}%</span>
            <span class="metric-delta neutral">Target 45.0%</span>
        </div>
        <div class="metric-card sla">
            <span class="metric-label">SLA Compliance</span>
            <span class="metric-value">98.4%</span>
            <span class="metric-delta positive">+0.4%</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

tabs = st.tabs(["Overview", "Scenario insights"])

with tabs[0]:
    main_cols = st.columns([1.45, 1.0])

    with main_cols[0]:
        st.markdown('<div class="section-label">Regional Performance</div>', unsafe_allow_html=True)
        chart_df = df.sort_values("prof", ascending=False).copy()
        chart_df["profit_m"] = chart_df["prof"] / 1_000_000
        margin_min = float(chart_df["margin"].min())
        margin_max = float(chart_df["margin"].max())
        region_fig = px.bar(
            chart_df,
            x="region",
            y="profit_m",
            text="profit_m",
            color="margin",
            color_continuous_scale=[[0, '#ff625f'], [0.28, '#ff9f43'], [0.52, '#ffd166'], [0.76, '#42d392'], [1, '#5da9ff']],
            range_color=[margin_min, margin_max],
            hover_data={"profit_m": ":.2f", "margin": ":.1f", "rev": ":.2f", "prof": False},
            template="plotly_dark",
        )
        region_fig.update_traces(
            marker_line_width=0,
            texttemplate="$%{y:.2f}M",
            textfont_color="#f8f3ea",
            cliponaxis=False,
        )
        region_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=15, r=15, t=10, b=15),
            font=dict(color="#edf7ff"),
            height=310,
            showlegend=False,
            yaxis_title="Operating Profit ($M)",
            coloraxis_colorbar={"title": "Margin %", "ticksuffix": "%", "thickness": 12},
        )
        st.plotly_chart(region_fig, use_container_width=True)

        st.write("")
        st.markdown('<div class="section-label">30-Day Capacity Outlook</div>', unsafe_allow_html=True)
        if os.path.exists("data/shipment_forecast.png"):
            st.image("data/shipment_forecast.png", use_container_width=True)
        else:
            st.info("The forecast image is not present yet. Run the forecasting script to generate it.")

    with main_cols[1]:
        st.markdown('<div class="section-label">Scenario Lab</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="scenario-number">
                <div>
                    <div class="label">Projected revenue</div>
                </div>
                <div class="value">${revenue_total / 1e6:.1f}M</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="scenario-number">
                <div>
                    <div class="label">Projected margin</div>
                </div>
                <div class="value">{margin_mean:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")
        st.markdown('<div class="section-label">Command Signals</div>', unsafe_allow_html=True)
        signal_items = [
            ("Capacity", "Healthy", "healthy"),
            ("Margin", status_text, "healthy" if status_text == "Healthy" else "watch" if status_text == "Watch" else "risk"),
            ("SLA", "Healthy", "healthy"),
            ("Demand", "Elevated", "watch"),
            ("Data Quality", "Stable", "info"),
        ]
        for key, value, css in signal_items:
            st.markdown(
                f"""
                <div class="status-row">
                    <div class="status-key">{key}</div>
                    <div class="status-val {css}">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")
        st.markdown('<div class="section-label">Operational Alerts</div>', unsafe_allow_html=True)
        alert_items = []
        if margin_mean < 40:
            alert_items.append(("Critical", "Margin variance detected"))
        elif margin_mean < 45:
            alert_items.append(("Warning", "Margin remains below the operating target"))
        else:
            alert_items.append(("Info", "Margin remains within target range"))

        if vol_adj > 10:
            alert_items.append(("Warning", "Demand surge above baseline"))
        else:
            alert_items.append(("Info", "Demand signal remains stable"))

        if fuel_adj > 50:
            alert_items.append(("Critical", "Fuel volatility is compressing operating leverage"))
        else:
            alert_items.append(("Info", "Fuel exposure remains within expected thresholds"))

        for level, text in alert_items:
            color = "alert-critical" if level == "Critical" else "alert-warning" if level == "Warning" else "alert-info"
            st.markdown(
                f"""
                <div class="alert-item">
                    <span class="alert-dot {color}"></span>
                    <div class="alert-text"><strong>{level}</strong> — {text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    intel_cols = st.columns([1.1, 1.1, 1.1])
    with intel_cols[0]:
        st.markdown('<div class="section-label">Operational Intelligence</div>', unsafe_allow_html=True)
        insight_text = (
            "Margin pressure is visible relative to the modeled operating target."
            if margin_mean < 40
            else "Margin remains within the expected operating range for the current scenario."
        )
        st.markdown(
            f"<div class='mini-card'><span class='mini-label'>Margin pressure</span><span class='mini-value'>{margin_mean:.1f}%</span><span class='mini-sub'>{insight_text}</span></div>",
            unsafe_allow_html=True,
        )

    with intel_cols[1]:
        st.markdown('<div class="section-label">Capacity Signal</div>', unsafe_allow_html=True)
        insight_text = (
            "Demand is trending above the baseline profile and should be monitored against network capacity."
            if vol_adj > 10
            else "Demand remains close to the baseline profile."
        )
        st.markdown(
            f"<div class='mini-card'><span class='mini-label'>Demand surge</span><span class='mini-value'>{vol_adj:+.0f}%</span><span class='mini-sub'>{insight_text}</span></div>",
            unsafe_allow_html=True,
        )

    with intel_cols[2]:
        st.markdown('<div class="section-label">Fuel Exposure</div>', unsafe_allow_html=True)
        insight_text = (
            "Fuel volatility is elevated and reducing net operating leverage."
            if fuel_adj > 50
            else "Fuel conditions are manageable under the current model."
        )
        st.markdown(
            f"<div class='mini-card'><span class='mini-label'>Fuel volatility</span><span class='mini-value'>${fuel_adj}</span><span class='mini-sub'>{insight_text}</span></div>",
            unsafe_allow_html=True,
        )

with tabs[1]:
    st.markdown('<div class="section-label">Scenario Details</div>', unsafe_allow_html=True)
    benchmark = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=margin_mean,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Target vs Actual"},
        delta={"reference": 45},
        gauge={
            "axis": {"range": [0, 60], "tickwidth": 1, "tickcolor": "#9bb5d8"},
            "bar": {"color": "#2dd4bf"},
            "bgcolor": "rgba(255,255,255,0.02)",
            "steps": [
                {"range": [0, 35], "color": "rgba(255, 107, 107, 0.18)"},
                {"range": [35, 45], "color": "rgba(251, 191, 36, 0.18)"},
                {"range": [45, 60], "color": "rgba(44, 212, 159, 0.18)"},
            ],
            "threshold": {"line": {"color": "#edf7ff", "width": 4}, "thickness": 0.7, "value": 45},
        },
    ))
    benchmark.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(l=20, r=20, t=35, b=20),
        font=dict(color="#edf7ff"),
    )
    st.plotly_chart(benchmark, use_container_width=True)

    st.write("")
    st.markdown(
        """
        <div class="panel">
            <div class="status-row"><div class="status-key">Network</div><div class="status-val healthy">Stable</div></div>
            <div class="status-row" style="margin-top: 0.7rem;"><div class="status-key">Data freshness</div><div class="status-val info">Live</div></div>
            <div class="status-row" style="margin-top: 0.7rem;"><div class="status-key">Forecast model</div><div class="status-val watch">Tracking</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="footer">
        <div>Global operations</div>
        <div>Warehouse network</div>
        <div>Command center</div>
    </div>
    """,
    unsafe_allow_html=True,
)

con.close()