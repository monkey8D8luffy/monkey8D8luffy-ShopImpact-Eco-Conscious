"""
ShopImpact - Streamlit Version (Optimized)
A colorful, interactive, and friendly web app to help users become mindful, eco-conscious shoppers.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="ShopImpact 🍃",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CONSTANTS ====================
PRODUCT_MULTIPLIERS = {
    'Fast Fashion': 2.5,
    'Electronics': 1.8,
    'Local Groceries': 0.3,
    'Second-Hand Item': 0.1,
    'Restaurant Meal': 0.8,
    'Leather Goods': 3.0,
    'Cosmetics': 1.5,
    'Home Decor': 1.2,
    'Books (New)': 0.5,
    'Books (Used)': 0.05,
}

ETHICAL_ALTERNATIVES = {
    'Fast Fashion': ['Vinted', 'ThredUp', 'Patagonia', 'Shop local', 'Rent the Runway'],
    'Electronics': ['BackMarket (Refurbished)', 'Framework', 'Fairphone', 'Buy used'],
    'Local Groceries': ['Keep it up! 🌱', 'Farmers markets', 'Zero-waste stores'],
    'Second-Hand Item': ['Amazing choice! 🎉', 'Keep shopping second-hand'],
    'Restaurant Meal': ['Plant-based options', 'Local restaurants', 'Cook at home'],
    'Leather Goods': ['Piñatex', 'Cork leather', 'Recycled materials', 'Vintage stores'],
    'Cosmetics': ['Lush', 'Ethique', 'Package-free brands', 'DIY natural products'],
    'Home Decor': ['Upcycle old items', 'Thrift stores', 'Support local artisans'],
    'Books (New)': ['Library', 'Buy used', 'Digital books', 'Book swaps'],
    'Books (Used)': ['Perfect! Keep it up! 📚'],
}

POPULAR_BRANDS = {
    'Fast Fashion': ['Zara', 'H&M', 'Forever 21', 'Shein', 'Uniqlo', 'Gap', 'Fashion Nova', 'Custom / Other'],
    'Electronics': ['Apple', 'Samsung', 'Dell', 'HP', 'Sony', 'LG', 'Microsoft', 'Google', 'Custom / Other'],
    'Local Groceries': ['Whole Foods', "Trader Joe's", 'Local Farm', 'Farmers Market', 'Co-op', 'Custom / Other'],
    'Second-Hand Item': ['Goodwill', 'ThredUp', 'Vinted', 'Poshmark', 'eBay', 'Depop', 'Local Thrift', 'Custom / Other'],
    'Restaurant Meal': ["McDonald's", 'Chipotle', 'Subway', 'Starbucks', 'Local Restaurant', 'Custom / Other'],
    'Leather Goods': ['Coach', 'Michael Kors', 'Fossil', 'Gucci', 'Prada', 'Local Artisan', 'Custom / Other'],
    'Cosmetics': ['Sephora', 'Ulta', 'MAC', 'Lush', 'The Body Shop', 'Custom / Other'],
    'Home Decor': ['IKEA', 'Target', 'HomeGoods', 'West Elm', 'CB2', 'Local Store', 'Custom / Other'],
    'Books (New)': ['Amazon', 'Barnes & Noble', 'Local Bookstore', 'Custom / Other'],
    'Books (Used)': ['ThriftBooks', 'Better World Books', 'Local Used Bookstore', 'Library Sale', 'Custom / Other'],
}

TIPS_LIST = [
    '🌍 Buying second-hand reduces CO₂ by up to 80% compared to new items!',
    '🌱 Local produce has 5x less carbon footprint than imported goods.',
    '♻️ Repairing items instead of replacing them can save tons of emissions.',
    '🚶‍♀️ Walking or biking to the store? You\'re already making an impact!',
    '🎒 Bringing your own bag saves about 6kg of CO₂ per year.',
    '💚 Every conscious choice counts - you\'re doing great!',
    '🌾 Plant-based meals typically have 50% less carbon impact.',
    '📦 Avoid same-day delivery - consolidated shipping is greener!',
]

MOTIVATIONAL_QUOTES = [
    "Every purchase is a vote for the kind of world you want to live in.",
    "Small changes, big impact! 🌍",
    "The future depends on what you do today.",
    "Be the change you wish to see in the world.",
    "Conscious choices create a better tomorrow.",
    "Your actions inspire others to be better too.",
    "Sustainability is not a trend, it's a responsibility.",
]

ECO_STANDARDS = {
    'monthlyCO2': 100,
    'monthlyBudget': 15000,
    'ecoFriendlyPercentage': 30,
}

SPENDING_BADGES = [
    {'name': 'Frugal Shopper', 'icon': '💰', 'limit': 5000, 'type': 'spend', 'description': 'Spend under ₹5,000/month'},
    {'name': 'Budget Conscious', 'icon': '🎯', 'limit': 10000, 'type': 'spend', 'description': 'Spend under ₹10,000/month'},
    {'name': 'Mindful Spender', 'icon': '🌟', 'limit': 15000, 'type': 'spend', 'description': 'Spend under ₹15,000/month'},
    {'name': 'Carbon Neutral Goal', 'icon': '🌱', 'limit': 50, 'type': 'co2', 'description': 'Keep CO₂ under 50kg/month'},
    {'name': 'Eco Warrior', 'icon': '🦸', 'limit': 30, 'type': 'co2', 'description': 'Keep CO₂ under 30kg/month'},
]

# Additional badges from React version
ACHIEVEMENT_BADGES = [
    {'name': 'Low Impact Shopper', 'icon': '🌱', 'condition': 'eco_friendly_5', 'description': '5+ eco-friendly items'},
    {'name': 'Second-Hand Hero', 'icon': '♻️', 'condition': 'second_hand_3', 'description': '3+ second-hand items'},
    {'name': 'Tracking Champion', 'icon': '📊', 'condition': 'purchases_10', 'description': '10+ purchases logged'},
    {'name': 'Carbon Minimalist', 'icon': '✨', 'condition': 'avg_co2_low', 'description': 'Avg CO₂ < 1.0 kg'},
]

ECO_FRIENDLY_CATEGORIES = ['Second-Hand Item', 'Local Groceries', 'Books (Used)']

DATA_FILE = Path("shopimpact_data.json")

# ==================== SVG ECO GRAPHIC ====================
def get_eco_graphic_svg(animate: bool = False) -> str:
    """Generate SVG eco graphic (leaf with sparkles)"""
    animation_class = 'eco-graphic-animate' if animate else ''
    sparkles_html = ""
    if animate:
        sparkles_html = """
            <circle cx="60" cy="50" r="3" fill="#fbbf24" class="sparkle sparkle-1"></circle>
            <circle cx="140" cy="70" r="2" fill="#fbbf24" class="sparkle sparkle-2"></circle>
            <circle cx="130" cy="140" r="3" fill="#fbbf24" class="sparkle sparkle-3"></circle>
            <circle cx="70" cy="150" r="2" fill="#fbbf24" class="sparkle sparkle-4"></circle>
        """
    
    # Use a unique ID for the gradient to avoid conflicts
    gradient_id = f"leafGradient{random.randint(1000, 9999)}"
    
    svg_html = f"""
    <div style="text-align: center; margin: 10px 0;">
        <svg width="200" height="200" viewBox="0 0 200 200" class="{animation_class}" style="margin: 0 auto; display: block;">
            <defs>
                <linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#22c55e;stop-opacity:1"></stop>
                    <stop offset="100%" style="stop-color:#16a34a;stop-opacity:1"></stop>
                </linearGradient>
            </defs>
            
            <ellipse cx="100" cy="100" rx="60" ry="80" fill="url(#{gradient_id})" transform="rotate(-20 100 100)"></ellipse>
            
            <line x1="70" y1="60" x2="120" y2="140" stroke="#15803d" stroke-width="3"></line>
            
            <line x1="88" y1="80" x2="60" y2="90" stroke="#15803d" stroke-width="2" opacity="0.7"></line>
            <line x1="95" y1="95" x2="65" y2="110" stroke="#15803d" stroke-width="2" opacity="0.7"></line>
            <line x1="102" y1="110" x2="72" y2="130" stroke="#15803d" stroke-width="2" opacity="0.7"></line>
            <line x1="105" y1="85" x2="135" y2="95" stroke="#15803d" stroke-width="2" opacity="0.7"></line>
            <line x1="112" y1="105" x2="142" y2="115" stroke="#15803d" stroke-width="2" opacity="0.7"></line>
            
            {sparkles_html}
            
            <g opacity="0.3">
                <ellipse cx="100" cy="160" rx="15" ry="10" fill="#064e3b"></ellipse>
                <circle cx="90" cy="150" r="4" fill="#064e3b"></circle>
                <circle cx="95" cy="148" r="3" fill="#064e3b"></circle>
                <circle cx="100" cy="147" r="3" fill="#064e3b"></circle>
                <circle cx="105" cy="148" r="3" fill="#064e3b"></circle>
                <circle cx="110" cy="150" r="4" fill="#064e3b"></circle>
            </g>
        </svg>
    </div>
    """
    
    return svg_html

# ==================== DATA PERSISTENCE ====================
@st.cache_data
def load_data_cached() -> Dict:
    """Load data from JSON file (cached)"""
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return get_default_data()
    return get_default_data()

def save_data(data: Dict) -> None:
    """Save data to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        # Clear cache to reload fresh data
        load_data_cached.clear()
    except Exception as e:
        st.error(f"Error saving data: {e}")

