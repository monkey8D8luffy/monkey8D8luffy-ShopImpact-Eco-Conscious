"""
ShopImpact - Streamlit Version
A colorful, interactive, and friendly web app to help users become mindful, eco-conscious shoppers.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random

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
    {'name': 'Frugal Shopper', 'icon': '💰', 'limit': 5000, 'type': 'spend'},
    {'name': 'Budget Conscious', 'icon': '🎯', 'limit': 10000, 'type': 'spend'},
    {'name': 'Mindful Spender', 'icon': '🌟', 'limit': 15000, 'type': 'spend'},
    {'name': 'Carbon Neutral Goal', 'icon': '🌱', 'limit': 50, 'type': 'co2'},
    {'name': 'Eco Warrior', 'icon': '🦸', 'limit': 30, 'type': 'co2'},
]

# ==================== SESSION STATE INITIALIZATION ====================
if 'purchases' not in st.session_state:
    st.session_state.purchases = []

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'name': '',
        'age': '',
        'location': '',
        'monthlyBudget': 15000,
        'co2Goal': 50,
        'joinDate': datetime.now().strftime('%Y-%m-%d')
    }

if 'show_success' not in st.session_state:
    st.session_state.show_success = False

if 'success_message' not in st.session_state:
    st.session_state.success_message = ''

# ==================== HELPER FUNCTIONS ====================
def calculate_co2(price, product_type):
    """Calculate CO2 impact based on price and product type"""
    multiplier = PRODUCT_MULTIPLIERS.get(product_type, 1.0)
    return price * multiplier

def get_monthly_stats(purchases):
    """Calculate statistics for current month"""
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
        if p['type'] in ['Second-Hand Item', 'Local Groceries', 'Books (Used)']
    )
    eco_friendly_percent = (eco_friendly_count / len(monthly_purchases)) * 100 if monthly_purchases else 0
    
    return {
        'totalSpend': total_spend,
        'totalCO2': total_co2,
        'ecoFriendlyPercent': eco_friendly_percent,
        'totalPurchases': len(monthly_purchases)
    }

def get_earned_badges(stats):
    """Get badges earned based on current stats"""
    earned = []
    for badge in SPENDING_BADGES:
        if badge['type'] == 'co2':
            if stats['totalCO2'] <= badge['limit'] and stats['totalCO2'] > 0:
                earned.append(badge)
        else:
            if stats['totalSpend'] <= badge['limit'] and stats['totalSpend'] > 0:
                earned.append(badge)
    return earned

def add_purchase(product_type, brand, price):
    """Add a new purchase to the session state"""
    co2_impact = calculate_co2(price, product_type)
    purchase = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'type': product_type,
        'brand': brand,
        'price': float(price),
        'co2_impact': float(co2_impact)
    }
    st.session_state.purchases.append(purchase)
    
    # Set success message
    if product_type in ['Second-Hand Item', 'Local Groceries', 'Books (Used)']:
        st.session_state.success_message = f"🌟 Eco-friendly choice! You're making a difference!"
        st.balloons()
    else:
        st.session_state.success_message = f"✅ Logged! Your {product_type} added {co2_impact:.1f} kg of CO₂."
    st.session_state.show_success = True

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
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
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("<h1 style='text-align: center; color: #16a34a;'>🍃 ShopImpact 🍃</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280; font-size: 18px;'>Your friendly guide to conscious shopping.</p>", unsafe_allow_html=True)

if st.session_state.user_profile['name']:
    st.markdown(f"<p style='text-align: center; color: #16a34a; font-size: 16px;'>Welcome back, {st.session_state.user_profile['name']}! 🌟</p>", unsafe_allow_html=True)

st.markdown("---")

# ==================== NAVIGATION TABS ====================
tab1, tab2 = st.tabs(["📊 Dashboard", "👤 Profile"])

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
                    key="product_type"
                )
            
            with col2:
                brands_list = POPULAR_BRANDS.get(product_type, ['Custom / Other'])
                selected_brand = st.selectbox("Brand", options=brands_list, key="brand")
            
            if selected_brand == 'Custom / Other':
                custom_brand = st.text_input("Enter Custom Brand Name", placeholder="e.g., Nike, Apple, Local Farm...")
                final_brand = custom_brand if custom_brand else "Custom"
            else:
                final_brand = selected_brand
            
            price = st.number_input("Price (₹)", min_value=0, step=1, value=0, key="price")
            
            # Show estimated CO2
            if price > 0:
                estimated_co2 = calculate_co2(price, product_type)
                st.info(f"**Estimated CO₂ Impact:** {estimated_co2:.1f} kg")
            
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
        
        # Show alternatives for last purchase
        if st.session_state.purchases:
            last_purchase = st.session_state.purchases[-1]
            alternatives = ETHICAL_ALTERNATIVES.get(last_purchase['type'], [])
            if alternatives:
                is_eco = last_purchase['type'] in ['Second-Hand Item', 'Local Groceries', 'Books (Used)']
                
                if is_eco:
                    st.markdown(f"""
                    <div style="background-color: #d1fae5; padding: 15px; border-radius: 10px; 
                                border-left: 4px solid #10b981; margin: 10px 0;">
                        <h4 style="color: #16a34a; margin-top: 0;">🎉 Amazing Choice!</h4>
                        <ul style="margin-bottom: 0;">
                            {''.join([f'<li>{alt}</li>' for alt in alternatives])}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="tip-card">
                        <h4 style="color: #2563eb; margin-top: 0;">✨ Greener choices for {last_purchase['type']}:</h4>
                        <ul style="margin-bottom: 0;">
                            {''.join([f'<li>{alt}</li>' for alt in alternatives])}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Dashboard
        st.markdown("### 📈 Your Shopping Dashboard")
        
        # Filter controls in expander
        with st.expander("🔍 Filter by Date Range"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                start_date = st.date_input("Start Date", value=None, key="start_date")
            with col_f2:
                end_date = st.date_input("End Date", value=None, key="end_date")
        
        # Filter purchases
        filtered_purchases = st.session_state.purchases.copy()
        if start_date or end_date:
            filtered_purchases = [
                p for p in filtered_purchases
                if (not start_date or datetime.strptime(p['date'], '%Y-%m-%d').date() >= start_date)
                and (not end_date or datetime.strptime(p['date'], '%Y-%m-%d').date() <= end_date)
            ]
        
        if filtered_purchases:
            total_co2 = sum(p['co2_impact'] for p in filtered_purchases)
            total_spend = sum(p['price'] for p in filtered_purchases)
            
            # Metrics
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                st.metric("Total Spend", f"₹{total_spend:,.0f}")
            with metric_col2:
                st.metric("Total CO₂ Impact", f"{total_co2:.1f} kg")
            with metric_col3:
                st.metric("Purchases", len(filtered_purchases))
            
            st.markdown("---")
            
            # Charts
            df_purchases = pd.DataFrame(filtered_purchases)
            
            # Bar chart
            st.markdown("#### CO₂ Impact by Category")
            category_data = df_purchases.groupby('type')['co2_impact'].sum().reset_index()
            category_data.columns = ['Category', 'CO2 (kg)']
            
            fig_bar = px.bar(
                category_data,
                x='Category',
                y='CO2 (kg)',
                color='CO2 (kg)',
                color_continuous_scale='Greens'
            )
            fig_bar.update_layout(
                showlegend=False,
                xaxis_tickangle=-45,
                height=400,
                margin=dict(l=20, r=20, t=30, b=100)
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Line chart
            st.markdown("#### Cumulative CO₂ Over Time")
            df_sorted = df_purchases.sort_values('date')
            df_sorted['cumulative_co2'] = df_sorted['co2_impact'].cumsum()
            
            fig_line = px.line(
                df_sorted,
                x='date',
                y='cumulative_co2',
                markers=True,
                labels={'cumulative_co2': 'Cumulative CO₂ (kg)', 'date': 'Date'}
            )
            fig_line.update_traces(line_color='#16a34a', line_width=3)
            fig_line.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=40))
            st.plotly_chart(fig_line, use_container_width=True)
            
            st.markdown("---")
            
            # Purchase Log
            st.markdown("#### 📋 Purchase History")
            
            export_col1, export_col2 = st.columns([3, 1])
            with export_col2:
                csv = df_purchases.to_csv(index=False)
                st.download_button(
                    label="📥 Export CSV",
                    data=csv,
                    file_name=f"shopimpact_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            # Display table
            display_df = df_purchases[['date', 'type', 'brand', 'price', 'co2_impact']].copy()
            display_df.columns = ['Date', 'Product Type', 'Brand', 'Price (₹)', 'CO₂ (kg)']
            display_df = display_df.sort_values('Date', ascending=False)
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("📝 No purchases logged yet. Start tracking your impact by logging your first purchase above!")
    
    # Sidebar Column
    with col_sidebar:
        st.markdown("### 🏆 Rewards & Tips")
        
        # Calculate monthly stats
        monthly_stats = get_monthly_stats(st.session_state.purchases)
        earned_badges = get_earned_badges(monthly_stats)
        
        # Show badges
        st.markdown("#### Your Badges")
        if earned_badges:
            for badge in earned_badges:
                st.markdown(f"""
                <div class="badge-card">
                    <span style="font-size: 32px;">{badge['icon']}</span>
                    <p style="margin: 5px 0; font-weight: bold;">{badge['name']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🏅 Earn badges by staying under spending and CO₂ limits!")
        
        st.markdown("---")
        
        # Eco Tip
        st.markdown(f"""
        <div class="tip-card">
            <h4 style="color: #2563eb; margin-top: 0;">💡 Eco Tip</h4>
            <p style="margin-bottom: 0;">{random.choice(TIPS_LIST)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Motivational Quote
        st.markdown(f"""
        <div class="quote-card">
            <p style="font-style: italic; margin: 0;">"{random.choice(MOTIVATIONAL_QUOTES)}"</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Reset button
        if st.button("🔄 Start New Month", type="secondary", use_container_width=True):
            if st.session_state.purchases:
                st.session_state.purchases = []
                st.success("✨ Fresh start! Ready for conscious shopping.")
                st.rerun()
        
        # Fun Stats
        if st.session_state.purchases:
            st.markdown("---")
            st.markdown("#### 📈 Quick Stats")
            
            total_items = len(st.session_state.purchases)
            eco_items = sum(1 for p in st.session_state.purchases 
                          if p['type'] in ['Second-Hand Item', 'Local Groceries', 'Books (Used)'])
            
            st.write(f"**Total tracked:** {total_items}")
            st.write(f"**Eco purchases:** {eco_items}")
            if total_items > 0:
                eco_percent = (eco_items / total_items) * 100
                st.write(f"**Eco rate:** {eco_percent:.0f}%")

# ==================== PROFILE TAB ====================
with tab2:
    st.markdown("### 👤 Your Profile")
    
    profile = st.session_state.user_profile
    
    # Profile display
    col_avatar, col_info = st.columns([1, 4])
    with col_avatar:
        avatar_letter = profile['name'][0].upper() if profile['name'] else '?'
        st.markdown(f"""
        <div style="width: 80px; height: 80px; border-radius: 50%; 
                    background-color: #16a34a; color: white; 
                    display: flex; align-items: center; justify-content: center;
                    font-size: 36px; font-weight: bold; margin: 10px auto;">
            {avatar_letter}
        </div>
        """, unsafe_allow_html=True)
    
    with col_info:
        st.markdown(f"## {profile['name'] if profile['name'] else 'Eco Hero'}")
        if profile['location']:
            st.write(f"📍 {profile['location']}")
        if profile['age']:
            st.write(f"🎂 Age: {profile['age']}")
        
        days_since = (datetime.now() - datetime.strptime(profile['joinDate'], '%Y-%m-%d')).days
        st.write(f"📅 Member for {days_since} days")
    
    st.markdown("---")
    
    # Edit Profile
    with st.expander("✏️ Edit Profile"):
        with st.form("profile_form"):
            name = st.text_input("Name", value=profile['name'])
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                age = st.text_input("Age", value=profile['age'])
            with col_p2:
                location = st.text_input("Location", value=profile['location'])
            
            col_p3, col_p4 = st.columns(2)
            with col_p3:
                monthly_budget = st.number_input("Monthly Budget (₹)", value=profile['monthlyBudget'], min_value=0, step=1000)
            with col_p4:
                co2_goal = st.number_input("Monthly CO₂ Goal (kg)", value=profile['co2Goal'], min_value=0, step=10)
            
            if st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True):
                st.session_state.user_profile = {
                    'name': name,
                    'age': age,
                    'location': location,
                    'monthlyBudget': monthly_budget,
                    'co2Goal': co2_goal,
                    'joinDate': profile['joinDate']
                }
                st.success("✅ Profile updated successfully! 🎉")
                st.rerun()
    
    # Monthly Stats
    st.markdown("### 📊 This Month's Stats")
    
    monthly_stats = get_monthly_stats(st.session_state.purchases)
    
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
        st.write("**💰 Your Budget Goal**")
        st.caption(f"₹{monthly_stats['totalSpend']:,.0f} / ₹{profile['monthlyBudget']:,}")
        st.progress(budget_progress / 100)
        if budget_progress < 100:
            st.caption(f"✅ {100 - budget_progress:.0f}% remaining")
        else:
            st.caption("⚠️ Budget exceeded!")
        st.markdown("")
    
    # Personal CO2 Goal
    if profile['co2Goal'] > 0:
        co2_progress = min((monthly_stats['totalCO2'] / profile['co2Goal']) * 100, 100)
        st.write("**📉 Your CO₂ Goal**")
        st.caption(f"{monthly_stats['totalCO2']:.1f} / {profile['co2Goal']} kg")
        st.progress(co2_progress / 100)
        if co2_progress < 100:
            st.caption(f"✅ {100 - co2_progress:.0f}% remaining")
        else:
            st.caption("⚠️ CO₂ goal exceeded!")
        st.markdown("")
    
    # Eco Standard - CO2
    eco_co2_progress = min((monthly_stats['totalCO2'] / ECO_STANDARDS['monthlyCO2']) * 100, 100)
    st.write("**🌍 Eco CO₂ Standard**")
    st.caption(f"{monthly_stats['totalCO2']:.1f} / {ECO_STANDARDS['monthlyCO2']} kg")
    st.progress(eco_co2_progress / 100)
    if eco_co2_progress < 100:
        st.caption(f"🎉 {100 - eco_co2_progress:.0f}% below eco standard!")
    else:
        st.caption(f"⚠️ {eco_co2_progress - 100:.0f}% above eco limit")
    st.markdown("")
    
    # Eco Standard - Budget
    eco_budget_progress = min((monthly_stats['totalSpend'] / ECO_STANDARDS['monthlyBudget']) * 100, 100)
    st.write("**💚 Eco Budget Standard**")
    st.caption(f"₹{monthly_stats['totalSpend']:,.0f} / ₹{ECO_STANDARDS['monthlyBudget']:,}")
    st.progress(eco_budget_progress / 100)
    if eco_budget_progress < 100:
        st.caption(f"✅ {100 - eco_budget_progress:.0f}% under eco budget")
    else:
        st.caption("⚠️ Consider reducing consumption")
    st.markdown("")
    
    # Eco-Friendly Percentage
    eco_percent_progress = min((monthly_stats['ecoFriendlyPercent'] / ECO_STANDARDS['ecoFriendlyPercentage']) * 100, 100)
    st.write("**♻️ Eco-Friendly Purchases**")
    st.caption(f"{monthly_stats['ecoFriendlyPercent']:.0f}% / {ECO_STANDARDS['ecoFriendlyPercentage']}%")
    st.progress(eco_percent_progress / 100)
    if monthly_stats['ecoFriendlyPercent'] >= ECO_STANDARDS['ecoFriendlyPercentage']:
        st.caption("🎉 Shopping sustainably!")
    else:
        st.caption("💡 Try more second-hand/local items")
    
    st.markdown("---")
    
    # Badges Section
    st.markdown("### 🏆 Your Badges")
    
    earned_badges = get_earned_badges(monthly_stats)
    
    if earned_badges:
        badge_cols = st.columns(2)
        for idx, badge in enumerate(earned_badges):
            with badge_cols[idx % 2]:
                limit_text = f"CO₂ < {badge['limit']} kg" if badge['type'] == 'co2' else f"< ₹{badge['limit']:,}"
                st.markdown(f"""
                <div class="badge-card">
                    <span style="font-size: 40px;">{badge['icon']}</span>
                    <p style="margin: 8px 0; font-weight: bold; font-size: 16px;">{badge['name']}</p>
                    <p style="margin: 0; font-size: 12px; color: #666;">{limit_text}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("🏅 No badges this month. Stay under limits to earn badges!")
    
    # Available badges
    st.markdown("#### Available Badges")
    badge_grid_cols = st.columns(5)
    for idx, badge in enumerate(SPENDING_BADGES):
        is_earned = any(b['name'] == badge['name'] for b in earned_badges)
        with badge_grid_cols[idx % 5]:
            opacity = "1.0" if is_earned else "0.4"
            limit_text = f"<{badge['limit']}kg" if badge['type'] == 'co2' else f"<₹{badge['limit']/1000:.0f}k"
            
            st.markdown(f"""
            <div style="background-color: {'#d1fae5' if is_earned else '#f3f4f6'}; 
                        padding: 10px; border-radius: 8px; text-align: center;
                        opacity: {opacity}; border: 1px solid {'#10b981' if is_earned else '#d1d5db'};">
                <span style="font-size: 24px;">{badge['icon']}</span>
                <p style="margin: 5px 0; font-size: 10px;">{limit_text}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Lifetime Achievements
    st.markdown("### 🌟 Lifetime Achievements")
    
    total_purchases = len(st.session_state.purchases)
    total_spent = sum(p['price'] for p in st.session_state.purchases)
    total_eco = sum(1 for p in st.session_state.purchases 
                   if p['type'] in ['Second-Hand Item', 'Local Groceries', 'Books (Used)'])
    
    achieve_col1, achieve_col2, achieve_col3, achieve_col4 = st.columns(4)
    
    with achieve_col1:
        st.markdown("""
        <div style="text-align: center; padding: 10px; background-color: white; 
                    border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <p style="font-size: 32px; margin: 0;">🛍️</p>
            <p style="font-size: 20px; margin: 5px 0; font-weight: bold;">""" + str(total_purchases) + """</p>
            <p style="font-size: 11px; margin: 0; color: #666;">Purchases</p>
        </div>
        """, unsafe_allow_html=True)
    
    with achieve_col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background-color: white; 
                    border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <p style="font-size: 32px; margin: 0;">💰</p>
            <p style="font-size: 20px; margin: 5px 0; font-weight: bold;">₹{total_spent:,.0f}</p>
            <p style="font-size: 11px; margin: 0; color: #666;">Total Spent</p>
        </div>
        """, unsafe_allow_html=True)
    
    with achieve_col3:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background-color: white; 
                    border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <p style="font-size: 32px; margin: 0;">🌱</p>
            <p style="font-size: 20px; margin: 5px 0; font-weight: bold;">{total_eco}</p>
            <p style="font-size: 11px; margin: 0; color: #666;">Eco Items</p>
        </div>
        """, unsafe_allow_html=True)
    
    with achieve_col4:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background-color: white; 
                    border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <p style="font-size: 32px; margin: 0;">🏆</p>
            <p style="font-size: 20px; margin: 5px 0; font-weight: bold;">{len(earned_badges)}</p>
            <p style="font-size: 11px; margin: 0; color: #666;">Badges</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #9ca3af; font-size: 14px;'>ShopImpact 🍃 | Making conscious shopping easy and fun!</p>",
    unsafe_allow_html=True
)
