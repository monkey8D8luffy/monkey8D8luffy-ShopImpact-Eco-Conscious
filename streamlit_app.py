"""
ShopImpact - Streamlit Version
A colorful, interactive, and friendly web app to help users become mindful, eco-conscious shoppers.
"" 


# Page configuration
st.set_page_config(
    page_title="ShopImpact 🍃",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f0fdf4 0%, #dbeafe 50%, #d1fae5 100%);
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .badge {
        display: inline-block;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 5px;
        font-weight: bold;
        border: 2px solid;
    }
    .eco-tip {
        background-color: #dbeafe;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
        margin: 10px 0;
    }
    .success-message {
        background-color: #d1fae5;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #10b981;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Product multipliers for CO2 calculation
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

# Ethical alternatives suggestions
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

# Popular brands by category
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

# Eco tips
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

# Motivational quotes
MOTIVATIONAL_QUOTES = [
    "Every purchase is a vote for the kind of world you want to live in.",
    "Small changes, big impact! 🌍",
    "The future depends on what you do today.",
    "Be the change you wish to see in the world.",
    "Conscious choices create a better tomorrow.",
    "Your actions inspire others to be better too.",
    "Sustainability is not a trend, it's a responsibility.",
]

# Eco-friendly standards (benchmarks)
ECO_STANDARDS = {
    'monthlyCO2': 100,  # kg - eco-friendly monthly CO2 limit
    'monthlyBudget': 15000,  # ₹ - suggested eco-conscious budget
    'ecoFriendlyPercentage': 30,  # % of purchases should be eco-friendly
}

# Spending-based badges with limits
SPENDING_BADGES = [
    {'name': 'Frugal Shopper', 'icon': '💰', 'limit': 5000, 'type': 'spend'},
    {'name': 'Budget Conscious', 'icon': '🎯', 'limit': 10000, 'type': 'spend'},
    {'name': 'Mindful Spender', 'icon': '🌟', 'limit': 15000, 'type': 'spend'},
    {'name': 'Carbon Neutral Goal', 'icon': '🌱', 'limit': 50, 'type': 'co2'},
    {'name': 'Eco Warrior', 'icon': '🦸', 'limit': 30, 'type': 'co2'},
]

# Initialize session state
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

if 'show_alternatives' not in st.session_state:
    st.session_state.show_alternatives = False

if 'last_product_type' not in st.session_state:
    st.session_state.last_product_type = ''

# Helper functions
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
        else:  # spend
            if stats['totalSpend'] <= badge['limit'] and stats['totalSpend'] > 0:
                earned.append(badge)
    return earned

def get_progress_color(progress):
    """Get color based on progress percentage"""
    if progress <= 50:
        return '#10b981'  # green
    elif progress <= 80:
        return '#eab308'  # yellow
    else:
        return '#ef4444'  # red

# Main App Header
st.markdown("<h1 style='text-align: center; color: #16a34a;'>🍃 ShopImpact 🍃</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280; font-size: 18px;'>Your friendly guide to conscious shopping.</p>", unsafe_allow_html=True)

# Welcome message
if st.session_state.user_profile['name']:
    st.markdown(f"<p style='text-align: center; color: #16a34a; font-size: 16px;'>Welcome back, {st.session_state.user_profile['name']}! 🌟</p>", unsafe_allow_html=True)

st.markdown("---")

# Navigation tabs
tab1, tab2 = st.tabs(["📊 Dashboard", "👤 Profile"])

# ========== DASHBOARD TAB ==========
with tab1:
    col_main, col_sidebar = st.columns([2, 1])
    
    # Main Content Column
    with col_main:
        # Purchase Form
        st.header("🛍️ Log a Purchase")
        
        with st.form("purchase_form"):
            product_type = st.selectbox(
                "Product Type",
                options=list(PRODUCT_MULTIPLIERS.keys())
            )
            
            # Brand selection with popular brands
            brands_list = POPULAR_BRANDS.get(product_type, ['Custom / Other'])
            selected_brand = st.selectbox("Brand", options=brands_list)
            
            # Custom brand input if "Custom / Other" is selected
            if selected_brand == 'Custom / Other':
                custom_brand = st.text_input("Enter Custom Brand Name", placeholder="e.g., Nike, Apple, Local Farm...")
                final_brand = custom_brand
            else:
                final_brand = selected_brand
            
            price = st.number_input("Price (₹)", min_value=0, step=1, value=0)
            
            # Show estimated CO2
            estimated_co2 = calculate_co2(price, product_type)
            st.info(f"**Estimated CO₂ Impact:** {estimated_co2:.1f} kg")
            
            submit_button = st.form_submit_button("Log Purchase", type="primary")
            
            if submit_button:
                if not final_brand or price <= 0:
                    st.error("Please fill in all fields with valid values.")
                else:
                    # Add purchase
                    purchase = {
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'type': product_type,
                        'brand': final_brand,
                        'price': price,
                        'co2_impact': estimated_co2
                    }
                    st.session_state.purchases.append(purchase)
                    st.session_state.show_alternatives = True
                    st.session_state.last_product_type = product_type
                    
                    # Show success message
                    if product_type in ['Second-Hand Item', 'Local Groceries', 'Books (Used)']:
                        st.success(f"🌟 Eco-friendly choice! You're making a difference!")
                        st.balloons()
                    else:
                        st.success(f"Logged! Your {product_type} added {estimated_co2:.1f} kg of CO₂.")
                    
                    st.rerun()
        
        # Show greener alternatives
        if st.session_state.show_alternatives and st.session_state.last_product_type:
            alternatives = ETHICAL_ALTERNATIVES.get(st.session_state.last_product_type, [])
            if alternatives:
                is_eco_friendly = st.session_state.last_product_type in ['Second-Hand Item', 'Local Groceries', 'Books (Used)']
                
                if is_eco_friendly:
                    st.markdown(f"""
                    <div class="success-message">
                        <h4>🎉 Amazing Choice!</h4>
                        <ul>
                            {''.join([f'<li>{alt}</li>' for alt in alternatives])}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="eco-tip">
                        <h4>✨ Greener choices for {st.session_state.last_product_type}:</h4>
                        <ul>
                            {''.join([f'<li>{alt}</li>' for alt in alternatives])}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Dashboard
        st.header("📈 Your Monthly Dashboard")
        
        # Date filter
        col_filter1, col_filter2, col_filter3 = st.columns([2, 2, 1])
        with col_filter1:
            start_date = st.date_input("Start Date", value=None)
        with col_filter2:
            end_date = st.date_input("End Date", value=None)
        with col_filter3:
            if st.button("Clear Filters"):
                start_date = None
                end_date = None
        
        # Filter purchases
        filtered_purchases = st.session_state.purchases.copy()
        if start_date or end_date:
            filtered_purchases = [
                p for p in filtered_purchases
                if (not start_date or datetime.strptime(p['date'], '%Y-%m-%d').date() >= start_date)
                and (not end_date or datetime.strptime(p['date'], '%Y-%m-%d').date() <= end_date)
            ]
        
        # Calculate metrics
        if filtered_purchases:
            total_co2 = sum(p['co2_impact'] for p in filtered_purchases)
            total_spend = sum(p['price'] for p in filtered_purchases)
            
            # Metrics
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric("Total CO₂ Impact", f"{total_co2:.1f} kg", delta=None)
            with metric_col2:
                st.metric("Total Spend", f"₹{total_spend:.0f}", delta=None)
            
            st.markdown("---")
            
            # Charts
            st.subheader("CO₂ Impact by Product Category")
            
            # Prepare data for bar chart
            df_purchases = pd.DataFrame(filtered_purchases)
            category_data = df_purchases.groupby('type')['co2_impact'].sum().reset_index()
            category_data.columns = ['Category', 'CO2 (kg)']
            
            fig_bar = px.bar(
                category_data,
                x='Category',
                y='CO2 (kg)',
                color='CO2 (kg)',
                color_continuous_scale='Greens'
            )
            fig_bar.update_layout(showlegend=False, xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, use_container_width=True)
            
            st.markdown("---")
            
            # Cumulative CO2 over time
            st.subheader("Cumulative CO₂ Over Time")
            
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
            st.plotly_chart(fig_line, use_container_width=True)
            
            st.markdown("---")
            
            # Purchase Log
            st.subheader("📋 Your Purchase Log")
            
            col_log1, col_log2 = st.columns([3, 1])
            with col_log2:
                if st.button("📥 Export CSV"):
                    csv = df_purchases.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="shopimpact_data.csv",
                        mime="text/csv"
                    )
            
            # Display table
            display_df = df_purchases[['date', 'type', 'brand', 'price', 'co2_impact']].copy()
            display_df.columns = ['Date', 'Product Type', 'Brand', 'Price (₹)', 'CO₂ (kg)']
            display_df['Price (₹)'] = display_df['Price (₹)'].apply(lambda x: f"₹{x:.0f}")
            display_df['CO₂ (kg)'] = display_df['CO₂ (kg)'].apply(lambda x: f"{x:.1f}")
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("No purchases logged yet. Start tracking your impact!")
    
    # Sidebar Column
    with col_sidebar:
        st.header("🏆 Rewards & Tips")
        
        # Calculate monthly stats for badges
        monthly_stats = get_monthly_stats(st.session_state.purchases)
        earned_badges = get_earned_badges(monthly_stats)
        
        # Show badges
        st.subheader("Your Badges")
        if earned_badges:
            for badge in earned_badges:
                st.markdown(f"""
                <div style="background-color: #d1fae5; padding: 10px; border-radius: 8px; 
                            border: 2px solid #10b981; margin: 5px 0; text-align: center;">
                    <span style="font-size: 24px;">{badge['icon']}</span>
                    <p style="margin: 5px 0; font-weight: bold;">{badge['name']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Start logging purchases to earn badges! 🏅")
        
        st.markdown("---")
        
        # Eco Tip
        st.markdown(f"""
        <div class="eco-tip">
            <h4>💡 Eco Tip of the Day</h4>
            <p>{random.choice(TIPS_LIST)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Motivational Quote
        st.markdown(f"""
        <div style="background-color: #e9d5ff; padding: 15px; border-radius: 10px; 
                    border-left: 4px solid #a855f7; margin: 15px 0;">
            <p style="font-style: italic; margin: 0;">"{random.choice(MOTIVATIONAL_QUOTES)}"</p>
        </div>
        """, unsafe_allow_html=True)
        
        # High contrast mode toggle
        st.markdown("---")
        high_contrast = st.checkbox("High Contrast Mode")
        
        # Reset button
        if st.button("🔄 Start a New Month", type="secondary"):
            if st.session_state.purchases:
                st.session_state.purchases = []
                st.success("Fresh start! Ready for a new month of conscious shopping.")
                st.rerun()
        
        # Fun Stats
        if st.session_state.purchases:
            st.markdown("---")
            st.subheader("📈 Fun Stats")
            
            total_items = len(st.session_state.purchases)
            eco_items = sum(1 for p in st.session_state.purchases 
                          if p['type'] in ['Second-Hand Item', 'Local Groceries', 'Books (Used)'])
            
            # Most purchased category
            df_all = pd.DataFrame(st.session_state.purchases)
            most_purchased = df_all['type'].value_counts().index[0] if not df_all.empty else 'N/A'
            
            st.write(f"**Total items tracked:** {total_items}")
            st.write(f"**Eco-friendly purchases:** {eco_items}")
            st.write(f"**Most purchased:** {most_purchased}")

# ========== PROFILE TAB ==========
with tab2:
    st.header("👤 Your Profile")
    
    profile = st.session_state.user_profile
    
    # Profile display
    col_avatar, col_info = st.columns([1, 3])
    with col_avatar:
        avatar_letter = profile['name'][0].upper() if profile['name'] else '?'
        st.markdown(f"""
        <div style="width: 100px; height: 100px; border-radius: 50%; 
                    background-color: #16a34a; color: white; 
                    display: flex; align-items: center; justify-content: center;
                    font-size: 48px; font-weight: bold;">
            {avatar_letter}
        </div>
        """, unsafe_allow_html=True)
    
    with col_info:
        st.markdown(f"### {profile['name'] if profile['name'] else 'Eco Hero'}")
        if profile['location']:
            st.write(f"📍 {profile['location']}")
        
        days_since = (datetime.now() - datetime.strptime(profile['joinDate'], '%Y-%m-%d')).days
        st.write(f"📅 Member for {days_since} days")
    
    st.markdown("---")
    
    # Edit Profile
    with st.expander("✏️ Edit Profile", expanded=False):
        with st.form("profile_form"):
            name = st.text_input("Name", value=profile['name'])
            age = st.text_input("Age", value=profile['age'])
            location = st.text_input("Location", value=profile['location'])
            monthly_budget = st.number_input("Monthly Budget (₹)", value=profile['monthlyBudget'], min_value=0, step=1000)
            co2_goal = st.number_input("Monthly CO₂ Goal (kg)", value=profile['co2Goal'], min_value=0, step=10)
            
            if st.form_submit_button("Save Changes", type="primary"):
                st.session_state.user_profile = {
                    'name': name,
                    'age': age,
                    'location': location,
                    'monthlyBudget': monthly_budget,
                    'co2Goal': co2_goal,
                    'joinDate': profile['joinDate']
                }
                st.success("Profile updated successfully! 🎉")
                st.rerun()
    
    # Monthly Stats
    st.subheader("📊 This Month's Stats")
    
    monthly_stats = get_monthly_stats(st.session_state.purchases)
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    with stat_col1:
        st.metric("Total Spend", f"₹{monthly_stats['totalSpend']:.0f}")
    with stat_col2:
        st.metric("CO₂ Impact", f"{monthly_stats['totalCO2']:.1f} kg")
    with stat_col3:
        st.metric("Purchases", monthly_stats['totalPurchases'])
    with stat_col4:
        st.metric("Eco-Friendly", f"{monthly_stats['ecoFriendlyPercent']:.0f}%")
    
    st.markdown("---")
    
    # Goals vs Eco Standards
    st.subheader("🎯 Your Goals vs Eco Standards")
    
    # Personal Budget Goal
    if profile['monthlyBudget'] > 0:
        budget_progress = min((monthly_stats['totalSpend'] / profile['monthlyBudget']) * 100, 100)
        st.write("**💰 Your Budget Goal**")
        st.write(f"₹{monthly_stats['totalSpend']:.0f} / ₹{profile['monthlyBudget']}")
        st.progress(budget_progress / 100)
        if budget_progress < 100:
            st.caption(f"✅ {100 - budget_progress:.0f}% remaining")
        else:
            st.caption("⚠️ Budget exceeded! Consider eco-friendly alternatives.")
        st.markdown("---")
    
    # Personal CO2 Goal
    if profile['co2Goal'] > 0:
        co2_progress = min((monthly_stats['totalCO2'] / profile['co2Goal']) * 100, 100)
        st.write("**📉 Your CO₂ Goal**")
        st.write(f"{monthly_stats['totalCO2']:.1f} / {profile['co2Goal']} kg")
        st.progress(co2_progress / 100)
        if co2_progress < 100:
            st.caption(f"✅ {100 - co2_progress:.0f}% remaining")
        else:
            st.caption("⚠️ CO₂ goal exceeded! Try second-hand or local options.")
        st.markdown("---")
    
    # Eco Standard - CO2
    eco_co2_progress = min((monthly_stats['totalCO2'] / ECO_STANDARDS['monthlyCO2']) * 100, 100)
    st.write("**🌍 Eco-Friendly CO₂ Standard**")
    st.write(f"{monthly_stats['totalCO2']:.1f} / {ECO_STANDARDS['monthlyCO2']} kg")
    st.progress(eco_co2_progress / 100)
    if eco_co2_progress < 100:
        st.caption(f"🎉 Great! You're {100 - eco_co2_progress:.0f}% below eco standards!")
    else:
        st.caption(f"⚠️ {eco_co2_progress - 100:.0f}% above eco-friendly limit.")
    st.markdown("---")
    
    # Eco Standard - Budget
    eco_budget_progress = min((monthly_stats['totalSpend'] / ECO_STANDARDS['monthlyBudget']) * 100, 100)
    st.write("**💚 Eco-Conscious Budget Standard**")
    st.write(f"₹{monthly_stats['totalSpend']:.0f} / ₹{ECO_STANDARDS['monthlyBudget']}")
    st.progress(eco_budget_progress / 100)
    if eco_budget_progress < 100:
        st.caption(f"✅ Excellent! {100 - eco_budget_progress:.0f}% under eco budget.")
    else:
        st.caption("⚠️ Consider reducing consumption this month.")
    st.markdown("---")
    
    # Eco-Friendly Percentage
    eco_percent_progress = min((monthly_stats['ecoFriendlyPercent'] / ECO_STANDARDS['ecoFriendlyPercentage']) * 100, 100)
    st.write("**♻️ Eco-Friendly Purchases**")
    st.write(f"{monthly_stats['ecoFriendlyPercent']:.0f}% / {ECO_STANDARDS['ecoFriendlyPercentage']}%")
    st.progress(eco_percent_progress / 100)
    if monthly_stats['ecoFriendlyPercent'] >= ECO_STANDARDS['ecoFriendlyPercentage']:
        st.caption("🎉 Amazing! You're shopping sustainably!")
    else:
        st.caption("💡 Try adding more second-hand or local items.")
    
    st.markdown("---")
    
    # Spending-Based Badges
    st.subheader("🏆 Your Badges")
    
    earned_badges = get_earned_badges(monthly_stats)
    
    if earned_badges:
        badge_cols = st.columns(2)
        for idx, badge in enumerate(earned_badges):
            with badge_cols[idx % 2]:
                limit_text = f"CO₂ under {badge['limit']} kg" if badge['type'] == 'co2' else f"Spending under ₹{badge['limit']}"
                st.markdown(f"""
                <div style="background-color: #d1fae5; padding: 15px; border-radius: 10px; 
                            border: 2px solid #10b981; margin: 10px 0;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 32px;">{badge['icon']}</span>
                        <div>
                            <p style="margin: 0; font-weight: bold; font-size: 16px;">{badge['name']}</p>
                            <p style="margin: 0; font-size: 12px; color: #666;">{limit_text}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No badges earned this month yet! Keep your spending and CO₂ under limits to earn badges.")
    
    # Available badges
    st.write("**Available Badges:**")
    badge_grid_cols = st.columns(3)
    for idx, badge in enumerate(SPENDING_BADGES):
        is_earned = any(b['name'] == badge['name'] for b in earned_badges)
        with badge_grid_cols[idx % 3]:
            opacity = "1.0" if is_earned else "0.5"
            bg_color = "#d1fae5" if is_earned else "#f3f4f6"
            border_color = "#10b981" if is_earned else "#d1d5db"
            limit_text = f"<{badge['limit']}kg" if badge['type'] == 'co2' else f"<₹{badge['limit']}"
            
            st.markdown(f"""
            <div style="background-color: {bg_color}; padding: 10px; border-radius: 8px; 
                        border: 1px solid {border_color}; margin: 5px 0; text-align: center;
                        opacity: {opacity};">
                <span style="font-size: 24px;">{badge['icon']}</span>
                <p style="margin: 5px 0; font-size: 12px; font-weight: bold;">{badge['name']}</p>
                <p style="margin: 0; font-size: 10px; color: #666;">{limit_text}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Lifetime Achievements
    st.subheader("🌟 Lifetime Achievements")
    
    total_purchases = len(st.session_state.purchases)
    total_spent = sum(p['price'] for p in st.session_state.purchases)
    total_eco = sum(1 for p in st.session_state.purchases 
                   if p['type'] in ['Second-Hand Item', 'Local Groceries', 'Books (Used)'])
    
    achieve_col1, achieve_col2, achieve_col3, achieve_col4 = st.columns(4)
    
    with achieve_col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px;">
            <p style="font-size: 36px; margin: 0;">🛍️</p>
            <p style="font-size: 20px; margin: 5px 0; font-weight: bold;">{total_purchases}</p>
            <p style="font-size: 12px; margin: 0; color: #666;">Total Purchases</p>
        </div>
        """, unsafe_allow_html=True)
    
    with achieve_col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px;">
            <p style="font-size: 36px; margin: 0;">💰</p>
            <p style="font-size: 20px; margin: 5px 0; font-weight: bold;">₹{total_spent:.0f}</p>
            <p style="font-size: 12px; margin: 0; color: #666;">Total Spent</p>
        </div>
        """, unsafe_allow_html=True)
    
    with achieve_col3:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px;">
            <p style="font-size: 36px; margin: 0;">🌱</p>
            <p style="font-size: 20px; margin: 5px 0; font-weight: bold;">{total_eco}</p>
            <p style="font-size: 12px; margin: 0; color: #666;">Eco Purchases</p>
        </div>
        """, unsafe_allow_html=True)
    
    with achieve_col4:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px;">
            <p style="font-size: 36px; margin: 0;">🏆</p>
            <p style="font-size: 20px; margin: 5px 0; font-weight: bold;">{len(earned_badges)}</p>
            <p style="font-size: 12px; margin: 0; color: #666;">Badges Earned</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #9ca3af; font-size: 14px;'>ShopImpact 🍃 | Making conscious shopping easy and fun!</p>",
    unsafe_allow_html=True
)
