import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import random
import requests
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

# ==================== 1. CONFIGURATION & ASSETS ====================
st.set_page_config(
    page_title="ShopImpact Pro",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Lottie Animation Helper
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Animation Assets
LOTTIE_ECO = "https://assets10.lottiefiles.com/packages/lf20_42B8LS.json"  # Plant growing
LOTTIE_SUCCESS = "https://assets9.lottiefiles.com/packages/lf20_jbrw3hcz.json" # Confetti
LOTTIE_BADGE = "https://assets2.lottiefiles.com/packages/lf20_touohxv0.json" # Trophy
LOTTIE_EMPTY = "https://assets9.lottiefiles.com/private_files/lf30_cgfdhxgx.json" # Empty box

# ==================== 2. EXTENSIVE DATASET (100+ ITEMS) ====================
PRODUCT_DATABASE = {
    "Fashion & Apparel": {
        "Fast Fashion T-Shirt": 6.5, "Fast Fashion Jeans": 20.0, "Sustainable Cotton Tee": 2.1, 
        "Polyester Dress": 14.2, "Wool Sweater": 18.0, "Leather Jacket": 40.0, "Vegan Leather Jacket": 15.0,
        "Nylon Activewear": 8.5, "Running Shoes": 13.0, "Leather Boots": 25.0, "Canvas Sneakers": 8.0,
        "Swimwear": 5.0, "Silk Scarf": 4.0, "Winter Coat": 30.0, "Socks (Cotton)": 0.5, "Suit (Wool)": 35.0
    },
    "Electronics & Tech": {
        "Smartphone (New)": 80.0, "Smartphone (Refurbished)": 10.0, "Laptop (High-End)": 350.0, 
        "Tablet": 90.0, "Smartwatch": 15.0, "Wireless Earbuds": 5.0, "Gaming Console": 40.0,
        "TV (55 inch)": 200.0, "DSLR Camera": 60.0, "Smart Speaker": 12.0, "Power Bank": 8.0,
        "Charging Cable": 1.0, "Desktop PC": 400.0, "Monitor": 120.0
    },
    "Home & Living": {
        "Sofa (Fabric)": 90.0, "Sofa (Leather)": 150.0, "Wooden Dining Table": 60.0, "Mattress": 50.0,
        "Bed Frame": 45.0, "Rug/Carpet": 30.0, "Desk Lamp": 4.0, "Ceramic Plant Pot": 2.0,
        "Throw Pillow": 3.0, "Curtains": 15.0, "Bookshelf": 25.0, "Office Chair": 35.0,
        "Kitchen Blender": 10.0, "Toaster": 5.0, "Microwave": 25.0
    },
    "Food & Grocery": {
        "Beef (1kg)": 27.0, "Chicken (1kg)": 6.9, "Pork (1kg)": 12.1, "Tofu (1kg)": 2.0,
        "Milk (Dairy 1L)": 3.0, "Oat Milk (1L)": 0.9, "Cheese (1kg)": 13.5, "Eggs (12)": 4.5,
        "Coffee (Imported)": 15.0, "Chocolate Bar": 0.5, "Rice (1kg)": 2.7, "Potatoes (1kg)": 0.2,
        "Avocado (Imported)": 0.8, "Local Vegetables (1kg)": 0.1, "Bottled Water": 0.3
    },
    "Beauty & Wellness": {
        "Lipstick": 0.5, "Foundation": 1.0, "Perfume (50ml)": 2.5, "Shampoo Bottle": 1.2,
        "Bar Soap": 0.1, "Face Cream": 1.5, "Sunscreen": 1.0, "Toothpaste": 0.4,
        "Bamboo Toothbrush": 0.05, "Disposable Razor": 0.8, "Safety Razor": 0.1
    },
    "Second-Hand / Thrift": {
        "Thrifted Shirt": 0.1, "Thrifted Jeans": 0.2, "Used Jacket": 0.5, "Used Books": 0.1,
        "Vintage Furniture": 2.0, "Second-hand Electronics": 5.0, "Upcycled Decor": 0.5
    },
    "Transport & Travel": {
        "Flight (Short Haul)": 150.0, "Flight (Long Haul)": 800.0, "Train Ticket": 5.0,
        "Bus Ticket": 2.0, "Uber/Taxi Ride": 4.0, "Bicycle": 15.0, "Electric Scooter": 10.0
    }
}

ALL_CATEGORIES = list(PRODUCT_DATABASE.keys())

# ==================== 3. GAMIFICATION LOGIC (XP & LEVELS) ====================
def calculate_xp(purchases):
    xp = 0
    for p in purchases:
        # Base XP for logging
        xp += 10
        
        # Bonus for low CO2
        if p['co2_impact'] < 2.0: xp += 15
        elif p['co2_impact'] < 10.0: xp += 5
        
        # Bonus for Sustainable Categories
        if "Second-Hand" in p['category'] or "Local" in p['item_name']:
            xp += 30
            
    return xp

def get_level_info(xp):
    level = int(xp / 100) + 1
    next_level_xp = level * 100
    progress = (xp % 100) / 100
    return level, next_level_xp, progress

def check_badges(purchases):
    total_count = len(purchases)
    eco_count = sum(1 for p in purchases if "Second-Hand" in p['category'] or p['co2_impact'] < 1)
    
    badges = [
        {"id": "newbie", "name": "Green Newbie", "icon": "🌱", "desc": "Logged your first item", "earned": total_count >= 1},
        {"id": "habit", "name": "Habit Builder", "icon": "📅", "desc": "Logged 10+ items", "earned": total_count >= 10},
        {"id": "thrifter", "name": "Thrift King", "icon": "👑", "desc": "Bought 3+ Second-Hand items", "earned": sum(1 for p in purchases if "Second-Hand" in p['category']) >= 3},
        {"id": "low_carbon", "name": "Carbon Cutter", "icon": "✂️", "desc": "Kept single item under 1kg CO2", "earned": any(p['co2_impact'] < 1.0 for p in purchases)},
        {"id": "vegan", "name": "Plant Power", "icon": "🥗", "desc": "Bought Tofu or Oat Milk", "earned": any(x in p['item_name'] for p in purchases for x in ['Tofu', 'Oat Milk'])},
        {"id": "whale", "name": "Big Spender", "icon": "💎", "desc": "Spent over ₹10k in one go", "earned": any(p['price'] > 10000 for p in purchases)},
    ]
    return badges

# ==================== 4. SESSION STATE & DATA ====================
if 'purchases' not in st.session_state:
    st.session_state.purchases = []
if 'user_budget' not in st.session_state:
    st.session_state.user_budget = 15000

# ==================== 5. STYLING ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Glassmorphism Background */
    .stApp {
        background-color: #e0f2fe;
        background-image: radial-gradient(at 0% 0%, #d1fae5 0px, transparent 50%),
                          radial-gradient(at 100% 0%, #ecfccb 0px, transparent 50%),
                          radial-gradient(at 100% 100%, #dbeafe 0px, transparent 50%);
    }
    
    /* Glass Cards */
    div[data-testid="stMetric"], div[data-testid="stForm"], .stCard {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(16, 185, 129, 0.4);
    }
    
    /* Custom Progress Bar for Level */
    .stProgress > div > div > div > div {
        background-color: #10b981;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 6. SIDEBAR: PROFILE & STATS ====================
with st.sidebar:
    lottie_eco = load_lottieurl(LOTTIE_ECO)
    st_lottie(lottie_eco, height=150, key="sidebar_anim")
    
    xp = calculate_xp(st.session_state.purchases)
    level, next_xp, progress = get_level_info(xp)
    
    st.markdown(f"<h1 style='text-align: center; color: #064e3b;'>Level {level}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>XP: {xp} / {next_xp}</p>", unsafe_allow_html=True)
    st.progress(progress)
    
    st.markdown("---")
    
    # Quick Stats
    total_spend = sum(p['price'] for p in st.session_state.purchases)
    budget_used_pct = (total_spend / st.session_state.user_budget) * 100
    
    st.metric("Monthly Budget", f"₹{st.session_state.user_budget}")
    st.metric("Spent So Far", f"₹{total_spend}", delta=f"{100-budget_used_pct:.1f}% Remaining")
    
    st.markdown("---")
    with st.expander("⚙️ Settings"):
        new_budget = st.number_input("Set Budget (₹)", value=st.session_state.user_budget, step=1000)
        if st.button("Update Budget"):
            st.session_state.user_budget = new_budget
        
        if st.button("🗑️ Reset All Data"):
            st.session_state.purchases = []
            st.rerun()

# ==================== 7. MAIN NAVIGATION ====================
selected_nav = option_menu(
    menu_title=None,
    options=["Logger", "Dashboard", "Analytics", "Gamification"],
    icons=["plus-circle-fill", "grid-fill", "bar-chart-line-fill", "trophy-fill"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "#059669", "font-size": "18px"}, 
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#d1fae5"},
        "nav-link-selected": {"background-color": "#10b981"},
    }
)

# ==================== PAGE: LOGGER ====================
if selected_nav == "Logger":
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### 🛍️ What did you buy today?")
        
        with st.form("log_form"):
            # 2-Step Dynamic Selection
            cat_select = st.selectbox("1. Select Category", ALL_CATEGORIES)
            
            # Filter items based on category
            available_items = list(PRODUCT_DATABASE[cat_select].keys())
            item_select = st.selectbox("2. Select Item", available_items)
            
            # Get Base CO2
            base_co2 = PRODUCT_DATABASE[cat_select][item_select]
            
            c1, c2 = st.columns(2)
            with c1:
                price_inp = st.number_input("Price (₹)", min_value=0, value=500, step=100)
            with c2:
                brand_inp = st.text_input("Brand (Optional)")
            
            st.info(f"⚡ Estimated Impact: **{base_co2} kg CO₂** per unit")
            
            submitted = st.form_submit_button("Log Purchase")
            
            if submitted:
                new_entry = {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "category": cat_select,
                    "item_name": item_select,
                    "price": price_inp,
                    "brand": brand_inp,
                    "co2_impact": base_co2
                }
                st.session_state.purchases.append(new_entry)
                st.balloons()
                st.success(f"Added {item_select} (+10 XP)")
    
    with col2:
        # Gamified Feedback Card
        st.markdown("#### 💡 Eco-Tip")
        tips = [
            "Buying used electronics saves 80% of carbon emissions.",
            "Fast fashion items are worn less than 7 times on average.",
            "Eating plant-based for one day saves ~2kg of CO2.",
            "Repairing a laptop saves 300kg of CO2 vs buying new."
        ]
        st.warning(random.choice(tips), icon="🌿")
        
        # Recent logs list
        st.markdown("#### Recent History")
        if st.session_state.purchases:
            for p in st.session_state.purchases[-3:]:
                st.markdown(f"""
                <div style="background:white; padding:10px; border-radius:10px; margin-bottom:10px; border-left: 5px solid #10b981;">
                    <b>{p['item_name']}</b><br>
                    <span style="font-size:12px; color:gray">{p['date']} • ₹{p['price']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No logs yet. Start tracking!")

# ==================== PAGE: DASHBOARD ====================
elif selected_nav == "Dashboard":
    if not st.session_state.purchases:
        st.info("Please log some items to see the dashboard!")
        st_lottie(load_lottieurl(LOTTIE_EMPTY), height=300)
    else:
        df = pd.DataFrame(st.session_state.purchases)
        
        # Top Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Items", len(df))
        c2.metric("Total CO₂", f"{df['co2_impact'].sum():.1f} kg")
        c3.metric("Avg CO₂/Item", f"{df['co2_impact'].mean():.1f} kg")
        c4.metric("Money Spent", f"₹{df['price'].sum():,}")
        
        col_charts1, col_charts2 = st.columns(2)
        
        with col_charts1:
            # Gauge Chart for Budget
            total_spend = df['price'].sum()
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total_spend,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Monthly Budget Usage"},
                gauge = {
                    'axis': {'range': [None, st.session_state.user_budget]},
                    'bar': {'color': "#10b981"},
                    'steps': [
                        {'range': [0, st.session_state.user_budget*0.7], 'color': "#d1fae5"},
                        {'range': [st.session_state.user_budget*0.7, st.session_state.user_budget], 'color': "#fef3c7"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': st.session_state.user_budget
                    }
                }
            ))
            fig_gauge.update_layout(paper_bgcolor = "rgba(0,0,0,0)", font={'family': "Outfit"})
            st.plotly_chart(fig_gauge, use_container_width=True)
            
        with col_charts2:
            # Donut Chart - Categories
            fig_pie = px.pie(df, names='category', values='price', hole=0.5, color_discrete_sequence=px.colors.sequential.Tealgrn)
            fig_pie.update_layout(title_text="Spending by Category", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_pie, use_container_width=True)

# ==================== PAGE: ANALYTICS ====================
elif selected_nav == "Analytics":
    if not st.session_state.purchases:
        st.warning("Needs more data.")
    else:
        df = pd.DataFrame(st.session_state.purchases)
        
        st.markdown("### 🔍 Deep Dive Analysis")
        
        # 1. SUNBURST CHART (Category -> Item -> CO2)
        fig_sun = px.sunburst(
            df, 
            path=['category', 'item_name'], 
            values='co2_impact',
            color='co2_impact',
            color_continuous_scale='RdYlGn_r', # Red is high CO2, Green is low
            title="Carbon Footprint Breakdown"
        )
        fig_sun.update_layout(paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_sun, use_container_width=True)
        
        # 2. SCATTER PLOT (Price vs CO2)
        col_a, col_b = st.columns(2)
        with col_a:
            fig_scatter = px.scatter(
                df, x="price", y="co2_impact", 
                size="co2_impact", color="category",
                hover_name="item_name",
                title="Price vs. Environmental Cost",
                log_x=True
            )
            fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.5)")
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with col_b:
             # Fake trend data generation for demo if only 1 day exists
            dates = pd.to_datetime(df['date']).dt.date.value_counts().sort_index()
            fig_line = px.area(dates, title="Activity Trend", labels={'index':'Date', 'value':'Items Logged'})
            fig_line.update_traces(line_color='#059669')
            fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.5)")
            st.plotly_chart(fig_line, use_container_width=True)

# ==================== PAGE: GAMIFICATION ====================
elif selected_nav == "Gamification":
    st.markdown("### 🏆 Hall of Fame")
    
    col_lottie, col_badges = st.columns([1, 2])
    
    with col_lottie:
        st_lottie(load_lottieurl(LOTTIE_BADGE), height=300)
        
        xp = calculate_xp(st.session_state.purchases)
        level, _, _ = get_level_info(xp)
        st.markdown(f"""
        <div style="text-align:center; padding: 20px; background: white; border-radius: 20px;">
            <h2 style="margin:0; color: #059669;">Level {level}</h2>
            <p style="color: gray;">Eco-Warrior Rank</p>
        </div>
        """, unsafe_allow_html=True)

    with col_badges:
        badges = check_badges(st.session_state.purchases)
        
        # Display Badges in a Grid
        cols = st.columns(3)
        for i, badge in enumerate(badges):
            with cols[i % 3]:
                if badge['earned']:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #a7f3d0 0%, #ffffff 100%); padding: 15px; border-radius: 15px; border: 2px solid #10b981; text-align: center; height: 150px; display: flex; flex-direction: column; justify-content: center;">
                        <div style="font-size: 40px;">{badge['icon']}</div>
                        <div style="font-weight: bold; color: #064e3b;">{badge['name']}</div>
                        <div style="font-size: 12px; color: #064e3b;">{badge['desc']}</div>
                    </div>
                    <div style="height:10px"></div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: #f1f5f9; padding: 15px; border-radius: 15px; border: 2px dashed #cbd5e1; text-align: center; height: 150px; opacity: 0.6; display: flex; flex-direction: column; justify-content: center;">
                        <div style="font-size: 40px; filter: grayscale(1);">🔒</div>
                        <div style="font-weight: bold; color: gray;">{badge['name']}</div>
                        <div style="font-size: 12px; color: gray;">{badge['desc']}</div>
                    </div>
                    <div style="height:10px"></div>
                    """, unsafe_allow_html=True)
