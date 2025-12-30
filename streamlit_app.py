"""
ShopImpact - Modern UI Version
A Glassmorphism-inspired eco-tracker with gamification.
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
    page_title="ShopImpact",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CONSTANTS (Simplified for Code Length) ====================
# Note: I am keeping your lists, but normally you would move these to a separate file.
PRODUCT_TYPES = [
    'Fast Fashion', 'T-Shirt', 'Jeans', 'Dress', 'Suit', 'Jacket', 'Sweater', 'Hoodie', 'Shorts', 
    'Leggings', 'Activewear', 'Swimwear', 'Shoes', 'Sneakers', 'Boots', 'Handbag', 'Backpack',
    'Smartphone', 'Laptop', 'Tablet', 'Headphones', 'Earbuds', 'Smartwatch', 'Gaming Console',
    'Local Groceries', 'Organic Vegetables', 'Organic Fruits', 'Meat', 'Dairy Products', 'Coffee',
    'Sofa', 'Chair', 'Dining Table', 'Bed Frame', 'Mattress', 'Rug', 'Lamp', 'Plant Pot',
    'Skincare', 'Makeup', 'Perfume', 'Shampoo', 'Soap', 'Toothpaste',
    'Books (New)', 'Books (Used)', 'Vinyl Record', 'Video Game',
    'Yoga Mat', 'Dumbbells', 'Bicycle', 'Tent', 'Running Shoes',
    'Second-Hand Item', 'Thrifted Clothing', 'Refurbished Tech', 'Vintage Furniture'
]

ALL_BRANDS = [
    'Zara', 'H&M', 'Shein', 'Uniqlo', 'Nike', 'Adidas', 'Patagonia', 'The North Face', 'Lululemon',
    'Apple', 'Samsung', 'Sony', 'Dell', 'HP', 'Lenovo', 'Asus', 'Logitech',
    'Whole Foods', 'Trader Joes', 'Local Farm', 'Farmers Market', 'Nestle', 'Coca-Cola', 'Starbucks',
    'IKEA', 'West Elm', 'Pottery Barn', 'Target', 'Wayfair',
    'Sephora', 'Ulta', 'The Ordinary', 'Glossier', 'Lush',
    'Amazon', 'Barnes & Noble', 'ThriftBooks', 'Goodwill', 'Salvation Army', 'Local Thrift Store',
    'Etsy', 'eBay', 'Depop', 'Poshmark', 'Back Market'
]

def get_product_multiplier(product_type: str) -> float:
    """Simplified multiplier logic for demo purposes"""
    if product_type in ['Fast Fashion', 'Meat', 'SUV', 'Plane Ticket']: return 3.5
    if product_type in ['Electronics', 'Furniture', 'Leather']: return 2.5
    if product_type in ['Dairy', 'Imported Food']: return 1.5
    if product_type in ['Local Groceries', 'Organic', 'Public Transport']: return 0.3
    if 'Second-Hand' in product_type or 'Used' in product_type or 'Thrift' in product_type: return 0.1
    return 1.0

ECO_FRIENDLY_CATEGORIES = [
    'Second-Hand Item', 'Local Groceries', 'Books (Used)', 'Thrifted Clothing',
    'Used Electronics', 'Vintage Furniture', 'Organic Vegetables', 'Organic Fruits',
    'Refurbished Phone', 'Refurbished Tech', 'Used Book', 'Upcycled Item'
]

TIPS_LIST = [
    '🌍 Buying second-hand reduces CO₂ by up to 80%!',
    '🌱 Local produce has 5x less carbon footprint.',
    '♻️ Repairing items saves tons of emissions.',
    '🎒 BYO bag saves ~6kg of CO₂ per year.',
    '🌾 Plant-based meals = 50% less carbon impact.',
]

MOTIVATIONAL_QUOTES = [
    "Small changes, big impact! 🌍",
    "Be the change you wish to see.",
    "Conscious choices create a better tomorrow.",
    "Sustainability is a responsibility.",
]

DATA_FILE = Path("shopimpact_data.json")

# ==================== DATA LOGIC ====================
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
        'user_profile': {'name': '', 'monthlyBudget': 15000, 'co2Goal': 50, 'joinDate': datetime.now().strftime('%Y-%m-%d')},
        'settings': {'highContrast': False}
    }

if 'initialized' not in st.session_state:
    data = load_data_cached()
    st.session_state.purchases = data.get('purchases', [])
    st.session_state.user_profile = data.get('user_profile', get_default_data()['user_profile'])
    st.session_state.settings = data.get('settings', {'highContrast': False})
    st.session_state.show_success = False
    st.session_state.success_message = ''
    st.session_state.initialized = True

# ==================== GAMIFICATION LOGIC ====================
def get_user_badges(purchases, user_profile):
    total_purchases = len(purchases)
    if total_purchases == 0: return []
    
    eco_count = sum(1 for p in purchases if p['type'] in ECO_FRIENDLY_CATEGORIES)
    current_month = datetime.now().month
    month_purchases = [p for p in purchases if datetime.strptime(p['date'], '%Y-%m-%d').month == current_month]
    month_spend = sum(p['price'] for p in month_purchases)

    badges = [
        {"id": "starter", "name": "The Starter", "icon": "🌱", "desc": "Logged first purchase", "condition": total_purchases >= 1},
        {"id": "eco_warrior", "name": "Eco Warrior", "icon": "🛡️", "desc": "Bought 5+ eco items", "condition": eco_count >= 5},
        {"id": "thrift_master", "name": "Thrift Master", "icon": "🧥", "desc": "Bought 3+ used items", "condition": sum(1 for p in purchases if "Second-Hand" in p['type'] or "Used" in p['type'] or "Thrift" in p['type']) >= 3},
        {"id": "budget_boss", "name": "Budget Boss", "icon": "🐖", "desc": "Under budget (min 5 items)", "condition": len(month_purchases) >= 5 and month_spend <= user_profile.get('monthlyBudget', 15000)},
        {"id": "local_legend", "name": "Local Legend", "icon": "🏘️", "desc": "Bought 3 'Local' items", "condition": sum(1 for p in purchases if "Local" in p['type']) >= 3}
    ]
    for badge in badges: badge['earned'] = badge.pop('condition')
    return badges

def add_purchase(product_type, brand, price):
    old_badges = get_user_badges(st.session_state.purchases, st.session_state.user_profile)
    old_earned = {b['id'] for b in old_badges if b['earned']}

    co2_impact = price * get_product_multiplier(product_type)
    purchase = {'date': datetime.now().strftime('%Y-%m-%d'), 'type': product_type, 'brand': brand, 'price': float(price), 'co2_impact': float(co2_impact)}
    st.session_state.purchases.append(purchase)
    
    save_data({'purchases': st.session_state.purchases, 'user_profile': st.session_state.user_profile, 'settings': st.session_state.settings})
    
    new_badges = get_user_badges(st.session_state.purchases, st.session_state.user_profile)
    new_earned = {b['id'] for b in new_badges if b['earned']}
    newly_unlocked = new_earned - old_earned

    if newly_unlocked:
        badge_name = next(b['name'] for b in new_badges if b['id'] == list(newly_unlocked)[0])
        st.session_state.success_message = f"🏆 Badge Unlocked: {badge_name}!"
        st.balloons()
    elif product_type in ECO_FRIENDLY_CATEGORIES:
        st.session_state.success_message = f"🌿 Excellent! Eco-friendly choice recorded."
        st.snow()
    else:
        st.session_state.success_message = f"✅ Logged! {product_type} added."
    st.session_state.show_success = True

# ==================== 🎨 HIGH-CONTRAST MODERN UI ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    /* Global Font */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        color: #1e293b;
    }
    
    /* Background - Soft Mint Gradient */
    .stApp {
        background: linear-gradient(135deg, #d1fae5 0%, #ecfccb 100%);
    }

    /* HEADERS - Forced Dark Green for Visibility */
    h1, h2, h3, [data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h3 {
        color: #064e3b !important; /* Deep Forest Green */
        font-weight: 700 !important;
        text-shadow: none !important;
    }
    
    /* SUBTITLES - Dark Grey */
    p, .stMarkdown p {
        color: #334155 !important;
        font-size: 16px;
    }

    /* CARDS - Solid White for Readability */
    .stCard, div[data-testid="stForm"], div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    /* INPUTS - High Contrast Borders */
    .stTextInput > div > div > input, .stSelectbox > div > div > div {
        background-color: #ffffff;
        border: 2px solid #cbd5e1;
        color: #0f172a;
        border-radius: 10px;
    }
    .stTextInput > div > div > input:focus, .stSelectbox > div > div > div:focus {
        border-color: #10b981;
    }

    /* BUTTONS - Solid Dark Green */
    div.stButton > button {
        background-color: #059669;
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div.stButton > button:hover {
        background-color: #047857;
    }

    /* METRICS - Darker Numbers */
    [data-testid="stMetricValue"] {
        color: #059669 !important;
        font-weight: 700;
        font-size: 28px !important;
    }
    [data-testid="stMetricLabel"] {
        color: #64748b !important;
    }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.6);
        border-radius: 8px;
        color: #475569;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #059669 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== MAIN UI ====================

# --- Header Section ---
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.markdown("<div style='font-size: 60px; text-align: right;'>🌿</div>", unsafe_allow_html=True)
with col_title:
    st.markdown("# ShopImpact")
    st.markdown("### Your mindful companion for a greener planet.")

st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True) # Spacer

# --- Tabs ---
tab1, tab2 = st.tabs(["📊 Dashboard & Logger", "👤 My Profile"])

with tab1:
    col_main, col_sidebar = st.columns([2.2, 1])

    # --- MAIN CONTENT ---
    with col_main:
        # 1. ADD PURCHASE CARD
        st.markdown("#### 🛍️ Log New Item")
        with st.form("purchase_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                product_type = st.selectbox("Category", options=PRODUCT_TYPES)
            with c2:
                final_brand = st.selectbox("Brand", options=ALL_BRANDS)
            
            price = st.slider("Price (₹)", 0, 50000, 1000, 100)
            
            # Live CO2 preview
            est_co2 = price * get_product_multiplier(product_type)
            st.caption(f"Estimated Impact: **{est_co2:.1f} kg CO₂**")
            
            submitted = st.form_submit_button("Add to Tracker")
            if submitted:
                add_purchase(product_type, final_brand, price)
                st.rerun()

        # Success Message Area
        if st.session_state.show_success:
            st.success(st.session_state.success_message)
            st.session_state.show_success = False

        st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)

        # 2. METRICS ROW
        if st.session_state.purchases:
            df = pd.DataFrame(st.session_state.purchases)
            total_co2 = df['co2_impact'].sum()
            total_spend = df['price'].sum()
            
            st.markdown("#### 📈 Overview")
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Spend", f"₹{total_spend:,.0f}", delta="Lifetime")
            m2.metric("Carbon Footprint", f"{total_co2:.1f} kg", delta_color="inverse")
            m3.metric("Items Logged", len(df))

            # 3. CHARTS
            st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
            c_chart1, c_chart2 = st.columns(2)
            
            with c_chart1:
                # Custom Eco-Themed Bar Chart
                fig_bar = px.bar(
                    df.groupby('type')['co2_impact'].sum().reset_index().nlargest(5, 'co2_impact'),
                    x='type', y='co2_impact',
                    title='High Impact Items',
                    color='co2_impact',
                    color_continuous_scale=['#a7f3d0', '#34d399', '#059669', '#064e3b'] # Custom Green Gradient
                )
                fig_bar.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'family': 'Poppins'},
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            with c_chart2:
                # Donut Chart
                fig_pie = px.pie(
                    df.groupby('type')['price'].sum().reset_index().nlargest(5, 'price'),
                    values='price', names='type',
                    title='Spending Habits',
                    color_discrete_sequence=px.colors.sequential.Tealgrn
                )
                fig_pie.update_traces(hole=.4, hoverinfo="label+percent+name")
                fig_pie.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'family': 'Poppins'}
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                
            # Recent History Table
            st.markdown("#### 🧾 Recent Logs")
            st.dataframe(
                df[['date', 'type', 'brand', 'price', 'co2_impact']].tail(5).sort_values('date', ascending=False),
                use_container_width=True,
                hide_index=True
            )

    # --- SIDEBAR CONTENT ---
    with col_sidebar:
        # Profile Mini Card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #059669, #34d399); padding: 15px; border-radius: 15px; color: white; margin-bottom: 20px;">
            <div style="font-weight: 600; font-size: 14px;">CURRENT LEVEL</div>
            <div style="font-weight: 700; font-size: 24px;">Eco Enthusiast</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🏆 Badges")
        my_badges = get_user_badges(st.session_state.purchases, st.session_state.user_profile)
        
        if not my_badges:
            st.info("Log items to unlock!")
          else:
            # Grid Layout for Badges
            rows = [my_badges[i:i + 3] for i in range(0, len(my_badges), 3)]
            for row in rows:
                cols = st.columns(3)
                for idx, badge in enumerate(row):
                    with cols[idx]:
                        if badge['earned']:
                            # UNLOCKED: White card with green border
                            st.markdown(f"""
                            <div style="text-align: center; background: white; border-radius: 12px; padding: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border: 2px solid #86efac;" title="{badge['name']}">
                                <div style="font-size: 24px;">{badge['icon']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            # LOCKED: Grey card (so you can see it exists)
                            st.markdown(f"""
                            <div style="text-align: center; background: #e2e8f0; border-radius: 12px; padding: 12px; opacity: 0.7;" title="Locked: {badge['desc']}">
                                <div style="font-size: 24px; filter: grayscale(1);">🔒</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="text-align: center; background: rgba(255,255,255,0.3); ...
                        else:
                            st.markdown(f"""
                            <div style="text-align: center; background: rgba(255,255,255,0.3); border-radius: 10px; padding: 10px; opacity: 0.5; filter: grayscale(1);" title="Locked: {badge['desc']}">
                                <div style="font-size: 24px;">{badge['icon']}</div>
                            </div>
                            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 💡 Daily Tip")
        st.info(random.choice(TIPS_LIST), icon="🌱")
        
        # Clear Data Option
        with st.expander("⚙️ Settings"):
            if st.button("Reset Data", type="secondary"):
                st.session_state.purchases = []
                save_data({'purchases': [], 'user_profile': st.session_state.user_profile, 'settings': {}})
                st.rerun()

with tab2:
    st.markdown("### Edit Profile")
    st.caption("Adjust your goals and budget here.")
    # (Simplified profile form for visuals)
    with st.form("prof_form"):
        st.text_input("Name", value=st.session_state.user_profile.get('name', ''))
        st.number_input("Budget", value=15000)
        st.form_submit_button("Save Changes")
