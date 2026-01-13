import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random
import requests
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

# ==================== 1. CONFIGURATION & THEME ====================
st.set_page_config(
    page_title="EcoTrack Pro",
    page_icon="🌿",
    layout="wide"
)

# Custom CSS for High Visibility & Nature Aesthetics
st.markdown("""
<style>
    :root {
        --primary: #2D6A4F;
        --secondary: #95D5B2;
        --background: #F8F9FA;
        --text: #1B4332;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f0fff4 0%, #e6fffa 100%);
    }

    /* High Visibility Headers */
    h1, h2, h3 {
        color: #1B4332 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
    }

    /* Modern Card Styling */
    div[data-testid="stMetric"] {
        background: white;
        border-radius: 15px;
        padding: 15px;
        border-left: 5px solid #2D6A4F;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* Better Slider and Input Visibility */
    .stSlider > div > div > div > div {
        background-color: #2D6A4F;
    }
    
    .stButton > button {
        width: 100%;
        background-color: #2D6A4F;
        color: white;
        border-radius: 8px;
        height: 3em;
        transition: 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #1B4332;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 2. ASSETS & DATABASE ====================
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

LOTTIE_LEAF = "https://assets1.lottiefiles.com/packages/lf20_m6cuL6.json" # Nature loop
LOTTIE_CHART = "https://assets3.lottiefiles.com/packages/lf20_qp1q7mct.json" # Analytics

# Expanded Brand Database
BRANDS = {
    "Fashion & Apparel": ["Patagonia", "Levi's", "H&M", "Zara", "Adidas", "Local Thrift", "Everlane"],
    "Electronics & Tech": ["Apple", "Samsung", "Dell", "HP", "Back Market (Refurb)", "Sony"],
    "Home & Living": ["IKEA", "West Elm", "Target", "Local Woodshop", "Second-hand"],
    "Food & Grocery": ["Whole Foods", "Local Farmers Market", "Walmart", "Tesco", "Aldi"],
    "Beauty & Wellness": ["Lush", "The Body Shop", "Sephora", "Ordinary", "Dr. Bronner's"]
}

PRODUCT_DATA = {
    "Fashion & Apparel": {"T-Shirt": 6.5, "Jeans": 20.0, "Sneakers": 13.0, "Coat": 30.0},
    "Electronics & Tech": {"Smartphone": 70.0, "Laptop": 300.0, "Tablet": 85.0, "Monitor": 110.0},
    "Food & Grocery": {"Beef (1kg)": 27.0, "Chicken (1kg)": 6.9, "Plant-based Meal": 1.5, "Dairy Milk": 3.0},
    "Home & Living": {"Chair": 20.0, "Table": 50.0, "Bedding": 10.0, "Decor": 5.0}
}

# ==================== 3. DATA LOGIC ====================
if 'purchases' not in st.session_state:
    st.session_state.purchases = []

def add_purchase(cat, item, price, brand):
    co2 = PRODUCT_DATA[cat][item]
    # Simple logic: Thrift/Refurbished brands reduce impact by 70%
    if "Thrift" in brand or "Refurb" in brand or "Second-hand" in brand:
        co2 = co2 * 0.3
        
    st.session_state.purchases.append({
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Category": cat,
        "Item": item,
        "Price": price,
        "Brand": brand,
        "CO2": co2,
        "Intensity": co2 / (price if price > 0 else 1)
    })

# ==================== 4. SIDEBAR & NAV ====================
with st.sidebar:
    st_lottie(load_lottieurl(LOTTIE_LEAF), height=150)
    st.title("EcoTrack Pro")
    
    selected = option_menu(
        menu_title=None,
        options=["Track", "Analytics", "Badges"],
        icons=["plus-circle", "pie-chart", "award"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"background-color": "#f0fff4"},
            "nav-link-selected": {"background-color": "#2D6A4F"},
        }
    )
    
    st.divider()
    if st.button("🍃 Clear All Data"):
        st.session_state.purchases = []
        st.rerun()

# ==================== 5. PAGES ====================

if selected == "Track":
    st.subheader("🛒 Log New Purchase")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.container():
            c1, c2 = st.columns(2)
            category = c1.selectbox("Category", list(PRODUCT_DATA.keys()))
            item = c2.selectbox("Item Type", list(PRODUCT_DATA[category].keys()))
            
            # Interactive Slider for Price
            price = st.select_slider(
                "Purchase Price (₹)",
                options=[0, 100, 500, 1000, 5000, 10000, 25000, 50000, 100000],
                value=1000
            )
            
            brand = st.selectbox("Brand / Source", BRANDS.get(category, ["Generic"]))
            
            if st.button("Confirm Purchase"):
                add_purchase(category, item, price, brand)
                st.success(f"Successfully logged {item} from {brand}!")
                st.balloons()

    with col2:
        st.info("**Environmental Impact Tip:**")
        if "Thrift" in brand or "Refurb" in brand:
            st.write("🌟 **Great choice!** Buying second-hand reduces the carbon footprint of this item by approximately 70%.")
        else:
            st.write("🌿 Consider checking 'Local Thrift' or 'Refurbished' options next time to earn more XP!")

# [attachment_0](attachment)

elif selected == "Analytics":
    if not st.session_state.purchases:
        st.warning("No data found. Start tracking your purchases to see insights!")
    else:
        df = pd.DataFrame(st.session_state.purchases)
        
        # Metric Row
        m1, m2, m3 = st.columns(3)
        total_co2 = df['CO2'].sum()
        m1.metric("Total Carbon Footprint", f"{total_co2:.1f} kg")
        m2.metric("Total Investment", f"₹{df['Price'].sum():,}")
        m3.metric("Avg Intensity", f"{df['Intensity'].mean():.2f} CO2/₹")

        st.divider()
        
        # Advanced Visuals
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("### 📊 CO2 Distribution")
            fig_pie = px.sunburst(df, path=['Category', 'Brand'], values='CO2',
                                 color='CO2', color_continuous_scale='Greens')
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_right:
            st.markdown("### 💸 Price vs Impact")
            # This helps users see if expensive items are actually better/worse
            fig_scatter = px.scatter(df, x="Price", y="CO2", size="CO2", 
                                   color="Category", hover_name="Item",
                                   template="plotly_white")
            st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("### 🕒 Impact Timeline")
        fig_line = px.area(df, x="Date", y="CO2", color="Category", 
                          line_group="Category", title="Daily Carbon Load")
        st.plotly_chart(fig_line, use_container_width=True)

elif selected == "Badges":
    st.subheader("🏆 Your Eco-Achievements")
    
    if not st.session_state.purchases:
        st_lottie(load_lottieurl("https://assets9.lottiefiles.com/private_files/lf30_cgfdhxgx.json"), height=200)
        st.write("Log your first item to unlock badges!")
    else:
        df = pd.DataFrame(st.session_state.purchases)
        
        # Badge Logic
        badges = [
            ("Green Starter", "First item logged!", len(df) > 0),
            ("Thrift Master", "Bought 2+ second-hand items", len(df[df['Brand'].str.contains("Thrift|Refurb", na=False)]) >= 2),
            ("Big Saver", "Kept total CO2 under 50kg", df['CO2'].sum() < 50),
            ("High Roller", "Spent over ₹10k on eco-friendly items", df['Price'].sum() > 10000)
        ]
        
        cols = st.columns(2)
        for i, (name, desc, earned) in enumerate(badges):
            with cols[i % 2]:
                status = "✅" if earned else "🔒"
                color = "#D8F3DC" if earned else "#F1F5F9"
                st.markdown(f"""
                <div style="background-color: {color}; padding: 20px; border-radius: 15px; border: 2px solid #2D6A4F; margin-bottom: 10px;">
                    <h4>{status} {name}</h4>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.sidebar.markdown("---")
st.sidebar.caption("v2.0 • Optimized for Nature & Clarity")
# Add these imports at the top
import io

# ==================== NEW FEATURES ADDED BELOW ====================

# 1. SUSTAINABLE COMPARISON TOOL (Add to "Track" or a new section)
if selected == "Track":
    # ... (previous logging code) ...
    
    st.divider()
    st.subheader("⚖️ Sustainable Comparison Tool")
    st.info("Compare the impact of your purchase before you log it.")
    
    comp_col1, comp_col2 = st.columns(2)
    with comp_col1:
        comp_cat = st.selectbox("Select Category to Compare", list(PRODUCT_DATA.keys()), key="comp_cat")
        comp_item = st.selectbox("Select Item", list(PRODUCT_DATA[comp_cat].keys()), key="comp_item")
    
    base_impact = PRODUCT_DATA[comp_cat][comp_item]
    thrift_impact = base_impact * 0.3 # 70% reduction for second-hand
    savings = base_impact - thrift_impact

    with comp_col2:
        st.write(f"**Standard Impact:** {base_impact} kg CO₂")
        st.write(f"**Eco-Option Impact:** {thrift_impact:.1f} kg CO₂")
        st.success(f"Potential Savings: **{savings:.1f} kg CO₂**")

    # 

# 2. DATA EXPORT FEATURE (Add to "Analytics")
elif selected == "Analytics":
    if not st.session_state.purchases:
        st.warning("No data to export.")
    else:
        # ... (previous analytics charts) ...
        
        st.divider()
        st.subheader("📥 Export Your Data")
        
        # Convert DataFrame to CSV
        df = pd.DataFrame(st.session_state.purchases)
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Download Shopping History as CSV",
            data=csv,
            file_name=f"ecotrack_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv',
            help="Download your logs to open in Excel or Google Sheets"
        )

# 3. ADVANCED BRAND FILTERING (Improved Analytics)
        st.markdown("### 🏷️ Brand Performance")
        brand_perf = df.groupby('Brand')['CO2'].mean().reset_index()
        fig_brand = px.bar(brand_perf, x='Brand', y='CO2', 
                          title="Average Carbon Intensity by Brand",
                          color='CO2', color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig_brand, use_container_width=True)

