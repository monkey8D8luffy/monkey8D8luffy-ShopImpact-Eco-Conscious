# monkey8D8luffy-ShopImpact-Eco-Conscious
# ShopImpact - Streamlit Version 🍃

A colorful, interactive, and friendly web app built with Python and Streamlit to help users become mindful, eco-conscious shoppers.

## Features

### 📊 Dashboard
- **Purchase Logging**: Log purchases with product type, brand (popular brands + custom option), and price in rupees (₹)
- **CO₂ Calculation**: Instant CO₂ footprint estimation for each purchase
- **Live Dashboard**: Real-time metrics showing total monthly CO₂ impact and spending
- **Visualizations**: 
  - Bar chart showing CO₂ impact by product category
  - Line chart showing cumulative CO₂ over time
- **Purchase Log**: Complete table of all logged purchases
- **Date Filtering**: Filter dashboard data by date range
- **CSV Export**: Download your purchase data

### 👤 Profile
- **User Information**: Store name, age, location, monthly budget, and CO₂ goals
- **Comparison Bars**: Compare your impact against eco-friendly standards
  - Personal budget goal vs actual spending
  - Personal CO₂ goal vs actual emissions
  - Eco-friendly CO₂ standard (100 kg/month)
  - Eco-conscious budget standard (₹15,000/month)
  - Eco-friendly purchase percentage (30% target)
- **Progress Tracking**: Visual progress bars with color-coded feedback (green/yellow/red)
- **Lifetime Achievements**: Total purchases, spending, eco items, and badges earned

### 🏆 Rewards & Gamification
- **Spending-Based Badges**:
  - 💰 Frugal Shopper (spending under ₹5,000)
  - 🎯 Budget Conscious (spending under ₹10,000)
  - 🌟 Mindful Spender (spending under ₹15,000)
  - 🌱 Carbon Neutral Goal (CO₂ under 50 kg)
  - 🦸 Eco Warrior (CO₂ under 30 kg)
- **Eco Tips**: Random sustainability tips displayed in sidebar
- **Motivational Quotes**: Encouraging messages
- **Fun Stats**: Track total items, eco-friendly purchases, and favorite categories

### 🌱 Eco-Friendly Features
- **Greener Alternatives**: Instant suggestions for ethical alternatives after logging purchases
- **Popular Brands**: Quick-select from popular brands in each category
- **Celebration**: Special congratulations for eco-friendly purchases (Second-Hand, Local, Used Books)
- **Positive Reinforcement**: Empowering, guilt-free tone throughout

## Installation

1. **Install Python** (version 3.8 or higher)

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

1. **Navigate to the project directory** in your terminal

2. **Run the Streamlit app**:
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Open your browser** - Streamlit will automatically open at `http://localhost:8501`

## Data Persistence

The app uses Streamlit's session state for data persistence during the session. Data is stored in:
- `st.session_state.purchases` - List of all purchase records
- `st.session_state.user_profile` - User profile information

**Note**: Data resets when you close the browser tab or restart the app. For permanent storage, you would need to add database integration (e.g., SQLite, PostgreSQL, or cloud storage).

## Usage Guide

### Logging a Purchase
1. Navigate to the **Dashboard** tab
2. Select a **Product Type** from the dropdown
3. Choose a **Brand** (popular brands or select "Custom / Other" to enter your own)
4. Enter the **Price in ₹** (rupees)
5. Review the estimated CO₂ impact
6. Click **Log Purchase**

### Setting Up Your Profile
1. Navigate to the **Profile** tab
2. Click **Edit Profile**
3. Fill in your information:
   - Name
   - Age
   - Location
   - Monthly Budget Goal (₹)
   - Monthly CO₂ Goal (kg)
4. Click **Save Changes**

### Viewing Progress
- Check the **Dashboard** for purchase history and charts
- Visit the **Profile** tab to see progress against goals
- Compare your impact with eco-friendly standards
- View earned badges based on your spending limits

### Exporting Data
1. Go to the **Dashboard** tab
2. Scroll to the Purchase Log section
3. Click **Export CSV**
4. Click **Download CSV** to save your data

### Starting Fresh
Click **🔄 Start a New Month** in the sidebar to clear all purchase data and begin tracking a new month.

## Product Categories & CO₂ Multipliers

- **Fast Fashion**: 2.5x
- **Electronics**: 1.8x
- **Local Groceries**: 0.3x (eco-friendly!)
- **Second-Hand Item**: 0.1x (eco-friendly!)
- **Restaurant Meal**: 0.8x
- **Leather Goods**: 3.0x
- **Cosmetics**: 1.5x
- **Home Decor**: 1.2x
- **Books (New)**: 0.5x
- **Books (Used)**: 0.05x (eco-friendly!)

## Eco-Friendly Standards

- **Monthly CO₂ Limit**: 100 kg
- **Eco-Conscious Budget**: ₹15,000
- **Eco-Friendly Purchase Target**: 30% of all purchases

## Customization

You can customize the app by modifying these dictionaries in `streamlit_app.py`:

- `PRODUCT_MULTIPLIERS` - CO₂ calculation multipliers
- `ETHICAL_ALTERNATIVES` - Suggested greener alternatives
- `POPULAR_BRANDS` - Popular brands by category
- `ECO_STANDARDS` - Eco-friendly benchmarks
- `SPENDING_BADGES` - Badge criteria and limits
- `TIPS_LIST` - Eco tips displayed in sidebar
- `MOTIVATIONAL_QUOTES` - Inspirational quotes

## Technologies Used

- **Python 3.8+**
- **Streamlit** - Web app framework
- **Pandas** - Data manipulation
- **Plotly** - Interactive charts

## Future Enhancements

Potential features to add:
- Database integration for permanent data storage
- User authentication and multi-user support
- Social sharing of achievements
- Monthly challenges and goals
- Product API integration for real CO₂ data
- Carbon offset recommendations
- Community leaderboard

## License

This is a sample educational project for demonstrating eco-conscious shopping tracking.

---

Made with 💚 for conscious shoppers everywhere!