def get_default_data() -> Dict:
    """Return default data structure"""
    return {
        'purchases': [],
        'user_profile': {
            'name': '',
            'age': '',
            'location': '',
            'monthlyBudget': 15000,
            'co2Goal': 50,
            'joinDate': datetime.now().strftime('%Y-%m-%d')
        },
        'settings': {
            'highContrast': False
        }
    }

# ==================== SESSION STATE INITIALIZATION ====================
if 'initialized' not in st.session_state:
    data = load_data_cached()
    st.session_state.purchases = data.get('purchases', [])
    st.session_state.user_profile = data.get('user_profile', get_default_data()['user_profile'])
    st.session_state.settings = data.get('settings', get_default_data()['settings'])
    st.session_state.show_success = False
    st.session_state.success_message = ''
    st.session_state.show_delete_confirm = False
    st.session_state.show_celebration = False
    st.session_state.initialized = True

# ==================== HELPER FUNCTIONS ====================
@st.cache_data
def calculate_co2(price: float, product_type: str) -> float:
    """Calculate CO2 impact based on price and product type"""
    multiplier = PRODUCT_MULTIPLIERS.get(product_type, 1.0)
    return round(price * multiplier, 2)

@st.cache_data
def get_monthly_stats(purchases: tuple) -> Dict:
    """Calculate statistics for current month (cached for performance)"""
    purchases = list(purchases)
    
    if not purchases:
        return {'totalSpend': 0, 'totalCO2': 0, 'ecoFriendlyPercent': 0, 'totalPurchases': 0}
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    monthly_purchases = [
        p for p in purchases 
        if datetime.strptime(p['date'], '%Y-%m-%d').month == current_month 
        and datetime.strptime(p['date'], '%Y-%m-%d').year == current_year
    ]
    
    if not monthly_purchases:
        return {'totalSpend': 0, 'totalCO2': 0, 'ecoFriendlyPercent': 0, 'totalPurchases': 0}
    
    total_spend = sum(p['price'] for p in monthly_purchases)
    total_co2 = sum(p['co2_impact'] for p in monthly_purchases)
    eco_friendly_count = sum(
        1 for p in monthly_purchases 
        if p['type'] in ECO_FRIENDLY_CATEGORIES
    )
    eco_friendly_percent = (eco_friendly_count / len(monthly_purchases)) * 100 if monthly_purchases else 0
    
    return {
        'totalSpend': round(total_spend, 2),
        'totalCO2': round(total_co2, 2),
        'ecoFriendlyPercent': round(eco_friendly_percent, 2),
        'totalPurchases': len(monthly_purchases)
    }

def get_all_badges(purchases: List[Dict], monthly_stats: Dict) -> List[Dict]:
    """Get all earned badges (spending + achievements)"""
    earned = []
    
    # Spending badges
    for badge in SPENDING_BADGES:
        if badge['type'] == 'co2':
            if 0 < monthly_stats['totalCO2'] <= badge['limit']:
                earned.append(badge)
        else:
            if 0 < monthly_stats['totalSpend'] <= badge['limit']:
                earned.append(badge)
    
    # Achievement badges
    eco_friendly_count = sum(1 for p in purchases if p['type'] in ECO_FRIENDLY_CATEGORIES)
    second_hand_count = sum(1 for p in purchases if p['type'] == 'Second-Hand Item')
    avg_co2 = monthly_stats['totalCO2'] / monthly_stats['totalPurchases'] if monthly_stats['totalPurchases'] > 0 else 0
    
    for badge in ACHIEVEMENT_BADGES:
        if badge['condition'] == 'eco_friendly_5' and eco_friendly_count >= 5:
            earned.append(badge)
        elif badge['condition'] == 'second_hand_3' and second_hand_count >= 3:
            earned.append(badge)
        elif badge['condition'] == 'purchases_10' and len(purchases) >= 10:
            earned.append(badge)
        elif badge['condition'] == 'avg_co2_low' and avg_co2 < 1.0 and len(purchases) >= 3:
            earned.append(badge)
    
    return earned

