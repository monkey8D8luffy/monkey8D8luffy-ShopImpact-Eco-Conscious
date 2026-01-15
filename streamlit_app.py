"""
ShopImpact - Ultimate Streamlit Edition v3.5
High Contrast Charts, Fixed Visibility, and Optimized Performance.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import random
from pathlib import Path
from typing import Dict

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="ShopImpact 🍃",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== HIGH CONTRAST CSS ====================
st.markdown("""
<style>
    /* --- GLOBAL TEXT RESET --- */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap');
    
    html, body, [class*="css"], .stMarkdown, h1, h2, h3, h4, p, span, label, div {
        font-family: 'Nunito', sans-serif;
        color: #000000 !important; /* Force Pure Black Text */
    }

    /* --- BACKGROUND --- */
    .stApp {
        background: linear-gradient(135deg, #e0f7fa 0%, #f1f8e9 100%);
    }

    /* --- CARDS & CONTAINERS (Solid White for Contrast) --- */
    div[data-testid="stMetric"], div[class*="stCard"], div[data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.95) !important; /* 95% Opacity White */
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }

    /* --- INPUTS & DROPDOWNS (Critical Fix) --- */
    .stSelectbox div[data-baseweb="select"] > div,
    .stTextInput input, 
    .stNumberInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-color: #4caf50 !important;
        font-weight: bold;
    }
    
    /* Fix Dropdown Menu Items */
    ul[data-baseweb="menu"] li {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Input Labels */
    .stSelectbox label, .stNumberInput label, .stSlider label {
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        color: #000000 !important;
    }

    /* --- BUTTONS --- */
    .stButton > button {
        background: #2e7d32 !important;
        color: #ffffff !important; /* White text on green button */
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 10px 25px;
        transition: transform 0.1s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        background: #1b5e20 !important;
    }

    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] button {
        font-weight: 800;
        color: #444444;
        background-color: rgba(255,255,255,0.8);
    }
    .stTabs [aria-selected="true"] {
        color: #2e7d32 !important;
        background-color: #ffffff !important;
        border-bottom: 3px solid #2e7d32;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA & LOGIC ====================
DATA_FILE = Path("shopimpact_data_v5.json")

# Simplified Impact Data (Water in Liters, Trees in Count)
IMPACT_MAP = {
    'Jeans': {'co2': 33.4, 'water': 7500, 'trees': 0.0},
    'T-Shirt': {'co2': 7.0, 'water': 2700, 'trees': 0.0},
    'Shoes': {'co2': 14.0, 'water': 4000, 'trees': 0.0},
    'Smartphone': {'co2': 60.0, 'water': 12000, 'trees': 0.0},
    'Laptop': {'co2': 250.0, 'water': 19000, 'trees': 0.0},
    'Burger': {'co2': 4.0, 'water': 2400, 'trees': 0.01},
    'Furniture': {'co2': 90.0, 'water': 0, 'trees': 0.5},
    'Book': {'co2': 2.0, 'water': 50, 'trees': 0.005},
    'Other': {'co2': 5.0, 'water': 100, 'trees': 0.0},
}
PRODUCT_LIST = list(IMPACT_MAP.keys())

def load_data():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r') as f: return json.load(f)
        except: pass
    return {'purchases': [], 'user': {'badges': []}}

def save_data(data):
    with open(DATA_FILE, 'w') as f: json.dump(data, f)

if 'data' not in st.session_state:
    st.session_state.data = load_data()

# ==================== UI HELPERS ====================
def clean_chart_layout(fig):
    """Applies a clean, high-contrast style to any Plotly chart"""
    fig.update_layout(
        paper_bgcolor='white',   # Solid white background
        plot_bgcolor='white',    # Solid white plot area
        font={'color': 'black'}, # Force all text black
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=True, gridcolor='#eeeeee', linecolor='black'),
        yaxis=dict(showgrid=True, gridcolor='#eeeeee', linecolor='black'),
    )
    return fig

# ==================== MAIN APP ====================
col_title, col_badge = st.columns([3, 1])
with col_title:
    st.title("🍃 ShopImpact")
    st.caption("High-Contrast Mode Enabled")
