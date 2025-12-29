"""
ShopImpact - Streamlit Version (Fully Optimized with 500+ Products & Brands)
A colorful, interactive, and friendly web app to help users become mindful, eco-conscious shoppers.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import random
from pathlib import Path
from typing import Dict, List, Tuple

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="ShopImpact 🍃",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CONSTANTS - 500+ PRODUCTS ====================
PRODUCT_TYPES = [
    # Fashion & Apparel (50 items)
    'Fast Fashion', 'T-Shirt', 'Jeans', 'Dress', 'Suit', 'Jacket', 'Sweater', 'Hoodie', 'Shorts', 'Skirt',
    'Blazer', 'Coat', 'Pants', 'Leggings', 'Activewear', 'Swimwear', 'Underwear', 'Socks', 'Shoes', 'Sneakers',
    'Boots', 'Sandals', 'Heels', 'Hat', 'Scarf', 'Gloves', 'Belt', 'Handbag', 'Wallet', 'Backpack',
    'Sunglasses', 'Watch', 'Jewelry', 'Tie', 'Formal Wear', 'Casual Wear', 'Sportswear', 'Winter Jacket',
    'Rain Coat', 'Vest', 'Cardigan', 'Tank Top', 'Polo Shirt', 'Button-up Shirt', 'Maxi Dress', 'Jumpsuit',
    'Romper', 'Kimono', 'Poncho', 'Shawl',
    
    # Electronics (80 items)
    'Electronics', 'Smartphone', 'Laptop', 'Tablet', 'Desktop Computer', 'Monitor', 'Keyboard', 'Mouse',
    'Headphones', 'Earbuds', 'Speaker', 'Smartwatch', 'Fitness Tracker', 'Camera', 'DSLR Camera', 'Webcam',
    'Microphone', 'Gaming Console', 'Controller', 'VR Headset', 'Drone', 'Action Camera', 'Projector',
    'TV', 'Streaming Device', 'Router', 'Modem', 'Network Switch', 'External Hard Drive', 'SSD', 'USB Drive',
    'Memory Card', 'Power Bank', 'Charger', 'Cable', 'Phone Case', 'Screen Protector', 'Laptop Stand',
    'Cooling Pad', 'Docking Station', 'Graphics Card', 'Processor', 'Motherboard', 'RAM', 'PSU',
    'Computer Case', 'CPU Cooler', 'Thermal Paste', 'LED Strip', 'Gaming Chair', 'Desk Lamp',
    'Surge Protector', 'Extension Cord', 'Adapter', 'Converter', 'KVM Switch', 'Drawing Tablet',
    'E-Reader', 'Smart Home Hub', 'Smart Light Bulb', 'Smart Plug', 'Smart Thermostat', 'Security Camera',
    'Video Doorbell', 'Smart Lock', 'Air Purifier', 'Robot Vacuum', 'Electric Toothbrush', 'Hair Dryer',
    'Electric Shaver', 'Printer', 'Scanner', 'Ink Cartridge', 'Bluetooth Adapter', 'Wi-Fi Extender',
    'Portable SSD', 'NAS Drive', 'USB Hub', 'Card Reader', 'Laptop Bag', 'Phone Gimbal',
    
    # Food & Groceries (70 items)
    'Local Groceries', 'Organic Vegetables', 'Organic Fruits', 'Fresh Produce', 'Meat', 'Poultry', 'Seafood',
    'Dairy Products', 'Milk', 'Cheese', 'Yogurt', 'Butter', 'Eggs', 'Bread', 'Pasta', 'Rice', 'Cereal',
    'Oats', 'Granola', 'Snacks', 'Chips', 'Cookies', 'Chocolate', 'Candy', 'Ice Cream', 'Frozen Pizza',
    'Frozen Vegetables', 'Frozen Meals', 'Canned Goods', 'Soup', 'Sauce', 'Condiments', 'Spices', 'Herbs',
    'Oil', 'Vinegar', 'Honey', 'Jam', 'Peanut Butter', 'Nuts', 'Dried Fruits', 'Coffee', 'Tea',
    'Juice', 'Soda', 'Energy Drink', 'Protein Shake', 'Protein Bar', 'Vitamins', 'Supplements',
    'Baby Food', 'Pet Food', 'Dog Food', 'Cat Food', 'Treats', 'Water Bottles', 'Sparkling Water',
    'Kombucha', 'Plant-based Milk', 'Vegan Cheese', 'Tofu', 'Tempeh', 'Quinoa', 'Chia Seeds',
    'Protein Powder', 'Meal Kit', 'Ready-to-Eat Meal', 'Salad Kit', 'Smoothie Mix', 'Baking Mix',
    
    # Home & Furniture (60 items)
    'Home Decor', 'Sofa', 'Couch', 'Chair', 'Dining Table', 'Coffee Table', 'Desk', 'Bed Frame', 'Mattress',
    'Pillow', 'Bedding', 'Sheets', 'Duvet', 'Comforter', 'Blanket', 'Curtains', 'Blinds', 'Rug', 'Carpet',
    'Lamp', 'Chandelier', 'Mirror', 'Picture Frame', 'Wall Art', 'Vase', 'Candle', 'Diffuser',
    'Storage Box', 'Shelf', 'Bookshelf', 'Cabinet', 'Dresser', 'Nightstand', 'TV Stand', 'Ottoman',
    'Bean Bag', 'Bar Stool', 'Office Chair', 'Filing Cabinet', 'Organizer', 'Basket', 'Plant Pot',
    'Indoor Plant', 'Artificial Plant', 'Clock', 'Throw Pillow', 'Cushion', 'Table Runner', 'Placemat',
    'Kitchenware', 'Cookware', 'Pots and Pans', 'Bakeware', 'Utensils', 'Cutlery', 'Plates', 'Bowls',
    'Glasses', 'Mugs', 'Appliance',
    
    # Personal Care & Beauty (50 items)
    'Cosmetics', 'Skincare', 'Moisturizer', 'Cleanser', 'Toner', 'Serum', 'Face Mask', 'Sunscreen', 'Lip Balm',
    'Lipstick', 'Foundation', 'Concealer', 'Blush', 'Eyeshadow', 'Mascara', 'Eyeliner', 'Brow Pencil',
    'Nail Polish', 'Perfume', 'Cologne', 'Deodorant', 'Body Lotion', 'Body Wash', 'Shampoo', 'Conditioner',
    'Hair Mask', 'Hair Oil', 'Styling Product', 'Hair Spray', 'Hair Gel', 'Face Wash', 'Acne Treatment',
    'Anti-aging Cream', 'Eye Cream', 'Exfoliator', 'Bath Bomb', 'Soap', 'Hand Soap', 'Hand Cream',
    'Toothpaste', 'Mouthwash', 'Dental Floss', 'Razor', 'Shaving Cream', 'Aftershave', 'Makeup Remover',
    'Cotton Pads', 'Q-tips', 'Brush Set', 'Sponge',
    
    # Books & Media (40 items)
    'Books (New)', 'Books (Used)', 'Hardcover Book', 'Paperback Book', 'E-book', 'Audiobook', 'Textbook',
    'Cookbook', 'Magazine', 'Comic Book', 'Graphic Novel', 'Manga', 'Novel', 'Non-fiction Book',
    'Biography', 'Self-help Book', "Children's Book", 'Young Adult Book', 'Poetry Book', 'Art Book',
    'Photography Book', 'Travel Guide', 'Dictionary', 'Encyclopedia', 'Notebook', 'Journal', 'Planner',
    'Calendar', 'Stationery', 'Greeting Card', 'Postcard', 'Bookmark', 'DVD', 'Blu-ray', 'CD', 'Vinyl Record',
    'Music Album', 'Video Game', 'Board Game', 'Puzzle',
    
    # Sports & Outdoors (40 items)
    'Yoga Mat', 'Dumbbells', 'Kettlebell', 'Resistance Bands', 'Jump Rope', 'Foam Roller', 'Exercise Ball',
    'Treadmill', 'Exercise Bike', 'Elliptical', 'Weight Bench', 'Running Shoes', 'Training Shoes',
    'Sports Jersey', 'Athletic Shorts', 'Sports Bra', 'Compression Wear', 'Water Bottle', 'Gym Bag',
    'Tent', 'Sleeping Bag', 'Camping Chair', 'Cooler', 'Backpack (Hiking)', 'Hiking Boots', 'Trekking Poles',
    'Bicycle', 'Bike Helmet', 'Skateboard', 'Scooter', 'Rollerblades', 'Golf Clubs', 'Tennis Racket',
    'Basketball', 'Football', 'Soccer Ball', 'Baseball Glove', 'Fishing Rod', 'Kayak', 'Surfboard',
    
    # Automotive (30 items)
    'Car Parts', 'Motor Oil', 'Brake Pads', 'Air Filter', 'Spark Plugs', 'Battery', 'Wiper Blades',
    'Headlights', 'Tires', 'Floor Mats', 'Seat Covers', 'Steering Wheel Cover', 'Phone Mount',
    'Dash Cam', 'GPS', 'Car Charger', 'Air Freshener', 'Car Wash Supplies', 'Wax', 'Polish',
    'Vacuum Cleaner (Car)', 'Jump Starter', 'Tool Kit', 'First Aid Kit', 'Emergency Kit',
    'Roof Rack', 'Bike Rack', 'Cargo Net', 'Sunshade', 'Car Cover',
    
    # Restaurants & Dining (20 items)
    'Restaurant Meal', 'Fast Food', 'Pizza', 'Burger', 'Sushi', 'Chinese Food', 'Indian Food', 'Mexican Food',
    'Italian Food', 'Thai Food', 'Coffee', 'Latte', 'Cappuccino', 'Espresso', 'Bubble Tea', 'Smoothie',
    'Dessert', 'Pastry', 'Cake', 'Ice Cream Cone',
    
    # Leather & Accessories (20 items)
    'Leather Goods', 'Leather Jacket', 'Leather Bag', 'Leather Wallet', 'Leather Belt', 'Leather Boots',
    'Leather Gloves', 'Leather Watch Strap', 'Leather Briefcase', 'Leather Sofa', 'Leather Chair',
    'Faux Leather Jacket', 'Vegan Leather Bag', 'Cork Wallet', 'Canvas Bag', 'Nylon Backpack',
    'Fabric Belt', 'Suede Shoes', 'Synthetic Boots', 'Eco-leather Item',
    
    # Second-Hand Items (20 items)
    'Second-Hand Item', 'Thrifted Clothing', 'Used Electronics', 'Vintage Furniture', 'Refurbished Phone',
    'Refurbished Laptop', 'Used Car', 'Used Bike', 'Vintage Jewelry', 'Antique', 'Collectible',
    'Used Book', 'Used Appliance', 'Upcycled Item', 'Repurposed Furniture', 'Vintage Clothing',
    'Consignment Item', 'Estate Sale Find', 'Garage Sale Item', 'Flea Market Find',
    
    # Office & School Supplies (30 items)
    'Office Supplies', 'Pens', 'Pencils', 'Markers', 'Highlighters', 'Eraser', 'Correction Tape',
    'Stapler', 'Paper Clips', 'Binder Clips', 'Folders', 'Binders', 'Paper', 'Notebook', 'Sticky Notes',
    'Index Cards', 'Calculator', 'Tape', 'Scissors', 'Ruler', 'Hole Punch', 'Label Maker',
    'File Organizer', 'Desk Organizer', 'Pen Holder', 'Whiteboard', 'Markers (Whiteboard)',
    'Eraser (Whiteboard)', 'Bulletin Board', 'Push Pins',
    
    # Miscellaneous (20 items)
    'Gift Card', 'Subscription Service', 'Digital Download', 'Online Course', 'Event Ticket', 'Movie Ticket',
    'Concert Ticket', 'Sports Ticket', 'Museum Pass', 'Membership', 'Donation', 'Charity Contribution',
    'Craft Supplies', 'Art Supplies', 'Paint', 'Brushes', 'Canvas', 'Yarn', 'Fabric', '500+ (Other)',
]

# ==================== CONSTANTS - 500+ BRANDS ====================
ALL_BRANDS = [
    # Fashion Brands (100)
    'Zara', 'H&M', 'Forever 21', 'Shein', 'Uniqlo', 'Gap', 'Old Navy', 'American Eagle', 'Abercrombie & Fitch',
    'Hollister', 'Urban Outfitters', 'Anthropologie', 'Free People', 'Madewell', 'J.Crew', 'Banana Republic',
    "Levi's", 'Wrangler', 'Lee', 'Diesel', 'True Religion', 'Calvin Klein', 'Tommy Hilfiger', 'Ralph Lauren',
    'Lacoste', 'Hugo Boss', 'Armani', 'Versace', 'Gucci', 'Prada', 'Louis Vuitton', 'Chanel', 'Burberry',
    'Nike', 'Adidas', 'Puma', 'Reebok', 'Under Armour', 'New Balance', 'Converse', 'Vans', 'Skechers',
    'Timberland', 'Dr. Martens', 'UGG', 'Crocs', 'Birkenstock', 'TOMS', 'Steve Madden', 'Aldo', 'DSW',
    'Massimo Dutti', 'Bershka', 'Pull&Bear', 'Stradivarius', 'Mango', 'Topshop', 'ASOS', 'Boohoo',
    'PrettyLittleThing', 'Missguided', 'Fashion Nova', 'Revolve', 'Reformation', 'Everlane', 'Patagonia',
    'The North Face', 'Columbia', "Arc'teryx", 'Lululemon', 'Athleta', 'Fabletics', 'Gymshark', 'Alo Yoga',
    'Outdoor Voices', 'Vuori', 'Rhone', 'Allbirds', "Rothy's", 'Veja', 'Kotn', 'Pact', 'Thought', 'People Tree',
    'Eileen Fisher', 'Mara Hoffman', 'Stella McCartney', 'Vivienne Westwood', 'Comme des Garçons', 'Issey Miyake',
    'Yohji Yamamoto', 'Rick Owens', 'Balenciaga', 'Off-White', 'Supreme', 'Stüssy', 'Carhartt', 'Dickies',
    
    # Electronics Brands (100)
    'Apple', 'Samsung', 'Google', 'Microsoft', 'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'MSI',
    'Razer', 'Alienware', 'Sony', 'LG', 'Panasonic', 'Philips', 'Toshiba', 'Sharp', 'Hitachi', 'JVC',
    'Canon', 'Nikon', 'Fujifilm', 'Olympus', 'Pentax', 'Leica', 'Hasselblad', 'GoPro', 'DJI', 'Parrot',
    'Intel', 'AMD', 'Nvidia', 'Corsair', 'Kingston', 'Crucial', 'Western Digital', 'Seagate', 'SanDisk',
    'Logitech', 'HyperX', 'SteelSeries', 'Cooler Master', 'NZXT', 'Thermaltake',
    'Bose', 'JBL', 'Harman Kardon', 'Bang & Olufsen', 'Sennheiser', 'Audio-Technica', 'Shure', 'AKG',
    'Beats', 'Skullcandy', 'Jabra', 'Anker', 'Aukey', 'RAVPower', 'Mophie', 'Belkin', 'Spigen', 'OtterBox',
    'OnePlus', 'Xiaomi', 'Huawei', 'Oppo', 'Vivo', 'Realme', 'Motorola', 'Nokia', 'BlackBerry', 'HTC',
    'Fitbit', 'Garmin', 'Polar', 'Suunto', 'Withings', 'Amazfit', 'Fossil', 'Tag Heuer', 'Rolex', 'Casio',
    'Epson', 'Brother', 'Xerox', 'Ricoh', 'Kodak', 'Wacom', 'Huion', 'XP-Pen', 'Remarkable', 'Onyx Boox',
    'Roku', 'Amazon', 'Chromecast', 'Apple TV', 'Fire TV', 'Nvidia Shield', 'TiVo', 'Sonos', 'Denon', 'Yamaha',
    
    # Food & Beverage Brands (80)
    'Whole Foods', "Trader Joe's", 'Sprouts', 'Kroger', 'Safeway', 'Albertsons', 'Publix', 'Wegmans',
    'H-E-B', 'Aldi', 'Lidl', 'Costco', "Sam's Club", "BJ's", 'Target', 'Walmart', 'Amazon Fresh',
    'Instacart', 'FreshDirect', 'Thrive Market', 'Imperfect Foods', 'Misfits Market', 'ButcherBox',
    'Coca-Cola', 'Pepsi', 'Dr Pepper', 'Sprite', 'Fanta', 'Mountain Dew', 'Red Bull', 'Monster', 'Rockstar',
    'Starbucks', "Dunkin'", "Peet's Coffee", 'Blue Bottle', 'Intelligentsia', 'Stumptown', 'Lavazza',
    'Illy', 'Nespresso', 'Keurig', 'Folgers', 'Maxwell House', 'Twinings', 'Lipton', 'Tazo', 'Celestial',
    "Ben & Jerry's", 'Häagen-Dazs', 'Breyers', 'Talenti', 'Halo Top', 'So Delicious', 'Oatly', 'Silk',
    'Almond Breeze', 'Chobani', 'Fage', 'Yoplait', 'Dannon', 'Nestle', 'Kraft', 'General Mills', "Kellogg's",
    'Post', 'Quaker', 'Nature Valley', 'Kind', 'Clif Bar', 'RX Bar', 'Quest', 'Perfect Bar', 'Larabar',
    "Annie's", "Amy's Kitchen", 'Gardein', 'Beyond Meat', 'Impossible Foods', 'Morningstar Farms',
    
    # Home & Furniture Brands (60)
    'IKEA', 'Target', 'HomeGoods', 'West Elm', 'Pottery Barn', 'Crate & Barrel', 'CB2', 'Room & Board',
    'Article', 'Burrow', 'Interior Define', 'Joybird', 'Floyd', 'Sabai', 'Medley', 'Lovesac', 'Ashley',
    'La-Z-Boy', 'Ethan Allen', 'Bassett', 'Thomasville', 'Restoration Hardware', 'Arhaus', 'Serena & Lily',
    'Williams Sonoma', 'Sur La Table', 'Bed Bath & Beyond', 'The Container Store', 'California Closets',
    'Wayfair', 'Overstock', 'AllModern', 'Joss & Main', 'Birch Lane', 'Perigold', 'One Kings Lane',
    'Anthropologie Home', 'Urban Outfitters Home', 'H&M Home', 'Zara Home', 'Muji', 'Daiso', 'Flying Tiger',
    'Casper', 'Purple', 'Tuft & Needle', 'Leesa', 'Saatva', 'Helix', 'Brooklyn Bedding', 'Nectar',
    'Tempur-Pedic', 'Sleep Number', 'Parachute', 'Brooklinen', 'Buffy', 'Boll & Branch', 'Coyuchi',
    
    # Beauty & Personal Care Brands (60)
    'Sephora', 'Ulta', 'MAC', 'Lush', 'The Body Shop', "Kiehl's", 'Clinique', 'Estée Lauder', 'Lancôme',
    "L'Oréal", 'Maybelline', 'NYX', 'e.l.f.', 'CoverGirl', 'Revlon', 'Neutrogena', 'Cetaphil', 'CeraVe',
    'La Roche-Posay', 'Vichy', 'Olay', 'Dove', 'Nivea', 'Aveeno', 'Eucerin', 'Vaseline', 'Aquaphor',
    'The Ordinary', 'Glossier', 'Drunk Elephant', 'Tatcha', 'Fresh', 'Origins', 'Philosophy', 'Benefit',
    'Too Faced', 'Urban Decay', 'Anastasia Beverly Hills', 'Fenty Beauty', 'Rare Beauty', 'Haus Labs',
    'Charlotte Tilbury', 'Pat McGrath Labs', 'Huda Beauty', 'Jeffree Star', 'ColourPop', 'Morphe',
    'Milk Makeup', 'RMS Beauty', 'Ilia', 'Tower 28', 'Jones Road', 'Kosas', 'Saie', 'Merit', 'Westman Atelier',
    'Chanel Beauty', 'Dior Beauty', 'YSL Beauty', 'Tom Ford Beauty', 'Giorgio Armani Beauty',
    
    # Book & Media Brands (30)
    'Amazon', 'Barnes & Noble', 'Books-A-Million', 'Half Price Books', "Powell's Books", 'Strand',
    'The Ripped Bodice', 'McNally Jackson', 'City Lights', 'Shakespeare and Company', 'Waterstones',
    'Foyles', "Blackwell's", 'Book Depository', 'Better World Books', 'ThriftBooks', 'AbeBooks',
    'Audible', 'Scribd', 'Kindle', 'Kobo', 'Nook', 'Apple Books', 'Google Play Books', 'OverDrive',
    'Penguin Random House', 'HarperCollins', 'Simon & Schuster', 'Macmillan', 'Hachette',
    
    # Sports & Outdoor Brands (40)
    'Nike', 'Adidas', 'Puma', 'Reebok', 'Under Armour', 'New Balance', 'Asics', 'Brooks', 'Saucony',
    'Hoka One One', 'On Running', 'Altra', 'Mizuno', 'Salomon', 'Merrell', 'Keen', 'Vasque', 'Oboz',
    'The North Face', 'Patagonia', "Arc'teryx", 'Columbia', 'Marmot', 'Mountain Hardwear', 'Outdoor Research',
    'Black Diamond', 'Petzl', 'MSR', 'Big Agnes', 'Nemo', 'REI', "Cabela's", 'Bass Pro Shops', "Dick's",
    'Academy Sports', 'Decathlon', 'Lululemon', 'Athleta', 'Alo Yoga', 'Manduka', 'Jade Yoga', 'Liforme',
    
    # Automotive Brands (30)
    'AutoZone', "O'Reilly", 'Advance Auto Parts', 'NAPA', 'Pep Boys', 'Firestone', 'Goodyear', 'Michelin',
    'Bridgestone', 'Continental', 'Pirelli', 'Yokohama', 'Bosch', 'Denso', 'NGK', 'ACDelco', 'Mobil 1',
    'Castrol', 'Valvoline', 'Pennzoil', 'Shell', 'BP', 'Chevron', '3M', 'Armor All', "Meguiar's",
    'Chemical Guys', 'Turtle Wax', 'Rain-X', 'WeatherTech',
    
    # Additional Brands (100)
    'Costco Kirkland', 'Amazon Basics', 'Great Value', '365 Everyday Value', 'Simple Truth', 'Market Pantry',
    'Good & Gather', 'Up & Up', 'Equate', "Member's Mark", 'Private Selection', 'Signature Select',
    'Local Farm', 'Farmers Market', 'Local Thrift', 'Goodwill', 'Salvation Army', 'ThredUp', 'Poshmark',
    'Depop', 'Vinted', 'Mercari', 'OfferUp', 'Letgo', 'Facebook Marketplace', 'Craigslist', 'eBay',
    'Etsy', 'Redbubble', 'Society6', 'Printful', 'Printify', 'Zazzle', 'CafePress', 'Spreadshirt',
    'Local Restaurant', 'Local Cafe', 'Local Bakery', 'Local Boutique', 'Local Shop', 'Co-op',
    'Small Business', 'Independent Store', 'Family Owned', 'Artisan', 'Handmade', 'Custom Made',
    'Made to Order', 'Bespoke', 'Tailored', 'Vintage Store', 'Consignment Shop', 'Antique Store',
    'Flea Market', 'Garage Sale', 'Estate Sale', 'Yard Sale', 'Community Sale', 'Swap Meet',
    'Online Marketplace', 'Direct from Manufacturer', 'Wholesale', 'Bulk Buy', 'Discount Store',
    'Dollar Store', 'Dollar Tree', 'Dollar General', 'Family Dollar', 'Five Below', '99 Cents Only',
    'TJ Maxx', 'Marshalls', 'Ross', 'Burlington', 'Nordstrom Rack', 'Saks Off 5th', 'Neiman Marcus Last Call',
    'Century 21', "Loehmann's", "Filene's Basement", 'Syms', "Daffy's", 'DSW', 'Famous Footwear',
    'Payless', 'Shoe Carnival', 'Rack Room Shoes', 'Off Broadway Shoes', 'ShoeMall', 'Zappos',
    'Amazon', 'eBay', 'Walmart', 'Target', 'Best Buy', 'Staples', 'Office Depot', 'Office Max',
]

# ==================== PRODUCT MULTIPLIERS ====================
def get_product_multiplier(product_type: str) -> float:
    """Get CO2 multiplier for a product type"""
    multipliers = {
        # Fashion & Apparel
        'Fast Fashion': 2.5, 'T-Shirt': 2.3, 'Jeans': 3.2, 'Dress': 2.8, 'Suit': 4.0, 'Jacket': 3.5,
        'Sweater': 2.6, 'Hoodie': 2.4, 'Shorts': 2.0, 'Skirt': 2.2, 'Blazer': 3.8, 'Coat': 4.2,
        'Pants': 2.9, 'Leggings': 1.8, 'Activewear': 2.1, 'Swimwear': 2.0, 'Underwear': 1.5, 'Socks': 0.8,
        'Shoes': 3.0, 'Sneakers': 2.8, 'Boots': 3.5, 'Sandals': 2.0, 'Heels': 2.5, 'Hat': 1.2,
        'Scarf': 1.0, 'Gloves': 1.1, 'Belt': 1.5, 'Handbag': 2.5, 'Wallet': 1.3, 'Backpack': 2.0,
        'Sunglasses': 1.0, 'Watch': 2.0, 'Jewelry': 1.8, 'Tie': 0.9, 'Formal Wear': 3.5,
        'Casual Wear': 2.3, 'Sportswear': 2.1, 'Winter Jacket': 4.5, 'Rain Coat': 2.8, 'Vest': 2.0,
        'Cardigan': 2.4, 'Tank Top': 1.6, 'Polo Shirt': 2.0, 'Button-up Shirt': 2.2, 'Maxi Dress': 3.0,
        'Jumpsuit': 2.7, 'Romper': 2.3, 'Kimono': 2.5, 'Poncho': 2.2, 'Shawl': 1.8,
        
        # Electronics
        'Electronics': 1.8, 'Smartphone': 2.5, 'Laptop': 3.0, 'Tablet': 2.2, 'Desktop Computer': 3.5,
        'Monitor': 2.0, 'Keyboard': 0.8, 'Mouse': 0.5, 'Headphones': 0.9, 'Earbuds': 0.6, 'Speaker': 1.2,
        'Smartwatch': 1.5, 'Fitness Tracker': 0.8, 'Camera': 2.5, 'DSLR Camera': 3.0, 'Webcam': 0.7,
        'Microphone': 0.9, 'Gaming Console': 2.8, 'Controller': 0.8, 'VR Headset': 2.0, 'Drone': 2.5,
        'Action Camera': 1.5, 'Projector': 2.0, 'TV': 3.5, 'Streaming Device': 0.6, 'Router': 0.8,
        'Modem': 0.7, 'Network Switch': 0.9, 'External Hard Drive': 0.8, 'SSD': 0.6, 'USB Drive': 0.3,
        'Memory Card': 0.2, 'Power Bank': 0.7, 'Charger': 0.4, 'Cable': 0.2, 'Phone Case': 0.3,
        'Screen Protector': 0.1, 'Laptop Stand': 0.5, 'Cooling Pad': 0.6, 'Docking Station': 0.9,
        'Graphics Card': 2.0, 'Processor': 1.5, 'Motherboard': 1.8, 'RAM': 0.7, 'PSU': 1.2,
        'Computer Case': 1.5, 'CPU Cooler': 0.8, 'Thermal Paste': 0.1, 'LED Strip': 0.3,
        'Gaming Chair': 2.5, 'Desk Lamp': 0.6, 'Surge Protector': 0.5, 'Extension Cord': 0.3,
        'Adapter': 0.2, 'Converter': 0.3, 'KVM Switch': 0.6, 'Drawing Tablet': 1.5, 'E-Reader': 1.0,
        'Smart Home Hub': 0.8, 'Smart Light Bulb': 0.3, 'Smart Plug': 0.2, 'Smart Thermostat': 0.8,
        'Security Camera': 1.0, 'Video Doorbell': 0.9, 'Smart Lock': 0.7, 'Air Purifier': 1.5,
        'Robot Vacuum': 2.0, 'Electric Toothbrush': 0.5, 'Hair Dryer': 0.8, 'Electric Shaver': 0.6,
        'Printer': 1.5, 'Scanner': 1.2, 'Ink Cartridge': 0.4, 'Bluetooth Adapter': 0.2,
        'Wi-Fi Extender': 0.5, 'Portable SSD': 0.6, 'NAS Drive': 1.8, 'USB Hub': 0.3,
        'Card Reader': 0.2, 'Laptop Bag': 1.0, 'Phone Gimbal': 1.2,
        
        # Food & Groceries
        'Local Groceries': 0.3, 'Organic Vegetables': 0.2, 'Organic Fruits': 0.25, 'Fresh Produce': 0.3,
        'Meat': 1.5, 'Poultry': 0.9, 'Seafood': 1.2, 'Dairy Products': 0.6, 'Milk': 0.5, 'Cheese': 0.8,
        'Yogurt': 0.5, 'Butter': 0.7, 'Eggs': 0.4, 'Bread': 0.3, 'Pasta': 0.2, 'Rice': 0.2, 'Cereal': 0.4,
        'Oats': 0.2, 'Granola': 0.3, 'Snacks': 0.5, 'Chips': 0.6, 'Cookies': 0.5, 'Chocolate': 0.8,
        'Candy': 0.5, 'Ice Cream': 0.7, 'Frozen Pizza': 0.6, 'Frozen Vegetables': 0.3, 'Frozen Meals': 0.7,
        'Canned Goods': 0.4, 'Soup': 0.4, 'Sauce': 0.3, 'Condiments': 0.3, 'Spices': 0.2, 'Herbs': 0.1,
        'Oil': 0.4, 'Vinegar': 0.2, 'Honey': 0.3, 'Jam': 0.3, 'Peanut Butter': 0.4, 'Nuts': 0.5,
        'Dried Fruits': 0.4, 'Coffee': 0.6, 'Tea': 0.2, 'Juice': 0.4, 'Soda': 0.5, 'Energy Drink': 0.6,
        'Protein Shake': 0.5, 'Protein Bar': 0.4, 'Vitamins': 0.3, 'Supplements': 0.4, 'Baby Food': 0.4,
        'Pet Food': 0.5, 'Dog Food': 0.6, 'Cat Food': 0.5, 'Treats': 0.3, 'Water Bottles': 0.4,
        'Sparkling Water': 0.4, 'Kombucha': 0.5, 'Plant-based Milk': 0.3, 'Vegan Cheese': 0.4,
        'Tofu': 0.2, 'Tempeh': 0.3, 'Quinoa': 0.3, 'Chia Seeds': 0.2, 'Protein Powder': 0.5,
        'Meal Kit': 0.8, 'Ready-to-Eat Meal': 0.7, 'Salad Kit': 0.4, 'Smoothie Mix': 0.4, 'Baking Mix': 0.3,
        
        # Home & Furniture
        'Home Decor': 1.2, 'Sofa': 4.0, 'Couch': 4.2, 'Chair': 2.0, 'Dining Table': 3.5, 'Coffee Table': 2.5,
        'Desk': 3.0, 'Bed Frame': 3.5, 'Mattress': 3.0, 'Pillow': 0.8, 'Bedding': 1.2, 'Sheets': 1.0,
        'Duvet': 1.5, 'Comforter': 1.6, 'Blanket': 1.2, 'Curtains': 1.0, 'Blinds': 1.2, 'Rug': 1.8,
        'Carpet': 2.5, 'Lamp': 0.9, 'Chandelier': 1.8, 'Mirror': 1.5, 'Picture Frame': 0.5, 'Wall Art': 0.8,
        'Vase': 0.6, 'Candle': 0.3, 'Diffuser': 0.4, 'Storage Box': 0.6, 'Shelf': 1.5, 'Bookshelf': 2.5,
        'Cabinet': 3.0, 'Dresser': 3.2, 'Nightstand': 1.8, 'TV Stand': 2.0, 'Ottoman': 1.5, 'Bean Bag': 1.2,
        'Bar Stool': 1.5, 'Office Chair': 2.5, 'Filing Cabinet': 2.8, 'Organizer': 0.5, 'Basket': 0.4,
        'Plant Pot': 0.5, 'Indoor Plant': 0.3, 'Artificial Plant': 0.6, 'Clock': 0.7, 'Throw Pillow': 0.6,
        'Cushion': 0.6, 'Table Runner': 0.4, 'Placemat': 0.2, 'Kitchenware': 0.8, 'Cookware': 1.2,
        'Pots and Pans': 1.5, 'Bakeware': 0.9, 'Utensils': 0.3, 'Cutlery': 0.5, 'Plates': 0.6, 'Bowls': 0.5,
        'Glasses': 0.4, 'Mugs': 0.4, 'Appliance': 2.0,
        
        # Personal Care & Beauty
        'Cosmetics': 1.5, 'Skincare': 1.3, 'Moisturizer': 1.2, 'Cleanser': 1.0, 'Toner': 0.9, 'Serum': 1.4,
        'Face Mask': 0.8, 'Sunscreen': 1.1, 'Lip Balm': 0.3, 'Lipstick': 0.6, 'Foundation': 1.3,
        'Concealer': 0.8, 'Blush': 0.6, 'Eyeshadow': 0.7, 'Mascara': 0.6, 'Eyeliner': 0.5, 'Brow Pencil': 0.4,
        'Nail Polish': 0.5, 'Perfume': 1.5, 'Cologne': 1.5, 'Deodorant': 0.6, 'Body Lotion': 1.0,
        'Body Wash': 0.8, 'Shampoo': 0.9, 'Conditioner': 0.9, 'Hair Mask': 1.0, 'Hair Oil': 0.8,
        'Styling Product': 0.7, 'Hair Spray': 0.7, 'Hair Gel': 0.6, 'Face Wash': 0.8, 'Acne Treatment': 1.0,
        'Anti-aging Cream': 1.5, 'Eye Cream': 1.2, 'Exfoliator': 0.9, 'Bath Bomb': 0.5, 'Soap': 0.4,
        'Hand Soap': 0.5, 'Hand Cream': 0.6, 'Toothpaste': 0.4, 'Mouthwash': 0.5, 'Dental Floss': 0.2,
        'Razor': 0.5, 'Shaving Cream': 0.6, 'Aftershave': 0.7, 'Makeup Remover': 0.7, 'Cotton Pads': 0.2,
        'Q-tips': 0.1, 'Brush Set': 0.8, 'Sponge': 0.2,
        
        # Books & Media
        'Books (New)': 0.5, 'Books (Used)': 0.05, 'Hardcover Book': 0.7, 'Paperback Book': 0.4,
        'E-book': 0.02, 'Audiobook': 0.03, 'Textbook': 0.9, 'Cookbook': 0.6, 'Magazine': 0.2,
        'Comic Book': 0.3, 'Graphic Novel': 0.5, 'Manga': 0.4, 'Novel': 0.5, 'Non-fiction Book': 0.5,
        'Biography': 0.5, 'Self-help Book': 0.5, "Children's Book": 0.4, 'Young Adult Book': 0.5,
        'Poetry Book': 0.4, 'Art Book': 0.8, 'Photography Book': 0.8, 'Travel Guide': 0.5, 'Dictionary': 0.6,
        'Encyclopedia': 1.0, 'Notebook': 0.3, 'Journal': 0.4, 'Planner': 0.4, 'Calendar': 0.3,
        'Stationery': 0.2, 'Greeting Card': 0.1, 'Postcard': 0.05, 'Bookmark': 0.05, 'DVD': 0.3,
        'Blu-ray': 0.4, 'CD': 0.2, 'Vinyl Record': 0.5, 'Music Album': 0.3, 'Video Game': 0.6,
        'Board Game': 0.8, 'Puzzle': 0.5,
        
        # Sports & Outdoors
        'Yoga Mat': 1.0, 'Dumbbells': 1.5, 'Kettlebell': 1.6, 'Resistance Bands': 0.5, 'Jump Rope': 0.3,
        'Foam Roller': 0.6, 'Exercise Ball': 0.8, 'Treadmill': 4.0, 'Exercise Bike': 3.5, 'Elliptical': 4.2,
        'Weight Bench': 2.5, 'Running Shoes': 2.8, 'Training Shoes': 2.6, 'Sports Jersey': 2.0,
        'Athletic Shorts': 1.8, 'Sports Bra': 1.5, 'Compression Wear': 1.9, 'Water Bottle': 0.5, 'Gym Bag': 1.2,
        'Tent': 3.0, 'Sleeping Bag': 2.5, 'Camping Chair': 1.8, 'Cooler': 2.0, 'Backpack (Hiking)': 2.2,
        'Hiking Boots': 3.0, 'Trekking Poles': 1.0, 'Bicycle': 5.0, 'Bike Helmet': 1.2, 'Skateboard': 1.5,
        'Scooter': 2.0, 'Rollerblades': 2.2, 'Golf Clubs': 3.5, 'Tennis Racket': 1.5, 'Basketball': 0.8,
        'Football': 0.7, 'Soccer Ball': 0.7, 'Baseball Glove': 1.2, 'Fishing Rod': 1.5, 'Kayak': 4.5,
        'Surfboard': 3.5,
        
        # Automotive
        'Car Parts': 2.0, 'Motor Oil': 0.8, 'Brake Pads': 1.2, 'Air Filter': 0.5, 'Spark Plugs': 0.3,
        'Battery': 2.5, 'Wiper Blades': 0.4, 'Headlights': 0.8, 'Tires': 3.5, 'Floor Mats': 1.0,
        'Seat Covers': 1.2, 'Steering Wheel Cover': 0.6, 'Phone Mount': 0.3, 'Dash Cam': 0.9, 'GPS': 0.8,
        'Car Charger': 0.3, 'Air Freshener': 0.2, 'Car Wash Supplies': 0.5, 'Wax': 0.4, 'Polish': 0.4,
        'Vacuum Cleaner (Car)': 1.5, 'Jump Starter': 1.2, 'Tool Kit': 1.5, 'First Aid Kit': 0.5,
        'Emergency Kit': 0.8, 'Roof Rack': 2.0, 'Bike Rack': 1.8, 'Cargo Net': 0.4, 'Sunshade': 0.3,
        'Car Cover': 1.5,
        
        # Restaurants & Dining
        'Restaurant Meal': 0.8, 'Fast Food': 0.9, 'Pizza': 0.7, 'Burger': 1.0, 'Sushi': 0.6,
        'Chinese Food': 0.7, 'Indian Food': 0.6, 'Mexican Food': 0.7, 'Italian Food': 0.7, 'Thai Food': 0.6,
        'Coffee': 0.3, 'Latte': 0.4, 'Cappuccino': 0.4, 'Espresso': 0.3, 'Bubble Tea': 0.5, 'Smoothie': 0.4,
        'Dessert': 0.5, 'Pastry': 0.4, 'Cake': 0.6, 'Ice Cream Cone': 0.4,
        
        # Leather & Accessories
        'Leather Goods': 3.0, 'Leather Jacket': 4.5, 'Leather Bag': 3.5, 'Leather Wallet': 2.0,
        'Leather Belt': 1.8, 'Leather Boots': 3.8, 'Leather Gloves': 2.2, 'Leather Watch Strap': 1.0,
        'Leather Briefcase': 3.8, 'Leather Sofa': 8.0, 'Leather Chair': 5.0, 'Faux Leather Jacket': 2.5,
        'Vegan Leather Bag': 1.8, 'Cork Wallet': 0.6, 'Canvas Bag': 0.8, 'Nylon Backpack': 1.5,
        'Fabric Belt': 0.6, 'Suede Shoes': 3.2, 'Synthetic Boots': 2.5, 'Eco-leather Item': 1.2,
        
        # Second-Hand Items
        'Second-Hand Item': 0.1, 'Thrifted Clothing': 0.08, 'Used Electronics': 0.15, 'Vintage Furniture': 0.12,
        'Refurbished Phone': 0.2, 'Refurbished Laptop': 0.25, 'Used Car': 0.5, 'Used Bike': 0.1,
        'Vintage Jewelry': 0.05, 'Antique': 0.08, 'Collectible': 0.1, 'Used Book': 0.03,
        'Used Appliance': 0.2, 'Upcycled Item': 0.05, 'Repurposed Furniture': 0.08, 'Vintage Clothing': 0.06,
        'Consignment Item': 0.09, 'Estate Sale Find': 0.1, 'Garage Sale Item': 0.07, 'Flea Market Find': 0.09,
        
        # Office & School Supplies
        'Office Supplies': 0.5, 'Pens': 0.2, 'Pencils': 0.15, 'Markers': 0.3, 'Highlighters': 0.25,
        'Eraser': 0.1, 'Correction Tape': 0.15, 'Stapler': 0.4, 'Paper Clips': 0.1, 'Binder Clips': 0.15,
        'Folders': 0.2, 'Binders': 0.4, 'Paper': 0.3, 'Notebook': 0.35, 'Sticky Notes': 0.2, 'Index Cards': 0.15,
        'Calculator': 0.6, 'Tape': 0.2, 'Scissors': 0.3, 'Ruler': 0.2, 'Hole Punch': 0.4, 'Label Maker': 0.8,
        'File Organizer': 0.5, 'Desk Organizer': 0.6, 'Pen Holder': 0.3, 'Whiteboard': 1.5,
        'Markers (Whiteboard)': 0.3, 'Eraser (Whiteboard)': 0.2, 'Bulletin Board': 1.0, 'Push Pins': 0.1,
        
        # Miscellaneous
        'Gift Card': 0.01, 'Subscription Service': 0.05, 'Digital Download': 0.02, 'Online Course': 0.03,
        'Event Ticket': 0.1, 'Movie Ticket': 0.15, 'Concert Ticket': 0.2, 'Sports Ticket': 0.2,
        'Museum Pass': 0.1, 'Membership': 0.05, 'Donation': 0.0, 'Charity Contribution': 0.0,
        'Craft Supplies': 0.6, 'Art Supplies': 0.7, 'Paint': 0.5, 'Brushes': 0.3, 'Canvas': 0.6,
        'Yarn': 0.4, 'Fabric': 0.7, '500+ (Other)': 1.0,
    }
    return multipliers.get(product_type, 1.0)

# ==================== TIPS & CONSTANTS ====================
TIPS_LIST = [
    '🌍 Buying second-hand reduces CO₂ by up to 80% compared to new items!',
    '🌱 Local produce has 5x less carbon footprint than imported goods.',
    '♻️ Repairing items instead of replacing them can save tons of emissions.',
    '🚶‍♀️ Walking or biking to the store? You\\'re already making an impact!',
    '🎒 Bringing your own bag saves about 6kg of CO₂ per year.',
    '💚 Every conscious choice counts - you\\'re doing great!',
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

ECO_FRIENDLY_CATEGORIES = [
    'Second-Hand Item', 'Local Groceries', 'Books (Used)', 'Thrifted Clothing',
    'Used Electronics', 'Vintage Furniture', 'Organic Vegetables', 'Organic Fruits',
    'Refurbished Phone', 'Refurbished Laptop', 'Used Book', 'Upcycled Item',
    'Repurposed Furniture', 'Vintage Clothing', 'Consignment Item'
]

DATA_FILE = Path("shopimpact_data.json")

# ==================== DATA PERSISTENCE ====================
@st.cache_data
def load_data_cached() -> Dict:
    """Load data from JSON file (cached)"""
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return get_default_data()
    return get_default_data()

def save_data(data: Dict) -> None:
    """Save data to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
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
        'settings': {'highContrast': False}
    }