def add_purchase(product_type: str, brand: str, price: float) -> None:
    """Add a new purchase to the session state and save to file"""
    co2_impact = calculate_co2(price, product_type)
    purchase = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'type': product_type,
        'brand': brand,
        'price': float(price),
        'co2_impact': float(co2_impact)
    }
    st.session_state.purchases.append(purchase)
    
    # Save to file
    save_data({
        'purchases': st.session_state.purchases,
        'user_profile': st.session_state.user_profile,
        'settings': st.session_state.settings
    })
    
    # Set success message and celebration
    if product_type in ECO_FRIENDLY_CATEGORIES:
        st.session_state.success_message = f"🌟 Eco-friendly choice! You're making a difference!"
        st.session_state.show_celebration = True
        st.balloons()
    else:
        st.session_state.success_message = f"✅ Logged! Your {product_type} added {co2_impact:.1f} kg of CO₂."
        st.session_state.show_celebration = False
    st.session_state.show_success = True

def delete_purchase(index: int) -> None:
    """Delete a purchase by index"""
    if 0 <= index < len(st.session_state.purchases):
        st.session_state.purchases.pop(index)
        save_data({
            'purchases': st.session_state.purchases,
            'user_profile': st.session_state.user_profile,
            'settings': st.session_state.settings
        })

# ==================== VISUALIZATION FUNCTIONS ====================
@st.cache_data
def create_co2_by_category_chart(purchases_tuple: tuple, high_contrast: bool = False) -> go.Figure:
    """Create bar chart for CO2 by category"""
    purchases = list(purchases_tuple)
    if not purchases:
        return None
    
    df = pd.DataFrame(purchases)
    category_data = df.groupby('type')['co2_impact'].sum().reset_index()
    category_data.columns = ['Category', 'CO2 (kg)']
    category_data = category_data.sort_values('CO2 (kg)', ascending=False)
    
    color_scale = 'Greys' if high_contrast else 'Greens'
    
    fig = px.bar(
        category_data,
        x='Category',
        y='CO2 (kg)',
        color='CO2 (kg)',
        color_continuous_scale=color_scale,
        title='CO₂ Impact by Category'
    )
    
    bg_color = '#000000' if high_contrast else 'rgba(0,0,0,0)'
    text_color = '#FFFFFF' if high_contrast else '#374151'
    
    fig.update_layout(
        showlegend=False,
        xaxis_tickangle=-45,
        height=400,
        margin=dict(l=20, r=20, t=40, b=100),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color)
    )
    return fig

@st.cache_data
def create_cumulative_co2_chart(purchases_tuple: tuple, high_contrast: bool = False) -> go.Figure:
    """Create line chart for cumulative CO2 over time"""
    purchases = list(purchases_tuple)
    if not purchases:
        return None
    
    df = pd.DataFrame(purchases)
    df = df.sort_values('date')
    df['cumulative_co2'] = df['co2_impact'].cumsum()
    
    line_color = '#FFFFFF' if high_contrast else '#16a34a'
    bg_color = '#000000' if high_contrast else 'rgba(0,0,0,0)'
    text_color = '#FFFFFF' if high_contrast else '#374151'
    
    fig = px.line(
        df,
        x='date',
        y='cumulative_co2',
        markers=True,
        labels={'cumulative_co2': 'Cumulative CO₂ (kg)', 'date': 'Date'},
        title='Cumulative CO₂ Over Time'
    )
    fig.update_traces(line_color=line_color, line_width=3, marker=dict(size=8))
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=40),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color)
    )
    return fig

@st.cache_data
def create_spending_by_category_chart(purchases_tuple: tuple, high_contrast: bool = False) -> go.Figure:
    """Create pie chart for spending by category"""
    purchases = list(purchases_tuple)
    if not purchases:
        return None
    
    df = pd.DataFrame(purchases)
    category_data = df.groupby('type')['price'].sum().reset_index()
    category_data.columns = ['Category', 'Spending']
    
    color_scale = px.colors.sequential.Greys if high_contrast else px.colors.sequential.Greens_r
    bg_color = '#000000' if high_contrast else 'rgba(0,0,0,0)'
    text_color = '#FFFFFF' if high_contrast else '#374151'
    
    fig = px.pie(
        category_data,
        values='Spending',
        names='Category',
        title='Spending Distribution',
        color_discrete_sequence=color_scale
    )
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor=bg_color,
        font=dict(color=text_color)
    )
    return fig

# ==================== CUSTOM CSS ====================
def get_custom_css(high_contrast: bool = False) -> str:
    """Generate custom CSS based on contrast mode"""
    if high_contrast:
        return """
        <style>
            /* High Contrast Mode */
            .main {
                background: #000000 !important;
                color: #FFFFFF !important;
            }
            
            .stTabs [data-baseweb="tab-list"] {
                background-color: #1a1a1a !important;
                border: 2px solid #FFFFFF !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                color: #FFFFFF !important;
                border: 1px solid #FFFFFF !important;
            }
            
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background-color: #FFFFFF !important;
                color: #000000 !important;
            }
            
            /* Cards */
            .eco-card, .tip-card, .quote-card, .badge-card, .stat-card {
                background-color: #1a1a1a !important;
                border: 2px solid #FFFFFF !important;
                color: #FFFFFF !important;
            }
            
            /* Buttons */
            .stButton > button {
                border: 2px solid #FFFFFF !important;
                color: #FFFFFF !important;
                background-color: #000000 !important;
            }
            
            .stButton > button:hover {
                background-color: #FFFFFF !important;
                color: #000000 !important;
            }
            
            /* Forms */
            .stTextInput > div > div > input,
            .stNumberInput > div > div > input,
            .stSelectbox > div > div {
                background-color: #1a1a1a !important;
                color: #FFFFFF !important;
                border: 2px solid #FFFFFF !important;
            }
            
            /* Metrics */
            [data-testid="stMetricValue"] {
                color: #FFFFFF !important;
            }
            
            /* Text */
            h1, h2, h3, h4, h5, h6, p, span, label {
                color: #FFFFFF !important;
            }
            
            /* Dataframe */
            .stDataFrame {
                border: 2px solid #FFFFFF !important;
            }
            
            /* Animation */
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-20px); }
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.3; }
            }
            
            .eco-graphic-animate {
                animation: bounce 1s ease-in-out 3;
            }
            
            .sparkle {
                animation: pulse 1.5s ease-in-out infinite;
            }
            
            .sparkle-1 { animation-delay: 0s; }
            .sparkle-2 { animation-delay: 0.2s; }
            .sparkle-3 { animation-delay: 0.4s; }
            .sparkle-4 { animation-delay: 0.6s; }
        </style>
        """
    else:
        return """
        <style>
            /* Normal Mode */
            .main {
                background: linear-gradient(135deg, #f0fdf4 0%, #dbeafe 50%, #d1fae5 100%);
            }
            
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background-color: white;
                border-radius: 10px;
                padding: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .stTabs [data-baseweb="tab"] {
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
            }
            
            /* Card styles */
            .eco-card {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border: 2px solid #10b981;
                margin: 10px 0;
            }
            
            .badge-card {
                background-color: #d1fae5;
                padding: 15px;
                border-radius: 10px;
                border: 2px solid #10b981;
                margin: 10px 0;
                text-align: center;
            }
            
            .tip-card {
                background-color: #dbeafe;
                padding: 15px;
                border-radius: 10px;
                border-left: 4px solid #3b82f6;
                margin: 10px 0;
            }
            
            .quote-card {
                background-color: #e9d5ff;
                padding: 15px;
                border-radius: 10px;
                border-left: 4px solid #a855f7;
                margin: 10px 0;
            }
            
            .stat-card {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
            }
            
            /* Button improvements */
            .stButton > button {
                border-radius: 8px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            /* Form improvements */
            .stNumberInput > div > div > input,
            .stTextInput > div > div > input,
            .stSelectbox > div > div > div {
                border-radius: 8px;
            }
            
            /* Metric styling */
            [data-testid="stMetricValue"] {
                font-size: 28px;
                font-weight: bold;
            }
            
            /* Animation */
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-20px); }
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.3; }
            }
            
            .eco-graphic-animate {
                animation: bounce 1s ease-in-out 3;
            }
            
            .sparkle {
                animation: pulse 1.5s ease-in-out infinite;
            }
            
            .sparkle-1 { animation-delay: 0s; }
            .sparkle-2 { animation-delay: 0.2s; }
            .sparkle-3 { animation-delay: 0.4s; }
            .sparkle-4 { animation-delay: 0.6s; }
        </style>
        """

