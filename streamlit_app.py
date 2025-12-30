"""
ShopImpact - Advanced Version 2.0
Features: High Contrast Mode, Advanced Analytics, Custom Entries, Editable History.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import random
from pathlib import Path
from typing import Dict, List

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="ShopImpact Pro",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== EXPANDED DATABASE ====================
PRODUCT_CATEGORIES = {
    "Fashion": ['T-Shirt', 'Jeans', 'Dress', 'Suit', 'Jacket', 'Sweater', 'Hoodie', 'Sneakers', 'Boots', 'Handbag', 'Jewelry', 'Fast Fashion Item'],
    "Tech": ['Smartphone', 'Laptop', 'Tablet', 'Headphones', 'Smartwatch', 'Gaming Console', 'Monitor', 'PC Components', 'Camera'],
    "Home": ['Sofa', 'Chair', 'Table', 'Bed', 'Mattress', 'Rug', 'Lamp', 'Decor', 'Kitchen Appliance', 'Air Conditioner'],
    "Groceries": ['Local Veggies', 'Imported Fruit', 'Meat (Beef)', 'Meat (Chicken)', 'Dairy', 'Processed Food', 'Coffee', 'Alcohol'],
    "Transport": ['Flight (Domestic)', 'Flight (Intl)', 'Gasoline (Full Tank)', 'Uber/Taxi Ride', 'Train Ticket'],
    "Wellness": ['Skincare', 'Makeup', 'Perfume', 'Supplement', 'Gym Equipment'],
    "Eco-Friendly": ['Second-Hand Clothes', 'Refurbished Tech', 'Vintage Furniture', 'Local Farmers Market', 'Bamboo Products', 'Repair Service']
}

# Flatten list for dropdowns
ALL_PRODUCTS = [item for sublist in PRODUCT_CATEGORIES.values() for item in sublist]

ALL_BRANDS = [
    'Zara', 'H&M', 'Shein', 'Uniqlo', 'Gucci', 'Louis Vuitton', 
    'Nike', 'Adidas', 'Patagonia', 'The North Face', 'Lululemon', 'Puma',
    'Apple', 'Samsung', 'Sony', 'Dell', 'HP', 'Lenovo', 'Asus', 'Logitech', 'Razer',
    'IKEA', 'West Elm', 'Pottery Barn', 'Target', 'Wayfair', 'Pepperfry',
    'Nestle', 'Coca-Cola', 'Pepsi', 'Starbucks', 'Whole Foods', 'Trader Joes',
    'Sephora', 'Ulta', 'Loreal', 'Estee Lauder', 'The Ordinary',
    'Amazon', 'Flipkart', 'Myntra', 'Ajio', 'Etsy', 'eBay'
]

def get_product_multiplier(product_type: str) -> float:
    """Advanced logic for CO2 estimation"""
    # High Impact
    if product_type in ['Meat (Beef)', 'Flight (Intl)', 'SUV', 'Fast Fashion Item']: return 4.5
    if product_type in ['Meat (Chicken)', 'Flight (Domestic)', 'Luxury Fashion']: return 3.0
    # Medium Impact
    if product_type in ['Smartphone', 'Laptop', 'Gaming Console', 'Imported Fruit']: return 2.5
    if product_type in ['Jeans', 'Furniture', 'Dairy']: return 1.8
    # Low Impact
    if product_type in ['Local Veggies', 'Public Transport', 'Coffee']: return 0.5
    # Positive/Very Low Impact
    if product_type in ['Second-Hand Clothes', 'Refurbished Tech', 'Repair Service']: return 0.1
    return 1.0

TIPS_LIST = [
    '🌍 Buying second-hand reduces CO₂ by up to 80%!',
    '🌱 Local produce has 5x less carbon footprint.',
    '♻️ Repairing items saves tons of emissions.',
    '🎒 BYO bag saves ~6kg of CO₂ per year.',
    '🌾 Plant-based meals = 50% less carbon impact.',
    '💡 LED bulbs use 75% less energy.',
    '🥩 Skipping meat one day a week saves huge CO₂.'
]

DATA_FILE = Path("shopimpact_data_v2.json")

# ==================== DATA MANAGEMENT ====================
@st.cache_data
def load_data_cached() -> Dict:
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r') as f: return json.load(f)
        except: return get_default_data()
    return get_default_data()

def save_data(data: Dict) -> None:
    with open(DATA_FILE, 'w') as f: json.dump(data, f, indent=2)
    load_data_cached.clear()

def get_default_data() -> Dict:
    return {
        'purchases': [],
        'user_profile': {'name': 'Eco Hero', 'monthlyBudget': 20000, 'co2Goal': 50},
        'settings': {'highContrast': False}
    }

# Initialize Session State
if 'initialized' not in st.session_state:
    data = load_data_cached()
    st.session_state.purchases = data.get('purchases', [])
    st.session_state.user_profile = data.get('user_profile', get_default_data()['user_profile'])
    st.session_state.high_contrast = data.get('settings', {}).get('highContrast', False)
    st.session_state.initialized = True

def toggle_contrast():
    st.session_state.high_contrast = not st.session_state.high_contrast
    # Save setting immediately
    save_data({'purchases': st.session_state.purchases, 'user_profile': st.session_state.user_profile, 'settings': {'highContrast': st.session_state.high_contrast}})

# ==================== DYNAMIC CSS THEME ====================
def inject_css():
    if st.session_state.high_contrast:
        # HIGH CONTRAST MODE (Black/Yellow/Cyan)
        st.markdown("""
        <style>
            .stApp { background-color: #000000; color: #FFFF00; }
            h1, h2, h3, h4, p, label, .stMarkdown, .stMetricLabel { color: #FFFF00 !important; font-family: 'Courier New', monospace !important; }
            [data-testid="stMetricValue"] { color: #00FFFF !important; }
            .stCard, div[data-testid="stForm"], div[data-testid="stMetric"] {
                background: #111111; border: 2px solid #FFFF00; border-radius: 0px; box-shadow: none;
            }
            .stTextInput > div > div > input, .stSelectbox > div > div > div {
                background-color: #000000; color: #FFFFFF; border: 2px solid #FFFFFF; border-radius: 0px;
            }
            div.stButton > button {
                background-color: #000000; color: #00FFFF !important; border: 2px solid #00FFFF; border-radius: 0px; text-transform: uppercase;
            }
            div.stButton > button:hover { background-color: #00FFFF; color: #000000 !important; }
            [data-testid="stSidebar"] { background-color: #1a1a1a; border-right: 3px solid #FFFF00; }
            .stTabs [aria-selected="true"] { background-color: #FFFF00 !important; color: #000000 !important; border: 1px solid #FFFF00; }
        </style>
        """, unsafe_allow_html=True)
    else:
        # MODERN ECO MODE (Glassmorphism/Mint)
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
            html, body, [class*="css"] { font-family: 'Poppins', sans-serif; color: #1e293b; }
            .stApp { background: linear-gradient(135deg, #e0f2fe 0%, #f0fdf4 100%); }
            h1, h2, h3 { color: #0f766e !important; }
            .stCard, div[data-testid="stForm"], div[data-testid="stMetric"] {
                background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(10px);
                border-radius: 20px; border: 1px solid #ffffff; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
            }
            [data-testid="stMetricValue"] { color: #059669 !important; }
            div.stButton > button {
                background: linear-gradient(90deg, #10b981 0%, #059669 100%); color: white; border: none; border-radius: 12px;
            }
            [data-testid="stSidebar"] { background-color: rgba(255,255,255,0.5); border-right: 1px solid #fff; }
        </style>
        """, unsafe_allow_html=True)

inject_css()

# ==================== MAIN UI ====================

# --- Sidebar ---
with st.sidebar:
    st.markdown("### ⚙️ Accessibility")
    st.toggle("High Contrast Mode", value=st.session_state.high_contrast, on_change=toggle_contrast)
    
    st.markdown("---")
    st.markdown("### 👤 User Profile")
    st.write(f"**{st.session_state.user_profile['name']}**")
    
    # Progress towards next rank (Mock logic)
    purchases_len = len(st.session_state.purchases)
    rank = "Novice"
    progress = 0
    if purchases_len > 5: rank = "Conscious Buyer"; progress = 30
    if purchases_len > 15: rank = "Sustainability Pro"; progress = 70
    
    st.caption(f"Rank: {rank}")
    st.progress(progress)
    
    st.markdown("---")
    st.info(random.choice(TIPS_LIST), icon="💡")

# --- Header ---
c1, c2 = st.columns([5, 1])
with c1:
    st.title("ShopImpact Pro")
    st.markdown("Advanced Tracking & Environmental Analytics")
with c2:
    st.metric("Budget", f"₹{st.session_state.user_profile['monthlyBudget']/1000}k")

# --- TABS ---
tab_input, tab_analytics, tab_history = st.tabs(["➕ Add Item", "📊 Advanced Analytics", "📝 History Editor"])

# ==================== TAB 1: INPUT ====================
with tab_input:
    col_form, col_preview = st.columns([1.5, 1])
    
    with col_form:
        with st.form("advanced_input"):
            st.markdown("#### Log Purchase")
            
            # Switch between list and custom
            entry_mode = st.radio("Entry Mode", ["Select from List", "Custom Entry"], horizontal=True, label_visibility="collapsed")
            
            if entry_mode == "Select from List":
                p_cat = st.selectbox("Category", list(PRODUCT_CATEGORIES.keys()))
                p_type = st.selectbox("Product", PRODUCT_CATEGORIES[p_cat])
                p_brand = st.selectbox("Brand", ALL_BRANDS)
            else:
                p_cat = "Custom"
                p_type = st.text_input("Product Name (e.g. Vintage Lamp)")
                p_brand = st.text_input("Brand Name")
            
            price = st.number_input("Price (₹)", min_value=0, value=1500, step=100)
            date_logged = st.date_input("Date", value=datetime.now())
            
            # Smart logic for custom items
            multiplier = get_product_multiplier(p_type)
            
            submitted = st.form_submit_button("Log Impact", use_container_width=True)
            
            if submitted:
                if not p_type:
                    st.error("Please enter a product name.")
                else:
                    new_p = {
                        "date": date_logged.strftime("%Y-%m-%d"),
                        "category": p_cat,
                        "type": p_type,
                        "brand": p_brand if p_brand else "Unknown",
                        "price": price,
                        "co2": float(price * multiplier),
                        "id": str(datetime.now().timestamp()) # Unique ID for editing
                    }
                    st.session_state.purchases.append(new_p)
                    save_data({'purchases': st.session_state.purchases, 'user_profile': st.session_state.user_profile, 'settings': {'highContrast': st.session_state.high_contrast}})
                    st.success("Item Logged Successfully!")
                    st.rerun()

    with col_preview:
        if st.session_state.purchases:
            last_item = st.session_state.purchases[-1]
            st.info("Last Added:")
            st.markdown(f"**{last_item['type']}** ({last_item['brand']})")
            st.markdown(f"💸 ₹{last_item['price']}")
            st.markdown(f"☁️ {last_item['co2']:.1f} kg CO₂")
        
        # Gamification Badges (Simplified for cleaner UI)
        st.markdown("#### Recent Achievements")
        eco_count = sum(1 for p in st.session_state.purchases if p['category'] == 'Eco-Friendly')
        if eco_count >= 1: st.markdown("🌱 **First Step:** Bought an eco item")
        if len(st.session_state.purchases) >= 5: st.markdown("🔥 **Tracker:** Logged 5+ items")

# ==================== TAB 2: ANALYTICS ====================
with tab_analytics:
    if not st.session_state.purchases:
        st.warning("No data yet. Log some items in the first tab!")
    else:
        df = pd.DataFrame(st.session_state.purchases)
        df['date'] = pd.to_datetime(df['date'])
        
        # 1. TOP ROW METRICS
        m1, m2, m3, m4 = st.columns(4)
        total_spend = df['price'].sum()
        total_co2 = df['co2'].sum()
        current_month_spend = df[df['date'].dt.month == datetime.now().month]['price'].sum()
        
        m1.metric("Total Spent", f"₹{total_spend:,.0f}")
        m2.metric("Total CO₂ Impact", f"{total_co2:,.1f} kg")
        m3.metric("This Month", f"₹{current_month_spend:,.0f}")
        m4.metric("Avg. Item Cost", f"₹{df['price'].mean():,.0f}")
        
        st.markdown("---")

        # 2. ADVANCED CHARTS
        c1, c2 = st.columns([1, 1])
        
        with c1:
            st.markdown("#### 🌗 Impact Breakdown (Sunburst)")
            # Sunburst Chart: Category -> Brand -> Impact
            fig_sun = px.sunburst(
                df, 
                path=['category', 'type'], 
                values='co2',
                color='co2',
                color_continuous_scale='RdYlGn_r' # Red is bad (high CO2), Green is good
            )
            fig_sun.update_layout(margin=dict(t=0, l=0, r=0, b=0), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_sun, use_container_width=True)

        with c2:
            st.markdown("#### 🐖 Monthly Budget Meter")
            budget = st.session_state.user_profile['monthlyBudget']
            # Gauge Chart
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = current_month_spend,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Monthly Limit"},
                delta = {'reference': budget, 'increasing': {'color': "red"}},
                gauge = {
                    'axis': {'range': [None, budget * 1.5]},
                    'bar': {'color': "#059669" if not st.session_state.high_contrast else "#FFFF00"},
                    'steps': [
                        {'range': [0, budget], 'color': "rgba(0, 255, 0, 0.1)"},
                        {'range': [budget, budget*1.5], 'color': "rgba(255, 0, 0, 0.1)"}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': budget}}))
            fig_gauge.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white" if st.session_state.high_contrast else "#1e293b"})
            st.plotly_chart(fig_gauge, use_container_width=True)

        # 3. TREND LINE
        st.markdown("#### 📈 Spending & Impact Trend")
        # Group by date
        daily_df = df.groupby('date')[['price', 'co2']].sum().reset_index().sort_values('date')
        fig_line = px.line(daily_df, x='date', y=['price', 'co2'], markers=True)
        fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hovermode="x unified")
        st.plotly_chart(fig_line, use_container_width=True)

# ==================== TAB 3: HISTORY EDITOR ====================
with tab_history:
    st.markdown("### 📝 Manage Records")
    st.caption("Double click any cell to edit details. Use the checkbox to delete rows.")
    
    if st.session_state.purchases:
        df_edit = pd.DataFrame(st.session_state.purchases)
        
        # Use Data Editor for interactivity
        edited_df = st.data_editor(
            df_edit,
            num_rows="dynamic",
            column_config={
                "price": st.column_config.NumberColumn("Price (₹)", format="₹%d"),
                "co2": st.column_config.NumberColumn("CO₂ (kg)", format="%.1f kg"),
                "date": st.column_config.DateColumn("Date"),
                "id": None # Hide ID column
            },
            use_container_width=True
        )
        
        if st.button("💾 Save Changes"):
            # Convert back to list of dicts
            updated_data = edited_df.to_dict('records')
            # Fix date formatting (Data editor converts to datetime objects)
            for item in updated_data:
                if isinstance(item['date'], (datetime, pd.Timestamp)):
                    item['date'] = item['date'].strftime("%Y-%m-%d")
            
            st.session_state.purchases = updated_data
            save_data({'purchases': st.session_state.purchases, 'user_profile': st.session_state.user_profile, 'settings': {'highContrast': st.session_state.high_contrast}})
            st.success("Database updated!")
            st.rerun()
    else:
        st.info("No records to edit.")