with col_badge:
    if st.session_state.data['user']['badges']:
        st.info(f"🏆 Latest Badge: {st.session_state.data['user']['badges'][-1]}")

tabs = st.tabs(["🛍️ Tracker", "📊 Analytics", "👤 Profile"])

# --- TRACKER TAB ---
with tabs[0]:
    c1, c2 = st.columns([1, 1.5], gap="large")
    
    with c1:
        st.subheader("📝 Add Item")
        with st.container():
            # Using a container with custom CSS class for white background
            st.markdown('<div style="background:white; padding:20px; border-radius:15px; box-shadow:0 2px 10px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
            
            with st.form("add_form", clear_on_submit=True):
                ptype = st.selectbox("Product Type", PRODUCT_LIST)
                brand = st.text_input("Brand Name", placeholder="e.g. Zara, Apple")
                price = st.slider("Price (₹)", 0, 50000, 1000)
                
                if st.form_submit_button("Add Purchase"):
                    impact = IMPACT_MAP.get(ptype, IMPACT_MAP['Other'])
                    entry = {
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                        'type': ptype, 'brand': brand or "Generic", 'price': price,
                        'co2': impact['co2'], 'water': impact['water'], 'trees': impact['trees']
                    }
                    st.session_state.data['purchases'].append(entry)
                    
                    # Simple Badge Logic
                    if len(st.session_state.data['purchases']) == 1:
                        st.session_state.data['user']['badges'].append("🌱 First Step")
                        st.toast("Badge Unlocked: First Step!")
                    
                    save_data(st.session_state.data)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.subheader("🚀 Impact Summary")
        df = pd.DataFrame(st.session_state.data['purchases'])
        
        if not df.empty:
            # Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("CO₂ (kg)", f"{df['co2'].sum():.1f}")
            m2.metric("Water (L)", f"{df['water'].sum():,.0f}")
            m3.metric("Trees Cut", f"{df['trees'].sum():.2f}")
            
            st.markdown("#### 🕒 Recent Log")
            st.dataframe(
                df[['date', 'type', 'brand', 'price', 'co2']].tail(5).sort_values('date', ascending=False),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No data yet. Add a purchase on the left!")

# --- ANALYTICS TAB (FIXED CHARTS) ---
with tabs[1]:
    if not df.empty:
        st.subheader("📊 Visual Insights")
        
        col_charts1, col_charts2 = st.columns(2)
        
        with col_charts1:
            # Chart 1: Water Usage Bar Chart
            fig_water = px.bar(
                df, x='type', y='water', 
                title="💧 Water Footprint by Item",
                color='water', color_continuous_scale='Blues'
            )
            st.plotly_chart(clean_chart_layout(fig_water), use_container_width=True)
            
        with col_charts2:
            # Chart 2: CO2 Distribution Pie
            fig_pie = px.pie(
                df, names='type', values='co2',
                title="☁️ CO₂ Breakdown",
                hole=0.4
            )
            # Pie charts need specific text updates
            fig_pie.update_traces(textinfo='percent+label', textfont_size=14)
            st.plotly_chart(clean_chart_layout(fig_pie), use_container_width=True)

        # Chart 3: Efficiency Scatter
        st.markdown("### 📉 Cost vs. Nature")
        fig_scatter = px.scatter(
            df, x='price', y='co2',
            size='water', color='type',
            title="Price vs Impact (Bubble Size = Water Usage)",
            hover_data=['brand']
        )
        st.plotly_chart(clean_chart_layout(fig_scatter), use_container_width=True)
        
    else:
        st.warning("Please add data in the Dashboard tab first.")

# --- PROFILE TAB ---
with tabs[2]:
    st.subheader("🏆 Your Achievements")
    badges = st.session_state.data['user']['badges']
    
    if badges:
        st.write("You have unlocked:")
        for b in set(badges):
            st.success(f"🏅 {b}")
    else:
        st.info("Start tracking to unlock badges!")
        
    if st.button("Reset All Data"):
        st.session_state.data = {'purchases': [], 'user': {'badges': []}}
        save_data(st.session_state.data)
        st.rerun()

# FOOTER
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #555;'>ShopImpact v3.5 | High Contrast Edition</div>", unsafe_allow_html=True)
