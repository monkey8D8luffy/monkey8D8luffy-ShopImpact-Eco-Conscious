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
        'Desk': 3.0, 'Bed Frame': 3.5, 'Mattress': 3.0, 'Pillow': 0.8, 'Bedding': 1.2, 'Sheet
