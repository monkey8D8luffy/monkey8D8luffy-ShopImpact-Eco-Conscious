"""
ShopImpact - Ultimate Streamlit Edition v3.0
Fixed Dropdowns, Enhanced Analytics (Water & Trees), and High Contrast UI.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import random
import time
from pathlib import Path
from typing import Dict

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="ShopImpact 🍃",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ADVANCED CSS & THEME FIXES ====================
st.markdown("""
<style>
    /* --- GLOBAL THEME --- */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
        color: #000000 !important;
    }

    .stApp {
        background: linear-gradient(120deg, #e0f2f1 0%, #f1f8e9 50%, #fffde7 100%);
        background-attachment: fixed;
    }

    /* --- CRITICAL FIX: DROPDOWN & INPUT VISIBILITY --- */
    /* Forces the dropdown menu (popover) to be white with black text */
    div[data-baseweb="popover"], div[data-baseweb="select"], div[role="listbox"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Target specific list items in the dropdown */
    li[role="option"] {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Hover state for dropdown items */
    li[role="option"]:hover {
        background-color: #e8f5e9 !important; /* Light green hover */
        color: #000000 !important;
    }

    /* Make selected value in the box visible */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-color: #4caf50 !important;
    }

    /* Input labels and text */
    .stSelectbox label, .stNumberInput label, .stSlider label, .stTextInput label {
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }

    /* --- GLASSMORPHISM CARDS --- */
    div[data-testid="stMetric"], div[class*="stCard"] {
        background: rgba(255, 255, 255, 0.9); /* High opacity for readability */
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.6);
        transition: transform 0.3s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
    }
    
    /* --- METRIC COLORS --- */
    [data-testid="stMetricValue"] { color: #000000 !important; }
    [data-testid="stMetricLabel"] { color: #444444 !important; }
    [data-testid="stMetricDelta"] { font-weight: bold; }

    /* --- BUTTONS --- */
    .stButton > button {
        background: linear-gradient(45deg, #2e7d32, #66bb6a);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 12px 28px;
        font-weight: 800;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.5);
    }
    
    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(255,255,255,0.8);
        border-radius: 15px;
        padding: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 800;
        color: #555555;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        color: #2e7d32 !important;
    }
    
    /* --- LEAF ANIMATION --- */
    @keyframes dropAndDry {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; }
        10% { opacity: 0.8; }
        100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
    }
    .leaf {
        position: fixed;
        font-size: 1.5rem;
        animation: dropAndDry 20s infinite linear;
        pointer-events: none;
        z-index: 0;
        color: #a5d6a7; /* Subtle green */
    }
</style>
<div class="leaf" style="left: 10%; animation-delay: 0s;">🍃</div>
<div class="leaf" style="left: 30%; animation-delay: 5s;">🍂</div>
<div class="leaf" style="left: 70%; animation-delay: 2s;">🌿</div>
<div class="leaf" style="left: 90%; animation-delay: 8s;">🌱</div>
""", unsafe_allow_html=True)

# ==================== IMPACT LOGIC (WATER & TREES) ====================
# Data Sources: Global footprint network averages (simplified for app)
IMPACT_DATA = {
    # Fashion (High Water)
    'Jeans': {'co2': 33.4, 'water': 7500, 'trees': 0.0},
    'T-Shirt': {'co2': 7.0, 'water': 2700, 'trees': 0.0},
    'Shoes': {'co2': 14.0, 'water': 4000, 'trees': 0.0},
    'Fast Fashion': {'co2': 10.0, 'water': 3000, 'trees': 0.0},
    'Coat': {'co2': 25.0, 'water': 1000, 'trees': 0.0},
    
    # Food (High Water & Land Use)
    'Meat': {'co2': 20.0, 'water': 15000, 'trees': 0.05}, # Deforestation for feed
    'Burger': {'co2': 4.0, 'water': 2400, 'trees': 0.01},
    'Coffee': {'co2': 0.4, 'water': 140, 'trees': 0.0},
    'Dairy Products': {'co2': 3.0, 'water': 1000, 'trees': 0.01},
    
    # Electronics (High CO2, High Water in Chip Mfg)
    'Smartphone': {'co2': 60.0, 'water': 12000, 'trees': 0.0},
    'Laptop': {'co2': 250.0, 'water': 19000, 'trees': 0.0},
    
    # Paper/Wood (High Trees)
    'Books (New)': {'co2': 2.0, 'water': 50, 'trees': 0.005},
    'Furniture': {'co2': 90.0, 'water': 0, 'trees': 0.5},
    'Sofa': {'co2': 120.0, 'water': 0, 'trees': 1.0},
    
    # Eco (Low Impact)
    'Second-Hand Item': {'co2': 1.0, 'water': 0, 'trees': 0},
    'Local Groceries': {'co2': 0.5, 'water': 100, 'trees': 0},
}

PRODUCT_TYPES = list(IMPACT_DATA.keys()) + [
    'Electronics', 'Home Decor', 'Cosmetics', 'Sports Gear', 'Car Parts', 'Other'
]

ALL_BRANDS = ['Zara', 'H&M', 'Nike', 'Apple', 'Samsung', 'IKEA', 'Local', 'Generic', 'Other']

def get_impact(product_type: str, price: float) -> Dict:
    """Calculate impact based on product type and price scaling"""
    base = IMPACT_DATA.get(product_type, {'co2': price * 0.05, 'water': price * 1.5, 'trees': 0})
    
    # Scale slightly with price (expensive items usually bigger/more resources)
    # But cap the scaling to avoid unrealistic numbers for luxury items
    scale = max(0.5, min(price / 1000, 3.0)) 
    
    return {
        'co2': base['co2'] * scale,
        'water': base['water'] * scale,
        'trees': base['trees'] * scale
    }

BADGES = {
    'first_step': {'name': '🌱 First Step', 'desc': 'Logged your first purchase', 'icon': '🌱'},
    'water_saver': {'name': '💧 Water Saver', 'desc': 'Chose low water impact item', 'icon': '💧'},
    'forest_guard': {'name': '🌲 Forest Guard', 'desc': 'Saved a tree (Recycled/Used)', 'icon': '🌲'},
    'big_spender': {'name': '💎 Big Spender', 'desc': 'Logged item > ₹10k', 'icon': '💎'},
    'thrift_king': {'name': '👑 Thrift King', 'desc': '3 Second-hand items', 'icon': '👑'}
}

# ==================== DATA & STATE ====================
DATA_FILE = Path("shopimpact_data_v4.json")

def load_data():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except: pass
    return {'purchases': [], 'user_profile': {'name': 'Friend', 'badges': []}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

if 'initialized' not in st.session_state:
    st.session_state.data = load_data()
    st.session_state.initialized = True

# ==================== APP LOGIC ====================
def add_purchase(ptype, brand, price):
    impact = get_impact(ptype, price)
    entry = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'type': ptype,
        'brand': brand,
        'price': price,
        'co2': impact['co2'],
        'water': impact['water'],
        'trees': impact['trees']
    }
    st.session_state.data['purchases'].append(entry)
    
    # Badge Logic
    badges = st.session_state.data['user_profile']['badges']
    new_badge = None
    
    if len(st.session_state.data['purchases']) == 1 and 'first_step' not in badges:
        new_badge = 'first_step'
    if impact['water'] < 100 and 'water_saver' not in badges:
        new_badge = 'water_saver'
    if price > 10000 and 'big_spender' not in badges:
        new_badge = 'big_spender'
        
    if new_badge:
        badges.append(new_badge)
        st.toast(f"🏆 {BADGES[new_badge]['name']} Unlocked!", icon=BADGES[new_badge]['icon'])
        st.balloons()
        
    save_data(st.session_state.data)

# ==================== MAIN UI ====================
col1, col2 = st.columns([3,1])
with col1:
    st.title("🍃 ShopImpact")
    st.caption("Track CO₂, Water Wasted, and Trees Cut from your shopping.")
with col2:
    if st.session_state.data['user_profile']['badges']:
        last = st.session_state.data['user_profile']['badges'][-1]
        st.info(f"🏆 Latest: {BADGES[last]['name']}")

st.markdown("---")

tabs = st.tabs(["🛍️ Dashboard", "🌊 Impact Analytics", "👤 Profile"])

# --- DASHBOARD ---
with tabs[0]:
    c_form, c_stats = st.columns([1, 1.5], gap="medium")
    
    with c_form:
        st.markdown("### 📝 New Purchase")
        with st.container():
            st.markdown('<div class="stCard">', unsafe_allow_html=True)
            with st.form("entry_form", clear_on_submit=True):
                # FIX: Explicit help text to ensure contrast if needed
                product = st.selectbox("📦 Product Type", PRODUCT_TYPES)
                brand = st.selectbox("🏷️ Brand", ALL_BRANDS)
                price = st.slider("💰 Price (₹)", 0, 50000, 1000)
                
                if st.form_submit_button("Add Purchase"):
                    add_purchase(product, brand, price)
                    st.success("Added!")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Quick Insight
            if product == 'Jeans':
                st.warning("👖 Did you know? 1 pair of jeans uses ~7,500 liters of water!")
            if product == 'Burger':
                st.warning("🍔 Beef production is a leading cause of deforestation.")

    with c_stats:
        st.markdown("### 🚀 Reality Check")
        df = pd.DataFrame(st.session_state.data['purchases'])
        
        if not df.empty:
            total_water = df['water'].sum()
            total_trees = df['trees'].sum()
            
            # Row 1: The Big 3 Metrics
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("💨 CO₂ Emitted", f"{df['co2'].sum():.1f} kg")
            with m2:
                # Convert water to "Bathtubs" (approx 150L per bath) for interest
                bathtubs = total_water / 150
                st.metric("💧 Water Wasted", f"{total_water:,.0f} L", f"~{bathtubs:.0f} Bathtubs")
            with m3:
                st.metric("🌲 Trees Cost", f"{total_trees:.2f}", "Trees cut")
            
            # Row 2: Visual Impact
            st.markdown("#### 🌍 Your Footprint Visualized")
            
            # Water Visual
            water_fill = min(total_water / 50000 * 100, 100)
            st.markdown(f"**Water Usage (Goal: < 50k L)**")
            st.progress(water_fill / 100)
            
            # Tree Visual
            if total_trees > 0:
                trees_emoji = "🌲 " * int(total_trees) + "🌱"
                st.markdown(f"**Forest Impact:** {trees_emoji}")
            else:
                st.markdown("**Forest Impact:** 🍃 Safe! No trees cut yet.")

        else:
            st.info("Log your first item to see how much water and trees you've impacted.")

# --- ANALYTICS ---
with tabs[1]:
    if not df.empty:
        st.markdown("### 📊 Deep Dive")
        
        # 1. Water Wasted Chart (Bar)
        fig_water = px.bar(
            df, x='type', y='water', 
            title="💧 Water Guzzlers (Liters)",
            color='water', color_continuous_scale='Blues'
        )
        # CRITICAL: Fix Chart Visibility
        fig_water.update_layout(
            font=dict(color='black', size=14),
            paper_bgcolor='rgba(255,255,255,0.6)',
            plot_bgcolor='rgba(255,255,255,0.6)',
            xaxis=dict(gridcolor='#ddd', title_font=dict(color='black')),
            yaxis=dict(gridcolor='#ddd', title_font=dict(color='black'))
        )
        st.plotly_chart(fig_water, use_container_width=True)
        
        col_a, col_b = st.columns(2)
        
        # 2. CO2 Trend (Area)
        with col_a:
            fig_trend = px.area(
                df, x='date', y='co2', 
                title="☁️ Cumulative CO₂ Impact",
                line_shape='spline'
            )
            fig_trend.update_traces(line_color='#e74c3c')
            fig_trend.update_layout(
                font=dict(color='black'),
                paper_bgcolor='rgba(255,255,255,0.6)',
                plot_bgcolor='rgba(255,255,255,0.6)',
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor='#ddd')
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
        # 3. Efficiency Bubble Chart
        with col_b:
            fig_bubble = px.scatter(
                df, x='price', y='co2', 
                size='water', color='type',
                title="📉 Efficiency (Size = Water Usage)",
                hover_data=['brand']
            )
            fig_bubble.update_layout(
                font=dict(color='black'),
                paper_bgcolor='rgba(255,255,255,0.6)',
                plot_bgcolor='rgba(255,255,255,0.6)',
                xaxis=dict(gridcolor='#ddd', title="Price (₹)"),
                yaxis=dict(gridcolor='#ddd', title="CO₂ (kg)")
            )
            st.plotly_chart(fig_bubble, use_container_width=True)
            
    else:
        st.warning("No data yet! Go to Dashboard and add items.")

# --- PROFILE ---
with tabs[2]:
    st.markdown("### 🏆 Hall of Shame & Fame")
    
    my_badges = st.session_state.data['user_profile']['badges']
    
    cols = st.columns(5)
    for i, (bid, bdata) in enumerate(BADGES.items()):
        with cols[i]:
            unlocked = bid in my_badges
            opacity = "1" if unlocked else "0.3"
            border = "2px solid gold" if unlocked else "1px dashed gray"
            
            st.markdown(f"""
            <div style="text-align:center; padding:10px; border:{border}; border-radius:10px; opacity:{opacity}; background:white; color:black;">
                <h1 style="margin:0;">{bdata['icon']}</h1>
                <p style="font-weight:bold; margin:0; font-size:0.8rem;">{bdata['name']}</p>
                <p style="font-size:0.7rem; margin:0;">{bdata['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
    if st.button("🗑️ Reset All Data"):
        st.session_state.data = {'purchases': [], 'user_profile': {'name': 'Friend', 'badges': []}}
        save_data(st.session_state.data)
        st.rerun()

# FOOTER
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: black; font-weight: bold;'>Made with 💧 & 🌲 | ShopImpact v3.0</div>", unsafe_allow_html=True)
