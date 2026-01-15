"""
ShopImpact - Ultimate Streamlit Edition
Fully Optimized, Gamified, and Beautifully Animated.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import random
import time
from pathlib import Path
from typing import Dict, List, Optional

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="ShopImpact 🍃",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ADVANCED CSS & ANIMATIONS ====================
st.markdown("""
<style>
    /* --- GLOBAL THEME --- */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    .stApp {
        background: linear-gradient(120deg, #e0f2f1 0%, #f1f8e9 50%, #fffde7 100%);
        background-attachment: fixed;
    }

    /* --- FALLING LEAF ANIMATION --- */
    @keyframes dropAndDry {
        0% { transform: translateY(-10vh) rotate(0deg) translateX(0px); opacity: 0; filter: hue-rotate(0deg); }
        10% { opacity: 1; }
        50% { filter: hue-rotate(0deg); } /* Green */
        80% { filter: hue-rotate(90deg) sepia(1); } /* Dried/Brown */
        100% { transform: translateY(110vh) rotate(720deg) translateX(50px); opacity: 0; filter: hue-rotate(90deg) sepia(1); }
    }

    .leaf {
        position: fixed;
        top: 0;
        left: 50%;
        font-size: 2rem;
        animation: dropAndDry 15s infinite linear;
        pointer-events: none;
        z-index: 0;
    }
    
    .leaf:nth-child(1) { left: 10%; animation-duration: 12s; animation-delay: 0s; }
    .leaf:nth-child(2) { left: 30%; animation-duration: 18s; animation-delay: 2s; font-size: 1.5rem; }
    .leaf:nth-child(3) { left: 70%; animation-duration: 14s; animation-delay: 5s; }
    .leaf:nth-child(4) { left: 90%; animation-duration: 20s; animation-delay: 1s; font-size: 2.5rem; }

    /* --- GLASSMORPHISM CARDS --- */
    div[data-testid="stMetric"], div[class*="stCard"] {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.15);
    }

    /* --- UI TRANSITIONS --- */
    .element-container {
        animation: fadeIn 0.8s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* --- BUTTONS --- */
    .stButton > button {
        background: linear-gradient(45deg, #43a047, #66bb6a);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 10px 25px;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(67, 160, 71, 0.3);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(67, 160, 71, 0.5);
    }
    
    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255,255,255,0.5);
        border-radius: 15px;
        padding: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 10px;
        color: #4a5568;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #fff;
        color: #2e7d32;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* --- BADGE POPUP STYLE --- */
    .badge-popup {
        padding: 15px;
        border-radius: 10px;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: white;
        text-align: center;
        font-weight: bold;
        animation: popIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    @keyframes popIn {
        0% { transform: scale(0); }
        100% { transform: scale(1); }
    }

</style>
<div class="leaf">🍃</div>
<div class="leaf">🍂</div>
<div class="leaf">🍃</div>
<div class="leaf">🍂</div>
""", unsafe_allow_html=True)

# ==================== CONSTANTS ====================
# (Kept original lists for full functionality)
PRODUCT_TYPES = [
    'Fast Fashion', 'T-Shirt', 'Jeans', 'Dress', 'Suit', 'Jacket', 'Sweater', 'Hoodie', 'Shorts', 'Skirt',
    'Blazer', 'Coat', 'Pants', 'Leggings', 'Activewear', 'Swimwear', 'Underwear', 'Socks', 'Shoes', 'Sneakers',
    'Electronics', 'Smartphone', 'Laptop', 'Tablet', 'Desktop Computer', 'Monitor', 'Keyboard', 'Mouse',
    'Headphones', 'Gaming Console', 'Smartwatch', 'Camera', 'TV', 'Speaker', 'Drone',
    'Local Groceries', 'Organic Vegetables', 'Organic Fruits', 'Meat', 'Dairy Products', 'Snacks',
    'Home Decor', 'Sofa', 'Chair', 'Table', 'Bed', 'Mattress', 'Kitchenware', 'Appliance',
    'Cosmetics', 'Skincare', 'Perfume', 'Hair Care', 'Personal Care',
    'Books (New)', 'Books (Used)', 'E-book', 'Vinyl Record', 'Video Game',
    'Yoga Mat', 'Gym Equipment', 'Bicycle', 'Sports Gear', 'Camping Gear',
    'Car Parts', 'Tires', 'Car Accessories',
    'Restaurant Meal', 'Fast Food', 'Coffee', 'Dessert',
    'Leather Goods', 'Vegan Leather',
    'Second-Hand Item', 'Thrifted Clothing', 'Used Electronics', 'Vintage Furniture', 'Refurbished Tech',
    'Office Supplies', 'Stationery', 'Art Supplies',
    'Gift Card', 'Subscription', 'Event Ticket', 'Digital Download', '500+ (Other)'
]

ALL_BRANDS = [
    'Zara', 'H&M', 'Nike', 'Adidas', 'Uniqlo', 'Gucci', 'Louis Vuitton', 'Patagonia', 'The North Face', 'Levi\'s',
    'Apple', 'Samsung', 'Sony', 'Dell', 'HP', 'Lenovo', 'Asus', 'Microsoft', 'Google', 'Canon',
    'Whole Foods', 'Trader Joe\'s', 'Nestle', 'Coca-Cola', 'Pepsi', 'Danone', 'Beyond Meat',
    'IKEA', 'West Elm', 'Pottery Barn', 'Ashley Furniture', 'Wayfair',
    'Sephora', 'L\'Oreal', 'Estee Lauder', 'Mac', 'Fenty Beauty', 'The Body Shop', 'Lush',
    'Amazon', 'Barnes & Noble', 'Penguin Random House', 'Nintendo', 'PlayStation', 'Xbox',
    'Toyota', 'Honda', 'Ford', 'Tesla', 'BMW',
    'Local Thrift Store', 'Goodwill', 'Salvation Army', 'Depop', 'Poshmark', 'Etsy', 'eBay',
    'Local Farm', 'Farmers Market', 'Small Business', 'Handmade', 'Generic', 'Other'
]

# Simplified Multipliers for logic (Expanded version used in calculation)
def get_product_multiplier(product_type: str) -> float:
    base_multipliers = {
        'Fast Fashion': 2.5, 'Jeans': 3.2, 'Coat': 4.2, 'Shoes': 3.0,
        'Electronics': 1.8, 'Smartphone': 2.5, 'Laptop': 3.0, 'Desktop Computer': 3.5,
        'Meat': 1.5, 'Dairy Products': 0.6, 'Local Groceries': 0.3, 'Organic Vegetables': 0.2,
        'Sofa': 4.0, 'Bed': 3.5, 'Appliance': 2.0,
        'Cosmetics': 1.5, 'Perfume': 1.5,
        'Books (New)': 0.5, 'Books (Used)': 0.05, 'E-book': 0.02,
        'Bicycle': 5.0, 'Car Parts': 2.0,
        'Second-Hand Item': 0.1, 'Thrifted Clothing': 0.08, 'Used Electronics': 0.15,
        'Digital Download': 0.02, 'Service': 0.0
    }
    # Fallback logic for types not explicitly listed
    if product_type in base_multipliers:
        return base_multipliers[product_type]
    elif 'Used' in product_type or 'Second-Hand' in product_type or 'Thrift' in product_type:
        return 0.1
    elif 'Leather' in product_type:
        return 3.5
    elif 'Plastic' in product_type:
        return 2.0
    else:
        return 1.0

ECO_FRIENDLY_CATEGORIES = [
    'Second-Hand Item', 'Local Groceries', 'Books (Used)', 'Thrifted Clothing',
    'Used Electronics', 'Vintage Furniture', 'Organic Vegetables', 'Organic Fruits',
    'Refurbished Tech', 'Bicycle', 'Vegan Leather', 'Digital Download'
]

# ==================== BADGE SYSTEM ====================
BADGES = {
    'first_step': {'name': '🌱 First Step', 'desc': 'Logged your first purchase', 'icon': '🌱'},
    'thrift_king': {'name': '👑 Thrift King', 'desc': 'Bought 3 second-hand items', 'icon': '👑'},
    'low_carbon': {'name': '🍃 Low Carbon', 'desc': 'Logged an item with < 1kg CO₂', 'icon': '🍃'},
    'big_saver': {'name': '💰 Big Saver', 'desc': 'Spent over ₹10,000 in one go', 'icon': '💰'},
    'eco_warrior': {'name': '🛡️ Eco Warrior', 'desc': 'Maintained < 50kg CO₂ total', 'icon': '🛡️'},
    'consistent': {'name': '📅 Consistent', 'desc': 'Logged 5 items total', 'icon': '📅'}
}

# ==================== DATA MANAGEMENT ====================
DATA_FILE = Path("shopimpact_data_v2.json")

def get_default_data() -> Dict:
    return {
        'purchases': [],
        'user_profile': {
            'name': 'Friend',
            'monthlyBudget': 15000,
            'co2Goal': 50,
            'badges': []
        }
    }

@st.cache_data
def load_data_cached() -> Dict:
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return get_default_data()
    return get_default_data()

def save_data(data: Dict) -> None:
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        load_data_cached.clear()
    except Exception as e:
        st.error(f"Error saving data: {e}")

# ==================== INITIALIZATION ====================
if 'initialized' not in st.session_state:
    data = load_data_cached()
    st.session_state.purchases = data.get('purchases', [])
    st.session_state.user_profile = data.get('user_profile', get_default_data()['user_profile'])
    # Ensure badges list exists in profile
    if 'badges' not in st.session_state.user_profile:
        st.session_state.user_profile['badges'] = []
    st.session_state.initialized = True

# ==================== LOGIC FUNCTIONS ====================
def check_badges():
    """Check for new badges and trigger animations"""
    purchases = st.session_state.purchases
    my_badges = st.session_state.user_profile['badges']
    new_badge = None

    # Logic for badges
    if len(purchases) >= 1 and 'first_step' not in my_badges:
        new_badge = 'first_step'
    
    thrift_count = sum(1 for p in purchases if p['type'] in ECO_FRIENDLY_CATEGORIES)
    if thrift_count >= 3 and 'thrift_king' not in my_badges:
        new_badge = 'thrift_king'
        
    if purchases and purchases[-1]['co2_impact'] < 1.0 and 'low_carbon' not in my_badges:
        new_badge = 'low_carbon'
        
    if purchases and purchases[-1]['price'] > 10000 and 'big_saver' not in my_badges:
        new_badge = 'big_saver'

    if len(purchases) >= 5 and 'consistent' not in my_badges:
        new_badge = 'consistent'

    if new_badge:
        st.session_state.user_profile['badges'].append(new_badge)
        badge_info = BADGES[new_badge]
        
        # Trigger Toast
        st.toast(f"🏆 BADGE UNLOCKED: {badge_info['name']}", icon=badge_info['icon'])
        time.sleep(0.5)
        st.balloons()
        
        save_data({
            'purchases': st.session_state.purchases,
            'user_profile': st.session_state.user_profile
        })

def add_purchase(product_type: str, brand: str, price: float):
    co2_impact = price * get_product_multiplier(product_type) / 100 # Adjusted scaling for realistic nums
    
    # Eco bonus calculation
    if product_type in ECO_FRIENDLY_CATEGORIES:
        co2_impact *= 0.5 # 50% reduction for eco items
    
    purchase = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'type': product_type,
        'brand': brand,
        'price': float(price),
        'co2_impact': float(co2_impact)
    }
    st.session_state.purchases.append(purchase)
    
    save_data({
        'purchases': st.session_state.purchases,
        'user_profile': st.session_state.user_profile
    })
    
    check_badges()

# ==================== MAIN UI ====================

# HEADER
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("# 🍃 ShopImpact")
    st.markdown("### *Your Conscious Shopping Companion*")
with col_h2:
    if st.session_state.user_profile['badges']:
        latest = st.session_state.user_profile['badges'][-1]
        st.info(f"Latest Badge: {BADGES[latest]['icon']} {BADGES[latest]['name']}")
    else:
        st.info("Start shopping to earn badges!")

st.markdown("---")

# TABS
tab_dash, tab_analytics, tab_profile = st.tabs(["🛍️ Dashboard", "📊 Analytics", "🏆 Profile & Badges"])

# --- DASHBOARD TAB ---
with tab_dash:
    col_input, col_stats = st.columns([1, 1.5], gap="large")
    
    with col_input:
        st.markdown("#### 📝 New Purchase")
        with st.container():
            st.markdown('<div class="stCard">', unsafe_allow_html=True)
            with st.form("add_item", clear_on_submit=True):
                product_type = st.selectbox("📦 What did you buy?", PRODUCT_TYPES)
                brand = st.selectbox("🏷️ Brand", ALL_BRANDS)
                price = st.number_input("💰 Price (₹)", min_value=0.0, step=100.0)
                
                submitted = st.form_submit_button("Add to Tracker", type="primary", use_container_width=True)
                
                if submitted:
                    if price > 0:
                        add_purchase(product_type, brand, price)
                        st.success(f"Added {product_type}!")
                    else:
                        st.warning("Please enter a price.")
            st.markdown('</div>', unsafe_allow_html=True)

            # Quick Tips Card
            st.markdown("#### 💡 Quick Eco-Tip")
            tips = [
                "Buying used saves ~80% CO₂ vs new!",
                "Local produce = 5x less transport emissions.",
                "Repair > Replace.",
                "Combine deliveries to save fuel."
            ]
            st.info(random.choice(tips))

    with col_stats:
        st.markdown("#### 🚀 Live Impact Overview")
        
        if st.session_state.purchases:
            df = pd.DataFrame(st.session_state.purchases)
            total_spend = df['price'].sum()
            total_co2 = df['co2_impact'].sum()
            
            # Metrics Row
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Total Spent", f"₹{total_spend:,.0f}", delta=f"{len(df)} items")
            with m2:
                st.metric("Total CO₂", f"{total_co2:.1f} kg", delta_color="inverse", delta="Low is good!")
            with m3:
                eco_items = df[df['type'].isin(ECO_FRIENDLY_CATEGORIES)].shape[0]
                st.metric("Eco Choices", f"{eco_items}", f"{eco_items/len(df)*100:.0f}% Rate")

            # Recent Activity Timeline
            st.markdown("#### 🕰️ Recent Activity")
            recent = df.tail(5).iloc[::-1]
            for _, row in recent.iterrows():
                icon = "🍃" if row['type'] in ECO_FRIENDLY_CATEGORIES else "🛍️"
                color = "#2e7d32" if row['type'] in ECO_FRIENDLY_CATEGORIES else "#4a5568"
                st.markdown(
                    f"""
                    <div style="padding: 10px; background: rgba(255,255,255,0.6); border-radius: 10px; margin-bottom: 8px; border-left: 4px solid {color};">
                        <span style="font-size: 1.2rem;">{icon}</span> 
                        <strong>{row['type']}</strong> ({row['brand']}) 
                        <span style="float: right; color: #666;">₹{row['price']:,.0f} | {row['co2_impact']:.1f}kg CO₂</span>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                """
                <div style="text-align: center; padding: 40px; color: #888;">
                    <h3>👻 Nothing here yet!</h3>
                    <p>Log your first purchase to see your impact statistics.</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

# --- ANALYTICS TAB ---
with tab_analytics:
    if st.session_state.purchases:
        df = pd.DataFrame(st.session_state.purchases)
        df['date_dt'] = pd.to_datetime(df['date'])
        
        row1_col1, row1_col2 = st.columns(2)
        
        with row1_col1:
            st.markdown("### 📅 Spending vs CO₂ Over Time")
            fig_line = px.line(df, x='date_dt', y=['price', 'co2_impact'], markers=True, 
                               labels={'value': 'Amount', 'date_dt': 'Date'},
                               color_discrete_map={'price': '#2ecc71', 'co2_impact': '#e74c3c'})
            fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend_title_text='')
            st.plotly_chart(fig_line, use_container_width=True)

        with row1_col2:
            st.markdown("### 🍩 Category Impact Breakdown")
            fig_pie = px.sunburst(df, path=['type', 'brand'], values='co2_impact', 
                                  color='co2_impact', color_continuous_scale='RdYlGn_r')
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True)
            
        st.markdown("### 📉 Efficiency Scatter Plot (Price vs Impact)")
        st.caption("Identify items that were expensive but low impact (Green zone) vs cheap but high impact (Red zone)")
        fig_scatter = px.scatter(df, x='price', y='co2_impact', color='type', size='co2_impact',
                                 hover_data=['brand'], size_max=40)
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(240,240,240,0.5)',
            xaxis_title="Price (₹)",
            yaxis_title="CO₂ Impact (kg)"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    else:
        st.info("Log some data to unlock analytics!")

# --- PROFILE TAB ---
with tab_profile:
    p_col1, p_col2 = st.columns([1, 2])
    
    with p_col1:
        st.markdown("### ⚙️ Settings")
        with st.form("profile_update"):
            new_name = st.text_input("Display Name", st.session_state.user_profile['name'])
            new_budget = st.number_input("Monthly Budget (₹)", value=st.session_state.user_profile['monthlyBudget'])
            new_goal = st.number_input("CO₂ Limit Goal (kg)", value=st.session_state.user_profile['co2Goal'])
            
            if st.form_submit_button("Update Profile"):
                st.session_state.user_profile.update({
                    'name': new_name,
                    'monthlyBudget': new_budget,
                    'co2Goal': new_goal
                })
                save_data({'purchases': st.session_state.purchases, 'user_profile': st.session_state.user_profile})
                st.success("Updated!")
                st.rerun()
                
        if st.button("🗑️ Reset All Data", type="secondary"):
            st.session_state.purchases = []
            st.session_state.user_profile['badges'] = []
            save_data(get_default_data())
            st.rerun()

    with p_col2:
        st.markdown(f"### 🏆 {st.session_state.user_profile['name']}'s Trophy Cabinet")
        
        my_badges = st.session_state.user_profile['badges']
        
        # Grid display for badges
        cols = st.columns(4)
        for idx, (badge_id, info) in enumerate(BADGES.items()):
            col = cols[idx % 4]
            with col:
                is_unlocked = badge_id in my_badges
                opacity = "1.0" if is_unlocked else "0.3"
                filter_css = "grayscale(0%)" if is_unlocked else "grayscale(100%)"
                border = "2px solid #FFD700" if is_unlocked else "2px dashed #ccc"
                
                st.markdown(
                    f"""
                    <div style="
                        text-align: center; 
                        padding: 15px; 
                        border-radius: 15px; 
                        border: {border};
                        background: rgba(255,255,255,0.5);
                        opacity: {opacity};
                        filter: {filter_css};
                        height: 150px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        transition: all 0.3s;
                    ">
                        <div style="font-size: 3rem; margin-bottom: 5px;">{info['icon']}</div>
                        <div style="font-weight: bold; font-size: 0.9rem;">{info['name']}</div>
                        <div style="font-size: 0.7rem; color: #555;">{info['desc']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# FOOTER
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; color: #999; font-size: 0.8rem;">
        Made with 💚 | ShopImpact v2.0 | <a href="#" style="color: #66bb6a; text-decoration: none;">Privacy Policy</a>
    </div>
    """, 
    unsafe_allow_html=True
)
"""
ShopImpact - Ultimate Streamlit Edition
Fully Optimized, Gamified, and Beautifully Animated.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import random
import time
from pathlib import Path
from typing import Dict, List, Optional

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="ShopImpact 🍃",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ADVANCED CSS & ANIMATIONS ====================
st.markdown("""
<style>
    /* --- GLOBAL THEME --- */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    .stApp {
        background: linear-gradient(120deg, #e0f2f1 0%, #f1f8e9 50%, #fffde7 100%);
        background-attachment: fixed;
    }

    /* --- FALLING LEAF ANIMATION --- */
    @keyframes dropAndDry {
        0% { transform: translateY(-10vh) rotate(0deg) translateX(0px); opacity: 0; filter: hue-rotate(0deg); }
        10% { opacity: 1; }
        50% { filter: hue-rotate(0deg); } /* Green */
        80% { filter: hue-rotate(90deg) sepia(1); } /* Dried/Brown */
        100% { transform: translateY(110vh) rotate(720deg) translateX(50px); opacity: 0; filter: hue-rotate(90deg) sepia(1); }
    }

    .leaf {
        position: fixed;
        top: 0;
        left: 50%;
        font-size: 2rem;
        animation: dropAndDry 15s infinite linear;
        pointer-events: none;
        z-index: 0;
    }
    
    .leaf:nth-child(1) { left: 10%; animation-duration: 12s; animation-delay: 0s; }
    .leaf:nth-child(2) { left: 30%; animation-duration: 18s; animation-delay: 2s; font-size: 1.5rem; }
    .leaf:nth-child(3) { left: 70%; animation-duration: 14s; animation-delay: 5s; }
    .leaf:nth-child(4) { left: 90%; animation-duration: 20s; animation-delay: 1s; font-size: 2.5rem; }

    /* --- GLASSMORPHISM CARDS --- */
    div[data-testid="stMetric"], div[class*="stCard"] {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.15);
    }

    /* --- UI TRANSITIONS --- */
    .element-container {
        animation: fadeIn 0.8s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* --- BUTTONS --- */
    .stButton > button {
        background: linear-gradient(45deg, #43a047, #66bb6a);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 10px 25px;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(67, 160, 71, 0.3);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(67, 160, 71, 0.5);
    }
    
    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255,255,255,0.5);
        border-radius: 15px;
        padding: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 10px;
        color: #4a5568;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #fff;
        color: #2e7d32;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* --- BADGE POPUP STYLE --- */
    .badge-popup {
        padding: 15px;
        border-radius: 10px;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: white;
        text-align: center;
        font-weight: bold;
        animation: popIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    @keyframes popIn {
        0% { transform: scale(0); }
        100% { transform: scale(1); }
    }

</style>
<div class="leaf">🍃</div>
<div class="leaf">🍂</div>
<div class="leaf">🍃</div>
<div class="leaf">🍂</div>
""", unsafe_allow_html=True)

# ==================== CONSTANTS ====================
# (Kept original lists for full functionality)
PRODUCT_TYPES = [
    'Fast Fashion', 'T-Shirt', 'Jeans', 'Dress', 'Suit', 'Jacket', 'Sweater', 'Hoodie', 'Shorts', 'Skirt',
    'Blazer', 'Coat', 'Pants', 'Leggings', 'Activewear', 'Swimwear', 'Underwear', 'Socks', 'Shoes', 'Sneakers',
    'Electronics', 'Smartphone', 'Laptop', 'Tablet', 'Desktop Computer', 'Monitor', 'Keyboard', 'Mouse',
    'Headphones', 'Gaming Console', 'Smartwatch', 'Camera', 'TV', 'Speaker', 'Drone',
    'Local Groceries', 'Organic Vegetables', 'Organic Fruits', 'Meat', 'Dairy Products', 'Snacks',
    'Home Decor', 'Sofa', 'Chair', 'Table', 'Bed', 'Mattress', 'Kitchenware', 'Appliance',
    'Cosmetics', 'Skincare', 'Perfume', 'Hair Care', 'Personal Care',
    'Books (New)', 'Books (Used)', 'E-book', 'Vinyl Record', 'Video Game',
    'Yoga Mat', 'Gym Equipment', 'Bicycle', 'Sports Gear', 'Camping Gear',
    'Car Parts', 'Tires', 'Car Accessories',
    'Restaurant Meal', 'Fast Food', 'Coffee', 'Dessert',
    'Leather Goods', 'Vegan Leather',
    'Second-Hand Item', 'Thrifted Clothing', 'Used Electronics', 'Vintage Furniture', 'Refurbished Tech',
    'Office Supplies', 'Stationery', 'Art Supplies',
    'Gift Card', 'Subscription', 'Event Ticket', 'Digital Download', '500+ (Other)'
]

ALL_BRANDS = [
    'Zara', 'H&M', 'Nike', 'Adidas', 'Uniqlo', 'Gucci', 'Louis Vuitton', 'Patagonia', 'The North Face', 'Levi\'s',
    'Apple', 'Samsung', 'Sony', 'Dell', 'HP', 'Lenovo', 'Asus', 'Microsoft', 'Google', 'Canon',
    'Whole Foods', 'Trader Joe\'s', 'Nestle', 'Coca-Cola', 'Pepsi', 'Danone', 'Beyond Meat',
    'IKEA', 'West Elm', 'Pottery Barn', 'Ashley Furniture', 'Wayfair',
    'Sephora', 'L\'Oreal', 'Estee Lauder', 'Mac', 'Fenty Beauty', 'The Body Shop', 'Lush',
    'Amazon', 'Barnes & Noble', 'Penguin Random House', 'Nintendo', 'PlayStation', 'Xbox',
    'Toyota', 'Honda', 'Ford', 'Tesla', 'BMW',
    'Local Thrift Store', 'Goodwill', 'Salvation Army', 'Depop', 'Poshmark', 'Etsy', 'eBay',
    'Local Farm', 'Farmers Market', 'Small Business', 'Handmade', 'Generic', 'Other'
]

# Simplified Multipliers for logic (Expanded version used in calculation)
def get_product_multiplier(product_type: str) -> float:
    base_multipliers = {
        'Fast Fashion': 2.5, 'Jeans': 3.2, 'Coat': 4.2, 'Shoes': 3.0,
        'Electronics': 1.8, 'Smartphone': 2.5, 'Laptop': 3.0, 'Desktop Computer': 3.5,
        'Meat': 1.5, 'Dairy Products': 0.6, 'Local Groceries': 0.3, 'Organic Vegetables': 0.2,
        'Sofa': 4.0, 'Bed': 3.5, 'Appliance': 2.0,
        'Cosmetics': 1.5, 'Perfume': 1.5,
        'Books (New)': 0.5, 'Books (Used)': 0.05, 'E-book': 0.02,
        'Bicycle': 5.0, 'Car Parts': 2.0,
        'Second-Hand Item': 0.1, 'Thrifted Clothing': 0.08, 'Used Electronics': 0.15,
        'Digital Download': 0.02, 'Service': 0.0
    }
    # Fallback logic for types not explicitly listed
    if product_type in base_multipliers:
        return base_multipliers[product_type]
    elif 'Used' in product_type or 'Second-Hand' in product_type or 'Thrift' in product_type:
        return 0.1
    elif 'Leather' in product_type:
        return 3.5
    elif 'Plastic' in product_type:
        return 2.0
    else:
        return 1.0

ECO_FRIENDLY_CATEGORIES = [
    'Second-Hand Item', 'Local Groceries', 'Books (Used)', 'Thrifted Clothing',
    'Used Electronics', 'Vintage Furniture', 'Organic Vegetables', 'Organic Fruits',
    'Refurbished Tech', 'Bicycle', 'Vegan Leather', 'Digital Download'
]

# ==================== BADGE SYSTEM ====================
BADGES = {
    'first_step': {'name': '🌱 First Step', 'desc': 'Logged your first purchase', 'icon': '🌱'},
    'thrift_king': {'name': '👑 Thrift King', 'desc': 'Bought 3 second-hand items', 'icon': '👑'},
    'low_carbon': {'name': '🍃 Low Carbon', 'desc': 'Logged an item with < 1kg CO₂', 'icon': '🍃'},
    'big_saver': {'name': '💰 Big Saver', 'desc': 'Spent over ₹10,000 in one go', 'icon': '💰'},
    'eco_warrior': {'name': '🛡️ Eco Warrior', 'desc': 'Maintained < 50kg CO₂ total', 'icon': '🛡️'},
    'consistent': {'name': '📅 Consistent', 'desc': 'Logged 5 items total', 'icon': '📅'}
}

# ==================== DATA MANAGEMENT ====================
DATA_FILE = Path("shopimpact_data_v2.json")

def get_default_data() -> Dict:
    return {
        'purchases': [],
        'user_profile': {
            'name': 'Friend',
            'monthlyBudget': 15000,
            'co2Goal': 50,
            'badges': []
        }
    }

@st.cache_data
def load_data_cached() -> Dict:
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return get_default_data()
    return get_default_data()

def save_data(data: Dict) -> None:
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        load_data_cached.clear()
    except Exception as e:
        st.error(f"Error saving data: {e}")

# ==================== INITIALIZATION ====================
if 'initialized' not in st.session_state:
    data = load_data_cached()
    st.session_state.purchases = data.get('purchases', [])
    st.session_state.user_profile = data.get('user_profile', get_default_data()['user_profile'])
    # Ensure badges list exists in profile
    if 'badges' not in st.session_state.user_profile:
        st.session_state.user_profile['badges'] = []
    st.session_state.initialized = True

# ==================== LOGIC FUNCTIONS ====================
def check_badges():
    """Check for new badges and trigger animations"""
    purchases = st.session_state.purchases
    my_badges = st.session_state.user_profile['badges']
    new_badge = None

    # Logic for badges
    if len(purchases) >= 1 and 'first_step' not in my_badges:
        new_badge = 'first_step'
    
    thrift_count = sum(1 for p in purchases if p['type'] in ECO_FRIENDLY_CATEGORIES)
    if thrift_count >= 3 and 'thrift_king' not in my_badges:
        new_badge = 'thrift_king'
        
    if purchases and purchases[-1]['co2_impact'] < 1.0 and 'low_carbon' not in my_badges:
        new_badge = 'low_carbon'
        
    if purchases and purchases[-1]['price'] > 10000 and 'big_saver' not in my_badges:
        new_badge = 'big_saver'

    if len(purchases) >= 5 and 'consistent' not in my_badges:
        new_badge = 'consistent'

    if new_badge:
        st.session_state.user_profile['badges'].append(new_badge)
        badge_info = BADGES[new_badge]
        
        # Trigger Toast
        st.toast(f"🏆 BADGE UNLOCKED: {badge_info['name']}", icon=badge_info['icon'])
        time.sleep(0.5)
        st.balloons()
        
        save_data({
            'purchases': st.session_state.purchases,
            'user_profile': st.session_state.user_profile
        })

def add_purchase(product_type: str, brand: str, price: float):
    co2_impact = price * get_product_multiplier(product_type) / 100 # Adjusted scaling for realistic nums
    
    # Eco bonus calculation
    if product_type in ECO_FRIENDLY_CATEGORIES:
        co2_impact *= 0.5 # 50% reduction for eco items
    
    purchase = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'type': product_type,
        'brand': brand,
        'price': float(price),
        'co2_impact': float(co2_impact)
    }
    st.session_state.purchases.append(purchase)
    
    save_data({
        'purchases': st.session_state.purchases,
        'user_profile': st.session_state.user_profile
    })
    
    check_badges()

# ==================== MAIN UI ====================

# HEADER
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("# 🍃 ShopImpact")
    st.markdown("### *Your Conscious Shopping Companion*")
with col_h2:
    if st.session_state.user_profile['badges']:
        latest = st.session_state.user_profile['badges'][-1]
        st.info(f"Latest Badge: {BADGES[latest]['icon']} {BADGES[latest]['name']}")
    else:
        st.info("Start shopping to earn badges!")

st.markdown("---")

# TABS
tab_dash, tab_analytics, tab_profile = st.tabs(["🛍️ Dashboard", "📊 Analytics", "🏆 Profile & Badges"])

# --- DASHBOARD TAB ---
with tab_dash:
    col_input, col_stats = st.columns([1, 1.5], gap="large")
    
    with col_input:
        st.markdown("#### 📝 New Purchase")
        with st.container():
            st.markdown('<div class="stCard">', unsafe_allow_html=True)
            with st.form("add_item", clear_on_submit=True):
                product_type = st.selectbox("📦 What did you buy?", PRODUCT_TYPES)
                brand = st.selectbox("🏷️ Brand", ALL_BRANDS)
                price = st.number_input("💰 Price (₹)", min_value=0.0, step=100.0)
                
                submitted = st.form_submit_button("Add to Tracker", type="primary", use_container_width=True)
                
                if submitted:
                    if price > 0:
                        add_purchase(product_type, brand, price)
                        st.success(f"Added {product_type}!")
                    else:
                        st.warning("Please enter a price.")
            st.markdown('</div>', unsafe_allow_html=True)

            # Quick Tips Card
            st.markdown("#### 💡 Quick Eco-Tip")
            tips = [
                "Buying used saves ~80% CO₂ vs new!",
                "Local produce = 5x less transport emissions.",
                "Repair > Replace.",
                "Combine deliveries to save fuel."
            ]
            st.info(random.choice(tips))

    with col_stats:
        st.markdown("#### 🚀 Live Impact Overview")
        
        if st.session_state.purchases:
            df = pd.DataFrame(st.session_state.purchases)
            total_spend = df['price'].sum()
            total_co2 = df['co2_impact'].sum()
            
            # Metrics Row
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Total Spent", f"₹{total_spend:,.0f}", delta=f"{len(df)} items")
            with m2:
                st.metric("Total CO₂", f"{total_co2:.1f} kg", delta_color="inverse", delta="Low is good!")
            with m3:
                eco_items = df[df['type'].isin(ECO_FRIENDLY_CATEGORIES)].shape[0]
                st.metric("Eco Choices", f"{eco_items}", f"{eco_items/len(df)*100:.0f}% Rate")

            # Recent Activity Timeline
            st.markdown("#### 🕰️ Recent Activity")
            recent = df.tail(5).iloc[::-1]
            for _, row in recent.iterrows():
                icon = "🍃" if row['type'] in ECO_FRIENDLY_CATEGORIES else "🛍️"
                color = "#2e7d32" if row['type'] in ECO_FRIENDLY_CATEGORIES else "#4a5568"
                st.markdown(
                    f"""
                    <div style="padding: 10px; background: rgba(255,255,255,0.6); border-radius: 10px; margin-bottom: 8px; border-left: 4px solid {color};">
                        <span style="font-size: 1.2rem;">{icon}</span> 
                        <strong>{row['type']}</strong> ({row['brand']}) 
                        <span style="float: right; color: #666;">₹{row['price']:,.0f} | {row['co2_impact']:.1f}kg CO₂</span>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                """
                <div style="text-align: center; padding: 40px; color: #888;">
                    <h3>👻 Nothing here yet!</h3>
                    <p>Log your first purchase to see your impact statistics.</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

# --- ANALYTICS TAB ---
with tab_analytics:
    if st.session_state.purchases:
        df = pd.DataFrame(st.session_state.purchases)
        df['date_dt'] = pd.to_datetime(df['date'])
        
        row1_col1, row1_col2 = st.columns(2)
        
        with row1_col1:
            st.markdown("### 📅 Spending vs CO₂ Over Time")
            fig_line = px.line(df, x='date_dt', y=['price', 'co2_impact'], markers=True, 
                               labels={'value': 'Amount', 'date_dt': 'Date'},
                               color_discrete_map={'price': '#2ecc71', 'co2_impact': '#e74c3c'})
            fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend_title_text='')
            st.plotly_chart(fig_line, use_container_width=True)

        with row1_col2:
            st.markdown("### 🍩 Category Impact Breakdown")
            fig_pie = px.sunburst(df, path=['type', 'brand'], values='co2_impact', 
                                  color='co2_impact', color_continuous_scale='RdYlGn_r')
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True)
            
        st.markdown("### 📉 Efficiency Scatter Plot (Price vs Impact)")
        st.caption("Identify items that were expensive but low impact (Green zone) vs cheap but high impact (Red zone)")
        fig_scatter = px.scatter(df, x='price', y='co2_impact', color='type', size='co2_impact',
                                 hover_data=['brand'], size_max=40)
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(240,240,240,0.5)',
            xaxis_title="Price (₹)",
            yaxis_title="CO₂ Impact (kg)"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    else:
        st.info("Log some data to unlock analytics!")

# --- PROFILE TAB ---
with tab_profile:
    p_col1, p_col2 = st.columns([1, 2])
    
    with p_col1:
        st.markdown("### ⚙️ Settings")
        with st.form("profile_update"):
            new_name = st.text_input("Display Name", st.session_state.user_profile['name'])
            new_budget = st.number_input("Monthly Budget (₹)", value=st.session_state.user_profile['monthlyBudget'])
            new_goal = st.number_input("CO₂ Limit Goal (kg)", value=st.session_state.user_profile['co2Goal'])
            
            if st.form_submit_button("Update Profile"):
                st.session_state.user_profile.update({
                    'name': new_name,
                    'monthlyBudget': new_budget,
                    'co2Goal': new_goal
                })
                save_data({'purchases': st.session_state.purchases, 'user_profile': st.session_state.user_profile})
                st.success("Updated!")
                st.rerun()
                
        if st.button("🗑️ Reset All Data", type="secondary"):
            st.session_state.purchases = []
            st.session_state.user_profile['badges'] = []
            save_data(get_default_data())
            st.rerun()

    with p_col2:
        st.markdown(f"### 🏆 {st.session_state.user_profile['name']}'s Trophy Cabinet")
        
        my_badges = st.session_state.user_profile['badges']
        
        # Grid display for badges
        cols = st.columns(4)
        for idx, (badge_id, info) in enumerate(BADGES.items()):
            col = cols[idx % 4]
            with col:
                is_unlocked = badge_id in my_badges
                opacity = "1.0" if is_unlocked else "0.3"
                filter_css = "grayscale(0%)" if is_unlocked else "grayscale(100%)"
                border = "2px solid #FFD700" if is_unlocked else "2px dashed #ccc"
                
                st.markdown(
                    f"""
                    <div style="
                        text-align: center; 
                        padding: 15px; 
                        border-radius: 15px; 
                        border: {border};
                        background: rgba(255,255,255,0.5);
                        opacity: {opacity};
                        filter: {filter_css};
                        height: 150px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        transition: all 0.3s;
                    ">
                        <div style="font-size: 3rem; margin-bottom: 5px;">{info['icon']}</div>
                        <div style="font-weight: bold; font-size: 0.9rem;">{info['name']}</div>
                        <div style="font-size: 0.7rem; color: #555;">{info['desc']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# FOOTER
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; color: #999; font-size: 0.8rem;">
        Made with 💚 | ShopImpact v2.0 | <a href="#" style="color: #66bb6a; text-decoration: none;">Privacy Policy</a>
    </div>
    """, 
    unsafe_allow_html=True
)