# Apply CSS
high_contrast = st.session_state.settings.get('highContrast', False)
st.markdown(get_custom_css(high_contrast), unsafe_allow_html=True)

# ==================== HEADER ====================
header_color = '#FFFFFF' if high_contrast else '#16a34a'
subheader_color = '#CCCCCC' if high_contrast else '#6b7280'
welcome_color = '#FFFFFF' if high_contrast else '#16a34a'

st.markdown(f"<h1 style='text-align: center; color: {header_color};'>🍃 ShopImpact 🍃</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: {subheader_color}; font-size: 18px;'>Your friendly guide to conscious shopping.</p>", unsafe_allow_html=True)

if st.session_state.user_profile['name']:
    st.markdown(f"<p style='text-align: center; color: {welcome_color}; font-size: 16px;'>Welcome back, {st.session_state.user_profile['name']}! 🌟</p>", unsafe_allow_html=True)

st.markdown("---")

# ==================== NAVIGATION TABS ====================
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "👤 Profile", "📈 Analytics"])

# ==================== DASHBOARD TAB ====================
with tab1:
    col_main, col_sidebar = st.columns([2.5, 1])
    
    with col_main:
        # Purchase Form
        st.markdown("### 🛍️ Log a Purchase")
        
        with st.form("purchase_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                product_type = st.selectbox(
                    "Product Type",
                    options=list(PRODUCT_MULTIPLIERS.keys()),
                    key="product_type",
                    help="Select the type of product you're purchasing"
                )
            
            with col2:
                brands_list = POPULAR_BRANDS.get(product_type, ['Custom / Other'])
                selected_brand = st.selectbox(
                    "Brand",
                    options=brands_list,
                    key="brand",
                    help="Select brand or choose 'Custom / Other'"
                )
            
            if selected_brand == 'Custom / Other':
                custom_brand = st.text_input(
                    "Enter Custom Brand Name",
                    placeholder="e.g., Nike, Apple, Local Farm...",
                    help="Enter the brand name"
                )
                final_brand = custom_brand if custom_brand else "Custom"
            else:
                final_brand = selected_brand
            
            price = st.number_input(
                "Price (₹)",
                min_value=0,
                step=1,
                value=0,
                key="price",
                help="Enter the price in Indian Rupees"
            )
            
            # Show estimated CO2
            if price > 0:
                estimated_co2 = calculate_co2(price, product_type)
                
                # Color code based on impact
                if product_type in ECO_FRIENDLY_CATEGORIES:
                    st.success(f"✨ **Estimated CO₂ Impact:** {estimated_co2:.1f} kg (Eco-friendly!)")
                elif estimated_co2 > 100:
                    st.warning(f"⚠️ **Estimated CO₂ Impact:** {estimated_co2:.1f} kg (High impact)")
                else:
                    st.info(f"📊 **Estimated CO₂ Impact:** {estimated_co2:.1f} kg")
            
            submit_col1, submit_col2 = st.columns([3, 1])
            with submit_col2:
                submit_button = st.form_submit_button("✅ Log Purchase", type="primary", use_container_width=True)
            
            if submit_button:
                if price <= 0:
                    st.error("⚠️ Please enter a valid price greater than 0.")
                elif not final_brand or final_brand == "Custom":
                    st.error("⚠️ Please enter a brand name.")
                else:
                    add_purchase(product_type, final_brand, price)
                    st.rerun()
        
        # Show success message
        if st.session_state.show_success:
            st.success(st.session_state.success_message)
            st.session_state.show_success = False
        
        # Show alternatives and eco graphic
        if st.session_state.purchases:
            last_purchase = st.session_state.purchases[-1]
            alternatives = ETHICAL_ALTERNATIVES.get(last_purchase['type'], [])
            
            col_alt, col_graphic = st.columns([2, 1])
            
            with col_alt:
                if alternatives:
                    is_eco = last_purchase['type'] in ECO_FRIENDLY_CATEGORIES
                    
                    if is_eco:
                        st.markdown(f"""
                        <div style="background-color: {'#1a5f3a' if high_contrast else '#d1fae5'}; 
                                    padding: 15px; border-radius: 10px; 
                                    border-left: 4px solid {'#FFFFFF' if high_contrast else '#10b981'}; margin: 10px 0;
                                    color: {'#FFFFFF' if high_contrast else '#000000'};">
                            <h4 style="color: {'#FFFFFF' if high_contrast else '#16a34a'}; margin-top: 0;">🎉 Amazing Choice!</h4>
                            <ul style="margin-bottom: 0;">
                                {''.join([f'<li>{alt}</li>' for alt in alternatives])}
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="tip-card" style="background-color: {'#1a3a5f' if high_contrast else '#dbeafe'};">
                            <h4 style="color: {'#FFFFFF' if high_contrast else '#2563eb'}; margin-top: 0;">✨ Greener choices for {last_purchase['type']}:</h4>
                            <ul style="margin-bottom: 0;">
                                {''.join([f'<li>{alt}</li>' for alt in alternatives])}
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
            
            with col_graphic:
                # Show eco graphic for eco-friendly purchases
                if last_purchase['type'] in ECO_FRIENDLY_CATEGORIES or st.session_state.show_celebration:
                    st.markdown(get_eco_graphic_svg(animate=st.session_state.show_celebration), unsafe_allow_html=True)
                    if st.session_state.show_celebration:
                        st.session_state.show_celebration = False
        
        st.markdown("---")
        
        # Dashboard section (rest of the code continues as before...)
        st.markdown("### 📈 Your Shopping Dashboard")
        
        # Filter and search controls
        with st.expander("🔍 Filter & Search", expanded=False):
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                start_date = st.date_input("Start Date", value=None, key="start_date")
            with col_f2:
                end_date = st.date_input("End Date", value=None, key="end_date")
            with col_f3:
                search_query = st.text_input("Search", placeholder="Brand or category...", key="search")
            
            selected_categories = st.multiselect(
                "Filter by Categories",
                options=list(PRODUCT_MULTIPLIERS.keys()),
                default=None,
                key="category_filter"
            )
        
        # Filter purchases
        filtered_purchases = st.session_state.purchases.copy()
        
        # Apply filters
        if start_date or end_date:
            filtered_purchases = [
                p for p in filtered_purchases
                if (not start_date or datetime.strptime(p['date'], '%Y-%m-%d').date() >= start_date)
                and (not end_date or datetime.strptime(p['date'], '%Y-%m-%d').date() <= end_date)
            ]
        
        if selected_categories:
            filtered_purchases = [p for p in filtered_purchases if p['type'] in selected_categories]
        
        if search_query:
            search_query = search_query.lower()
            filtered_purchases = [
                p for p in filtered_purchases 
                if search_query in p['brand'].lower() or search_query in p['type'].lower()
            ]
        
        if filtered_purchases:
            total_co2 = sum(p['co2_impact'] for p in filtered_purchases)
            total_spend = sum(p['price'] for p in filtered_purchases)
            avg_co2 = total_co2 / len(filtered_purchases) if filtered_purchases else 0
            
            # Metrics
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            with metric_col1:
                st.metric("Total Spend", f"₹{total_spend:,.0f}")
            with metric_col2:
                st.metric("Total CO₂", f"{total_co2:.1f} kg")
            with metric_col3:
                st.metric("Purchases", len(filtered_purchases))
            with metric_col4:
                st.metric("Avg CO₂/Item", f"{avg_co2:.1f} kg")
            
            st.markdown("---")
            
            # Charts
            df_purchases = pd.DataFrame(filtered_purchases)
            
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                fig_bar = create_co2_by_category_chart(tuple(filtered_purchases), high_contrast)
                if fig_bar:
                    st.plotly_chart(fig_bar, use_container_width=True)
            
            with chart_col2:
                fig_pie = create_spending_by_category_chart(tuple(filtered_purchases), high_contrast)
                if fig_pie:
                    st.plotly_chart(fig_pie, use_container_width=True)
            
            # Line chart
            fig_line = create_cumulative_co2_chart(tuple(filtered_purchases), high_contrast)
            if fig_line:
                st.plotly_chart(fig_line, use_container_width=True)
            
            st.markdown("---")
            
            # Purchase Log
            st.markdown("#### 📋 Purchase History")
            
            export_col1, export_col2, export_col3 = st.columns([2, 1, 1])
            with export_col2:
                csv = df_purchases.to_csv(index=False)
                st.download_button(
                    label="📥 Export CSV",
                    data=csv,
                    file_name=f"shopimpact_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with export_col3:
                json_data = json.dumps(filtered_purchases, indent=2)
                st.download_button(
                    label="📥 Export JSON",
                    data=json_data,
                    file_name=f"shopimpact_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            # Display table
            display_df = df_purchases[['date', 'type', 'brand', 'price', 'co2_impact']].copy()
            display_df.columns = ['Date', 'Product Type', 'Brand', 'Price (₹)', 'CO₂ (kg)']
            display_df = display_df.sort_values('Date', ascending=False).reset_index(drop=True)
            
            st.dataframe(display_df, use_container_width=True, hide_index=False)
            
            # Undo last purchase
            if st.button("↩️ Undo Last Purchase", type="secondary"):
                if st.session_state.purchases:
                    last = st.session_state.purchases[-1]
                    delete_purchase(len(st.session_state.purchases) - 1)
                    st.success(f"✅ Removed: {last['brand']} - {last['type']}")
                    st.rerun()
        else:
            st.info("📝 No purchases logged yet. Start tracking your impact by logging your first purchase above!")
    
    # Sidebar Column
    with col_sidebar:
        st.markdown("### 🏆 Rewards & Tips")
        
        # High Contrast Toggle
        contrast_label = "🌓 High Contrast Mode" if high_contrast else "🌓 High Contrast Mode"
        new_contrast = st.checkbox(contrast_label, value=high_contrast, key="contrast_toggle")
        
        if new_contrast != high_contrast:
            st.session_state.settings['highContrast'] = new_contrast
            save_data({
                'purchases': st.session_state.purchases,
                'user_profile': st.session_state.user_profile,
                'settings': st.session_state.settings
            })
            st.rerun()
        
        st.markdown("---")
        
        # Calculate stats
        monthly_stats = get_monthly_stats(tuple(st.session_state.purchases))
        all_badges = get_all_badges(st.session_state.purchases, monthly_stats)
        
        # Show badges
        st.markdown("#### Your Badges")
        if all_badges:
            for badge in all_badges[:5]:  # Show top 5
                badge_bg = '#1a1a1a' if high_contrast else '#d1fae5'
                badge_border = '#FFFFFF' if high_contrast else '#10b981'
                badge_text = '#FFFFFF' if high_contrast else '#000000'
                
                st.markdown(f"""
                <div class="badge-card" style="background-color: {badge_bg}; border-color: {badge_border}; color: {badge_text};">
                    <span style="font-size: 32px;">{badge['icon']}</span>
                    <p style="margin: 5px 0; font-weight: bold;">{badge['name']}</p>
                    <p style="margin: 0; font-size: 12px; opacity: 0.8;">{badge.get('description', '')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🏅 Earn badges by staying under spending and CO₂ limits!")
        
        st.markdown("---")
        
        # Eco Tip
        tip_bg = '#1a3a5f' if high_contrast else '#dbeafe'
        tip_text = '#FFFFFF' if high_contrast else '#2563eb'
        
        st.markdown(f"""
        <div class="tip-card" style="background-color: {tip_bg};">
            <h4 style="color: {tip_text}; margin-top: 0;">💡 Eco Tip</h4>
            <p style="margin-bottom: 0; color: {tip_text};">{random.choice(TIPS_LIST)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Motivational Quote
        quote_bg = '#3a1a5f' if high_contrast else '#e9d5ff'
        quote_text = '#FFFFFF' if high_contrast else '#a855f7'
        
        st.markdown(f"""
        <div class="quote-card" style="background-color: {quote_bg};">
            <p style="font-style: italic; margin: 0; color: {quote_text};">"{random.choice(MOTIVATIONAL_QUOTES)}"</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Show eco graphic if user has eco purchases
        has_eco = any(p['type'] in ECO_FRIENDLY_CATEGORIES for p in st.session_state.purchases)
        if has_eco:
            st.markdown(get_eco_graphic_svg(animate=False), unsafe_allow_html=True)
            st.markdown("---")
        
        # Reset button with confirmation
        if st.button("🔄 Clear All Data", type="secondary", use_container_width=True):
            st.session_state.show_delete_confirm = True
        
        if st.session_state.get('show_delete_confirm', False):
            st.warning("⚠️ This will delete all purchases!")
            col_conf1, col_conf2 = st.columns(2)
            with col_conf1:
                if st.button("✅ Yes", use_container_width=True):
                    st.session_state.purchases = []
                    save_data({
                        'purchases': [],
                        'user_profile': st.session_state.user_profile,
                        'settings': st.session_state.settings
                    })
                    st.session_state.show_delete_confirm = False
                    st.success("✨ Data cleared!")
                    st.rerun()
            with col_conf2:
                if st.button("❌ No", use_container_width=True):
                    st.session_state.show_delete_confirm = False
                    st.rerun()
        
        # Quick Stats
        if st.session_state.purchases:
            st.markdown("---")
            st.markdown("#### 📈 Quick Stats")
            
            total_items = len(st.session_state.purchases)
            eco_items = sum(1 for p in st.session_state.purchases 
                          if p['type'] in ECO_FRIENDLY_CATEGORIES)
            
            st.write(f"**Total tracked:** {total_items}")
            st.write(f"**Eco purchases:** {eco_items}")
            if total_items > 0:
                eco_percent = (eco_items / total_items) * 100
                st.write(f"**Eco rate:** {eco_percent:.0f}%")
                st.progress(min(eco_percent / 100, 1.0))

# ==================== PROFILE TAB ====================
with tab2:
    st.markdown("### 👤 Your Profile")
    
    profile = st.session_state.user_profile
    
    # Profile display
    col_avatar, col_info = st.columns([1, 4])
    with col_avatar:
        avatar_letter = profile['name'][0].upper() if profile['name'] else '?'
        avatar_bg = '#FFFFFF' if high_contrast else '#16a34a'
        avatar_text = '#000000' if high_contrast else 'white'
        
        st.markdown(f"""
        <div style="width: 80px; height: 80px; border-radius: 50%; 
                    background-color: {avatar_bg}; color: {avatar_text}; 
                    display: flex; align-items: center; justify-content: center;
                    font-size: 36px; font-weight: bold; margin: 10px auto;
                    border: {'2px solid #000000' if high_contrast else 'none'};">
            {avatar_letter}
        </div>
        """, unsafe_allow_html=True)
    
    with col_info:
        name_color = '#FFFFFF' if high_contrast else '#000000'
        st.markdown(f"<h2 style='color: {name_color};'>{profile['name'] if profile['name'] else 'Eco Hero'}</h2>", unsafe_allow_html=True)
        if profile['location']:
            st.write(f"📍 {profile['location']}")
        if profile['age']:
            st.write(f"🎂 Age: {profile['age']}")
        
        days_since = (datetime.now() - datetime.strptime(profile['joinDate'], '%Y-%m-%d')).days
        st.write(f"📅 Member for {days_since} days")
    
    st.markdown("---")
    
    # Edit Profile
    with st.expander("✏️ Edit Profile", expanded=False):
        with st.form("profile_form"):
            name = st.text_input("Name", value=profile['name'], placeholder="Your name")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                age = st.text_input("Age", value=profile['age'], placeholder="Your age")
            with col_p2:
                location = st.text_input("Location", value=profile['location'], placeholder="City, Country")
            
            col_p3, col_p4 = st.columns(2)
            with col_p3:
                monthly_budget = st.number_input(
                    "Monthly Budget (₹)",
                    value=profile['monthlyBudget'],
                    min_value=0,
                    step=1000,
                    help="Your monthly spending budget"
                )
            with col_p4:
                co2_goal = st.number_input(
                    "Monthly CO₂ Goal (kg)",
                    value=profile['co2Goal'],
                    min_value=0,
                    step=10,
                    help="Your target CO₂ limit per month"
                )
            
            if st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True):
                st.session_state.user_profile = {
                    'name': name,
                    'age': age,
                    'location': location,
                    'monthlyBudget': monthly_budget,
                    'co2Goal': co2_goal,
                    'joinDate': profile['joinDate']
                }
                save_data({
                    'purchases': st.session_state.purchases,
                    'user_profile': st.session_state.user_profile,
                    'settings': st.session_state.settings
                })
                st.success("✅ Profile updated successfully! 🎉")
                st.rerun()
    
    # Monthly Stats
    st.markdown("### 📊 This Month's Stats")
    
    monthly_stats = get_monthly_stats(tuple(st.session_state.purchases))
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    with stat_col1:
        st.metric("Spend", f"₹{monthly_stats['totalSpend']:,.0f}")
    with stat_col2:
        st.metric("CO₂", f"{monthly_stats['totalCO2']:.1f} kg")
    with stat_col3:
        st.metric("Purchases", monthly_stats['totalPurchases'])
    with stat_col4:
        st.metric("Eco %", f"{monthly_stats['ecoFriendlyPercent']:.0f}%")
    
    st.markdown("---")
    
    # Goals vs Eco Standards
    st.markdown("### 🎯 Your Goals vs Eco Standards")
    
    # Personal Budget Goal
    if profile['monthlyBudget'] > 0:
        budget_progress = min((monthly_stats['totalSpend'] / profile['monthlyBudget']) * 100, 100)
        remaining_budget = max(profile['monthlyBudget'] - monthly_stats['totalSpend'], 0)
        
        st.write("**💰 Your Budget Goal**")
        col_budget1, col_budget2 = st.columns([3, 1])
        with col_budget1:
            st.caption(f"₹{monthly_stats['totalSpend']:,.0f} / ₹{profile['monthlyBudget']:,}")
            st.progress(min(budget_progress / 100, 1.0))
        with col_budget2:
            if budget_progress < 100:
                st.metric("Left", f"₹{remaining_budget:,.0f}")
            else:
                st.metric("Over", f"₹{monthly_stats['totalSpend'] - profile['monthlyBudget']:,.0f}")
        
        if budget_progress >= 100:
            st.caption("⚠️ Budget exceeded!")
        elif budget_progress >= 80:
            st.caption("⚠️ Approaching budget limit")
        else:
            st.caption(f"✅ {100 - budget_progress:.0f}% remaining")
        st.markdown("")
    
    # Personal CO2 Goal
    if profile['co2Goal'] > 0:
        co2_progress = min((monthly_stats['totalCO2'] / profile['co2Goal']) * 100, 100)
        remaining_co2 = max(profile['co2Goal'] - monthly_stats['totalCO2'], 0)
        
        st.write("**📉 Your CO₂ Goal**")
        col_co2_1, col_co2_2 = st.columns([3, 1])
        with col_co2_1:
            st.caption(f"{monthly_stats['totalCO2']:.1f} / {profile['co2Goal']} kg")
            st.progress(min(co2_progress / 100, 1.0))
        with col_co2_2:
            if co2_progress < 100:
                st.metric("Left", f"{remaining_co2:.1f} kg")
            else:
                st.metric("Over", f"{monthly_stats['totalCO2'] - profile['co2Goal']:.1f} kg")
        
        if co2_progress >= 100:
            st.caption("⚠️ CO₂ goal exceeded!")
        elif co2_progress >= 80:
            st.caption("⚠️ Approaching CO₂ limit")
        else:
            st.caption(f"✅ {100 - co2_progress:.0f}% remaining")
        st.markdown("")
    
    # Eco Standard - CO2
    eco_co2_progress = min((monthly_stats['totalCO2'] / ECO_STANDARDS['monthlyCO2']) * 100, 100)
    st.write("**🌍 Eco CO₂ Standard**")
    st.caption(f"{monthly_stats['totalCO2']:.1f} / {ECO_STANDARDS['monthlyCO2']} kg")
    st.progress(min(eco_co2_progress / 100, 1.0))
    if eco_co2_progress < 100:
        st.caption(f"🎉 {100 - eco_co2_progress:.0f}% below eco standard!")
    else:
        st.caption(f"⚠️ {eco_co2_progress - 100:.0f}% above eco limit")
    st.markdown("")
    
    # Eco Standard - Budget
    eco_budget_progress = min((monthly_stats['totalSpend'] / ECO_STANDARDS['monthlyBudget']) * 100, 100)
    st.write("**💚 Eco Budget Standard**")
    st.caption(f"₹{monthly_stats['totalSpend']:,.0f} / ₹{ECO_STANDARDS['monthlyBudget']:,}")
    st.progress(min(eco_budget_progress / 100, 1.0))
    if eco_budget_progress < 100:
        st.caption(f"✅ {100 - eco_budget_progress:.0f}% under eco budget")
    else:
        st.caption("⚠️ Consider reducing consumption")
    st.markdown("")
    
    # Eco-Friendly Percentage
    eco_percent_progress = min((monthly_stats['ecoFriendlyPercent'] / ECO_STANDARDS['ecoFriendlyPercentage']) * 100, 100)
    st.write("**♻️ Eco-Friendly Purchases**")
    st.caption(f"{monthly_stats['ecoFriendlyPercent']:.0f}% / {ECO_STANDARDS['ecoFriendlyPercentage']}%")
    st.progress(min(eco_percent_progress / 100, 1.0))
    if monthly_stats['ecoFriendlyPercent'] >= ECO_STANDARDS['ecoFriendlyPercentage']:
        st.caption("🎉 Shopping sustainably!")
    else:
        st.caption("💡 Try more second-hand/local items")
    
    st.markdown("---")
    
    # Badges Section
    st.markdown("### 🏆 Your Badges")
    
    all_badges = get_all_badges(st.session_state.purchases, monthly_stats)
    
    if all_badges:
        badge_cols = st.columns(min(len(all_badges), 3))
        for idx, badge in enumerate(all_badges):
            with badge_cols[idx % len(badge_cols)]:
                badge_bg = '#1a5f3a' if high_contrast else '#d1fae5'
                badge_border = '#FFFFFF' if high_contrast else '#10b981'
                badge_text = '#FFFFFF' if high_contrast else '#000000'
                
                limit_text = badge.get('description', '')
                if 'limit' in badge:
                    limit_text = f"CO₂ < {badge['limit']} kg" if badge['type'] == 'co2' else f"< ₹{badge['limit']:,}"
                
                st.markdown(f"""
                <div class="badge-card" style="background-color: {badge_bg}; border-color: {badge_border}; color: {badge_text};">
                    <span style="font-size: 40px;">{badge['icon']}</span>
                    <p style="margin: 8px 0; font-weight: bold; font-size: 16px;">{badge['name']}</p>
                    <p style="margin: 0; font-size: 12px; opacity: 0.8;">{limit_text}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("🏅 No badges this month. Stay under limits to earn badges!")
    
    st.markdown("---")
    
    # Lifetime Achievements
    st.markdown("### 🌟 Lifetime Achievements")
    
    total_purchases = len(st.session_state.purchases)
    total_spent = sum(p['price'] for p in st.session_state.purchases)
    total_eco = sum(1 for p in st.session_state.purchases 
                   if p['type'] in ECO_FRIENDLY_CATEGORIES)
    
    achieve_col1, achieve_col2, achieve_col3, achieve_col4 = st.columns(4)
    
    stat_card_bg = '#1a1a1a' if high_contrast else 'white'
    stat_card_border = '#FFFFFF' if high_contrast else '#e5e7eb'
    stat_card_text = '#FFFFFF' if high_contrast else '#000000'
    
    with achieve_col1:
        st.markdown(f"""
        <div class="stat-card" style="background-color: {stat_card_bg}; border: 1px solid {stat_card_border}; color: {stat_card_text};">
            <p style="font-size: 32px; margin: 0;">🛍️</p>
            <p style="font-size: 24px; margin: 5px 0; font-weight: bold;">{total_purchases}</p>
            <p style="font-size: 12px; margin: 0; opacity: 0.7;">Purchases</p>
        </div>
        """, unsafe_allow_html=True)
    
    with achieve_col2:
        st.markdown(f"""
        <div class="stat-card" style="background-color: {stat_card_bg}; border: 1px solid {stat_card_border}; color: {stat_card_text};">
            <p style="font-size: 32px; margin: 0;">💰</p>
            <p style="font-size: 24px; margin: 5px 0; font-weight: bold;">₹{total_spent:,.0f}</p>
            <p style="font-size: 12px; margin: 0; opacity: 0.7;">Total Spent</p>
        </div>
        """, unsafe_allow_html=True)
    
    with achieve_col3:
        st.markdown(f"""
        <div class="stat-card" style="background-color: {stat_card_bg}; border: 1px solid {stat_card_border}; color: {stat_card_text};">
            <p style="font-size: 32px; margin: 0;">🌱</p>
            <p style="font-size: 24px; margin: 5px 0; font-weight: bold;">{total_eco}</p>
            <p style="font-size: 12px; margin: 0; opacity: 0.7;">Eco Items</p>
        </div>
        """, unsafe_allow_html=True)
    
    with achieve_col4:
        st.markdown(f"""
        <div class="stat-card" style="background-color: {stat_card_bg}; border: 1px solid {stat_card_border}; color: {stat_card_text};">
            <p style="font-size: 32px; margin: 0;">🏆</p>
            <p style="font-size: 24px; margin: 5px 0; font-weight: bold;">{len(all_badges)}</p>
            <p style="font-size: 12px; margin: 0; opacity: 0.7;">Badges</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== ANALYTICS TAB ====================
with tab3:
    st.markdown("### 📈 Advanced Analytics")
    
    if st.session_state.purchases:
        df_all = pd.DataFrame(st.session_state.purchases)
        
        # Time range selector
        time_range = st.selectbox(
            "Time Range",
            ["All Time", "Last 7 Days", "Last 30 Days", "Last 90 Days", "This Month", "Last Month"],
            key="time_range"
        )
        
        # Filter by time range
        if time_range == "Last 7 Days":
            cutoff_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            df_filtered = df_all[df_all['date'] >= cutoff_date]
        elif time_range == "Last 30 Days":
            cutoff_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            df_filtered = df_all[df_all['date'] >= cutoff_date]
        elif time_range == "Last 90 Days":
            cutoff_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
            df_filtered = df_all[df_all['date'] >= cutoff_date]
        elif time_range == "This Month":
            current_month = datetime.now().month
            current_year = datetime.now().year
            df_filtered = df_all[
                (pd.to_datetime(df_all['date']).dt.month == current_month) &
                (pd.to_datetime(df_all['date']).dt.year == current_year)
            ]
        elif time_range == "Last Month":
            last_month_date = datetime.now() - timedelta(days=30)
            last_month = last_month_date.month
            last_year = last_month_date.year
            df_filtered = df_all[
                (pd.to_datetime(df_all['date']).dt.month == last_month) &
                (pd.to_datetime(df_all['date']).dt.year == last_year)
            ]
        else:
            df_filtered = df_all
        
        if not df_filtered.empty:
            # Key metrics
            st.markdown("#### Key Metrics")
            kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
            
            with kpi_col1:
                st.metric("Total Purchases", len(df_filtered))
            with kpi_col2:
                st.metric("Total Spent", f"₹{df_filtered['price'].sum():,.0f}")
            with kpi_col3:
                st.metric("Total CO₂", f"{df_filtered['co2_impact'].sum():.1f} kg")
            with kpi_col4:
                st.metric("Avg per Purchase", f"₹{df_filtered['price'].mean():,.0f}")
            with kpi_col5:
                eco_count = len(df_filtered[df_filtered['type'].isin(ECO_FRIENDLY_CATEGORIES)])
                eco_pct = (eco_count / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
                st.metric("Eco %", f"{eco_pct:.0f}%")
            
            st.markdown("---")
            
            # Charts
            chart_row1_col1, chart_row1_col2 = st.columns(2)
            
            # Spending over time
            with chart_row1_col1:
                st.markdown("#### Spending Over Time")
                df_time = df_filtered.groupby('date')['price'].sum().reset_index()
                df_time = df_time.sort_values('date')
                
                area_color = '#FFFFFF' if high_contrast else '#16a34a'
                bg_color = '#000000' if high_contrast else 'rgba(0,0,0,0)'
                text_color = '#FFFFFF' if high_contrast else '#374151'
                
                fig_spending = px.area(
                    df_time,
                    x='date',
                    y='price',
                    labels={'price': 'Spending (₹)', 'date': 'Date'},
                    color_discrete_sequence=[area_color]
                )
                fig_spending.update_layout(
                    height=350,
                    margin=dict(l=20, r=20, t=20, b=40),
                    plot_bgcolor=bg_color,
                    paper_bgcolor=bg_color,
                    font=dict(color=text_color)
                )
                st.plotly_chart(fig_spending, use_container_width=True)
            
            # Top categories
            with chart_row1_col2:
                st.markdown("#### Top Categories by Spend")
                category_spend = df_filtered.groupby('type')['price'].sum().reset_index()
                category_spend = category_spend.sort_values('price', ascending=True).tail(10)
                
                color_scale = 'Greys' if high_contrast else 'Greens'
                bg_color = '#000000' if high_contrast else 'rgba(0,0,0,0)'
                text_color = '#FFFFFF' if high_contrast else '#374151'
                
                fig_top_cat = px.bar(
                    category_spend,
                    x='price',
                    y='type',
                    orientation='h',
                    labels={'price': 'Total Spent (₹)', 'type': 'Category'},
                    color='price',
                    color_continuous_scale=color_scale
                )
                fig_top_cat.update_layout(
                    height=350,
                    margin=dict(l=20, r=20, t=20, b=40),
                    showlegend=False,
                    plot_bgcolor=bg_color,
                    paper_bgcolor=bg_color,
                    font=dict(color=text_color)
                )
                st.plotly_chart(fig_top_cat, use_container_width=True)
            
            st.markdown("---")
            
            # Detailed statistics table
            st.markdown("#### Category Statistics")
            category_stats = df_filtered.groupby('type').agg({
                'price': ['sum', 'mean', 'count'],
                'co2_impact': ['sum', 'mean']
            }).round(2)
            category_stats.columns = ['Total Spent (₹)', 'Avg Spent (₹)', 'Count', 'Total CO₂ (kg)', 'Avg CO₂ (kg)']
            category_stats = category_stats.sort_values('Total Spent (₹)', ascending=False)
            
            st.dataframe(category_stats, use_container_width=True)
            
            # Insights
            st.markdown("---")
            st.markdown("#### 💡 Insights")
            
            insights_col1, insights_col2 = st.columns(2)
            
            with insights_col1:
                # Highest impact category
                highest_co2_cat = df_filtered.groupby('type')['co2_impact'].sum().idxmax()
                highest_co2_val = df_filtered.groupby('type')['co2_impact'].sum().max()
                
                insight_bg = '#5f1a1a' if high_contrast else '#fee2e2'
                insight_border = '#FFFFFF' if high_contrast else '#dc2626'
                insight_text = '#FFFFFF' if high_contrast else '#dc2626'
                
                st.markdown(f"""
                <div class="tip-card" style="background-color: {insight_bg}; border-color: {insight_border};">
                    <h4 style="color: {insight_text}; margin-top: 0;">⚠️ Highest Impact Category</h4>
                    <p style="margin: 0; color: {insight_text};"><strong>{highest_co2_cat}</strong></p>
                    <p style="margin: 5px 0 0 0; color: {insight_text};">{highest_co2_val:.1f} kg CO₂</p>
                </div>
                """, unsafe_allow_html=True)
            
            with insights_col2:
                # Most frequent category
                most_frequent = df_filtered['type'].mode()[0] if not df_filtered.empty else "N/A"
                frequency = len(df_filtered[df_filtered['type'] == most_frequent]) if most_frequent != "N/A" else 0
                
                freq_bg = '#1a3a5f' if high_contrast else '#dbeafe'
                freq_border = '#FFFFFF' if high_contrast else '#3b82f6'
                freq_text = '#FFFFFF' if high_contrast else '#2563eb'
                
                st.markdown(f"""
                <div class="tip-card" style="background-color: {freq_bg}; border-color: {freq_border};">
                    <h4 style="color: {freq_text}; margin-top: 0;">🔄 Most Frequent</h4>
                    <p style="margin: 0; color: {freq_text};"><strong>{most_frequent}</strong></p>
                    <p style="margin: 5px 0 0 0; color: {freq_text};">{frequency} purchases</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📊 No data available for selected time range.")
    else:
        st.info("📊 Start logging purchases to see analytics!")

# ==================== FOOTER ====================
st.markdown("---")
footer_color = '#CCCCCC' if high_contrast else '#9ca3af'
st.markdown(
    f"<p style='text-align: center; color: {footer_color}; font-size: 14px;'>ShopImpact 🍃 | Making conscious shopping easy and fun!</p>",
    unsafe_allow_html=True
)