# ==================== SESSION STATE INITIALIZATION ====================
if 'initialized' not in st.session_state:
    data = load_data_cached()
    st.session_state.purchases = data.get('purchases', [])
    st.session_state.user_profile = data.get('user_profile', get_default_data()['user_profile'])
    st.session_state.settings = data.get('settings', {'highContrast': False})
    st.session_state.show_success = False
    st.session_state.success_message = ''
    st.session_state.initialized = True

# ==================== HELPER FUNCTIONS ====================
def add_purchase(product_type: str, brand: str, price: float) -> None:
    """Add a new purchase"""
    co2_impact = price * get_product_multiplier(product_type)
    purchase = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'type': product_type,
        'brand': brand,
        'price': float(price),
        'co2_impact': float(co2_impact)
    }
    st.session_state.purchases.append(purchase)
    save_data({
        'purchases': st.session_state.purchases,
        'user_profile': st.session_state.user_profile,
        'settings': st.session_state.settings
    })
    
    if product_type in ECO_FRIENDLY_CATEGORIES:
        st.session_state.success_message = f"🌟 Eco-friendly choice! You're making a difference!"
        st.balloons()
    else:
        st.session_state.success_message = f"✅ Logged! Your {product_type} added {co2_impact:.1f} kg of CO₂."
    st.session_state.show_success = True

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Modern gradient background */
    .main {
        background: linear-gradient(135deg, #f0fdf4 0%, #dbeafe 50%, #d1fae5 100%);
    }
    
    /* Clean card styles */
    .stCard {
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Modern tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: white;
        border-radius: 12px;
        padding: 6px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
    }
    
    /* Button improvements */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("<h1 style='text-align: center; color: #16a34a;'>🍃 ShopImpact 🍃</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280; font-size: 18px;'>Your friendly guide to conscious shopping — now with 500+ products & brands!</p>", unsafe_allow_html=True)

if st.session_state.user_profile['name']:
    st.markdown(f"<p style='text-align: center; color: #16a34a; font-size: 16px;'>Welcome back, {st.session_state.user_profile['name']}! 🌟</p>", unsafe_allow_html=True)

st.markdown("---")

# ==================== MAIN TAB NAVIGATION ====================
tab1, tab2 = st.tabs(["📊 Dashboard", "👤 Profile"])

# ==================== DASHBOARD TAB ====================
with tab1:
    col_main, col_sidebar = st.columns([2.5, 1])
    
    with col_main:
        # Purchase Form
        st.markdown("### 🛍️ Log a Purchase")
        st.markdown(f"*Choose from {len(PRODUCT_TYPES)} products and {len(ALL_BRANDS)} brands*")
        st.markdown("")
        
        with st.form("purchase_form", clear_on_submit=True):
            # Product Type - Searchable Select
            product_search = st.text_input("🔍 Search Products", placeholder="Type to search...", key="product_search")
            filtered_products = [p for p in PRODUCT_TYPES if product_search.lower() in p.lower()] if product_search else PRODUCT_TYPES
            product_type = st.selectbox(
                f"📦 Product Type ({len(filtered_products)} shown)",
                options=filtered_products,
                help="Search and select a product type"
            )
            
            # Brand - Searchable Select
            brand_search = st.text_input("🔍 Search Brands", placeholder="Type to search or enter custom...", key="brand_search")
            filtered_brands = [b for b in ALL_BRANDS if brand_search.lower() in b.lower()] if brand_search else ALL_BRANDS[:100]
            
            if brand_search and not any(brand_search.lower() == b.lower() for b in filtered_brands):
                st.info(f"✏️ Custom brand: **{brand_search}**")
                final_brand = brand_search
            else:
                selected_brand = st.selectbox(
                    f"🏷️ Brand ({len(filtered_brands)} shown)",
                    options=filtered_brands if filtered_brands else ["Enter custom brand above"],
                    help="Search and select a brand or type custom above",
                    disabled=not filtered_brands
                )
                final_brand = selected_brand if filtered_brands else brand_search
            
            # Price Slider
            price = st.slider(
                "💰 Price (₹)",
                min_value=0,
                max_value=50000,
                value=1000,
                step=100,
                help="Slide to set the price"
            )
            st.markdown(f"<p style='text-align: center; font-size: 24px; color: #16a34a; font-weight: bold;'>₹{price:,}</p>", unsafe_allow_html=True)
            
            # CO2 Estimate
            if price > 0:
                estimated_co2 = price * get_product_multiplier(product_type)
                if product_type in ECO_FRIENDLY_CATEGORIES:
                    st.success(f"✨ **Estimated CO₂ Impact:** {estimated_co2:.1f} kg (Eco-friendly!)")
                elif estimated_co2 > 100:
                    st.warning(f"⚠️ **Estimated CO₂ Impact:** {estimated_co2:.1f} kg (High impact)")
                else:
                    st.info(f"📊 **Estimated CO₂ Impact:** {estimated_co2:.1f} kg")
            
            submit_button = st.form_submit_button("✅ Log Purchase", type="primary", use_container_width=True)
            
            if submit_button:
                if price <= 0:
                    st.error("⚠️ Please set a price greater than 0.")
                elif not final_brand:
                    st.error("⚠️ Please select or enter a brand name.")
                else:
                    add_purchase(product_type, final_brand, price)
                    st.rerun()
        
        # Show success message
        if st.session_state.show_success:
            st.success(st.session_state.success_message)
            st.session_state.show_success = False
        
        st.markdown("---")
        
        # Purchase History
        if st.session_state.purchases:
            st.markdown("### 📈 Your Shopping Dashboard")
            
            df = pd.DataFrame(st.session_state.purchases)
            total_co2 = df['co2_impact'].sum()
            total_spend = df['price'].sum()
            
            # Metrics
            met_col1, met_col2, met_col3, met_col4 = st.columns(4)
            with met_col1:
                st.metric("💰 Total Spend", f"₹{total_spend:,.0f}")
            with met_col2:
                st.metric("🌍 Total CO₂", f"{total_co2:.1f} kg")
            with met_col3:
                st.metric("🛍️ Purchases", len(df))
            with met_col4:
                avg_co2 = total_co2 / len(df)
                st.metric("📈 Avg CO₂", f"{avg_co2:.1f} kg")
            
            # Charts
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                fig_bar = px.bar(
                    df.groupby('type')['co2_impact'].sum().reset_index().sort_values('co2_impact', ascending=False).head(10),
                    x='type',
                    y='co2_impact',
                    title='Top 10 CO₂ by Category',
                    color='co2_impact',
                    color_continuous_scale='Greens'
                )
                fig_bar.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with col_chart2:
                fig_pie = px.pie(
                    df.groupby('type')['price'].sum().reset_index().head(10),
                    values='price',
                    names='type',
                    title='Top 10 Spending Distribution'
                )
                fig_pie.update_layout(height=350)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # Table
            st.markdown("#### 📋 Recent Purchases")
            display_df = df[['date', 'type', 'brand', 'price', 'co2_impact']].tail(20).sort_values('date', ascending=False)
            display_df.columns = ['Date', 'Product', 'Brand', 'Price (₹)', 'CO₂ (kg)']
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Export
            col_exp1, col_exp2 = st.columns(2)
            with col_exp1:
                csv = df.to_csv(index=False)
                st.download_button("📥 Export CSV", csv, file_name="shopimpact_data.csv", mime="text/csv", use_container_width=True)
            with col_exp2:
                if st.button("🔄 Clear All Data", use_container_width=True):
                    st.session_state.purchases = []
                    save_data({
                        'purchases': [],
                        'user_profile': st.session_state.user_profile,
                        'settings': st.session_state.settings
                    })
                    st.rerun()
        else:
            st.info("📝 No purchases logged yet. Start tracking your impact!")
    
    with col_sidebar:
        st.markdown("### 🎯 Quick Stats")
        
        if st.session_state.purchases:
            eco_count = sum(1 for p in st.session_state.purchases if p['type'] in ECO_FRIENDLY_CATEGORIES)
            eco_pct = (eco_count / len(st.session_state.purchases)) * 100 if st.session_state.purchases else 0
            
            st.metric("🌱 Eco Purchases", f"{eco_pct:.0f}%")
            st.progress(eco_pct / 100)
        
        st.markdown("---")
        st.markdown("### 💡 Eco Tip")
        st.info(random.choice(TIPS_LIST))
        
        st.markdown("---")
        st.markdown("### ✨ Motivation")
        st.success(f"*\"{random.choice(MOTIVATIONAL_QUOTES)}\"*")

# ==================== PROFILE TAB ====================
with tab2:
    st.markdown("### 👤 Your Profile")
    
    profile = st.session_state.user_profile
    
    with st.form("profile_form"):
        name = st.text_input("Name", value=profile.get('name', ''))
        age = st.text_input("Age", value=profile.get('age', ''))
        location = st.text_input("Location", value=profile.get('location', ''))
        monthly_budget = st.number_input("Monthly Budget (₹)", min_value=0, value=profile.get('monthlyBudget', 15000), step=1000)
        co2_goal = st.number_input("Monthly CO₂ Goal (kg)", min_value=0, value=profile.get('co2Goal', 50), step=5)
        
        if st.form_submit_button("💾 Save Profile", type="primary"):
            st.session_state.user_profile = {
                'name': name,
                'age': age,
                'location': location,
                'monthlyBudget': monthly_budget,
                'co2Goal': co2_goal,
                'joinDate': profile.get('joinDate', datetime.now().strftime('%Y-%m-%d'))
            }
            save_data({
                'purchases': st.session_state.purchases,
                'user_profile': st.session_state.user_profile,
                'settings': st.session_state.settings
            })
            st.success("✅ Profile updated successfully!")
            st.rerun()
    
    # Display current month stats vs goals
    if st.session_state.purchases:
        st.markdown("---")
        st.markdown("### 📊 This Month vs Your Goals")
        
        current_month_purchases = [
            p for p in st.session_state.purchases
            if datetime.strptime(p['date'], '%Y-%m-%d').month == datetime.now().month
            and datetime.strptime(p['date'], '%Y-%m-%d').year == datetime.now().year
        ]
        
        if current_month_purchases:
            month_spend = sum(p['price'] for p in current_month_purchases)
            month_co2 = sum(p['co2_impact'] for p in current_month_purchases)
            
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.markdown("**💰 Budget**")
                budget_pct = (month_spend / monthly_budget * 100) if monthly_budget > 0 else 0
                st.progress(min(budget_pct / 100, 1.0))
                st.caption(f"₹{month_spend:,.0f} / ₹{monthly_budget:,} ({budget_pct:.0f}%)")
            
            with col_g2:
                st.markdown("**🌍 CO₂**")
                co2_pct = (month_co2 / co2_goal * 100) if co2_goal > 0 else 0
                st.progress(min(co2_pct / 100, 1.0))
                st.caption(f"{month_co2:.1f} / {co2_goal} kg ({co2_pct:.0f}%)")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 14px;'>Made with 💚 for conscious shoppers | Track 500+ products & brands</p>", unsafe_allow_html=True)
