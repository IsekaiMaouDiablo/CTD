import streamlit as st
import json
import os
from datetime import datetime

# ==========================
# 🔧 APP CONFIG
# ==========================
st.set_page_config(
    page_title="Thockaholics", 
    page_icon="⌨️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

CART_FILE = "cart_data.json"
ORDERS_FILE = "orders.json"


# ==========================
# 📦 PRODUCT CATALOG
# ==========================
PRODUCT_CATALOG = {
    "switches": [
        {
            "name": "Gateron Oil King", 
            "price": 7.80, 
            "desc": "Premium linear switches with factory lubrication", 
            "stock": "In Stock", 
            "unit": 10,
            "image": "https://images.unsplash.com/photo-1595225476474-87563907a212?w=400&h=300&fit=crop",
            "specs": {
                "Type": "Linear",
                "Top Housing": "Nylon PA66",
                "Stem": "POM",
                "Bottom Housing": "Nylon PA66",
                "Spring": "22mm, Single staged",
                "Pre-travel": "2.0mm",
                "Actuation Force": "55g",
                "Bottom out": "65g"
            }
        },
        {
            "name": "Cherry MX Red", 
            "price": 5.50, 
            "desc": "Classic linear switches, smooth and reliable", 
            "stock": "In Stock", 
            "unit": 10,
            "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=300&fit=crop",
            "specs": {
                "Type": "Linear",
                "Top Housing": "Nylon",
                "Stem": "POM",
                "Bottom Housing": "Nylon",
                "Spring": "20mm, Single staged",
                "Pre-travel": "2.0mm",
                "Actuation Force": "45g",
                "Bottom out": "60g"
            }
        },
        {
            "name": "Gateron Yellow", 
            "price": 5, 
            "desc": "Budget-friendly linear switches", 
            "stock": "In Stock", 
            "unit": 10,
            "image": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=400&h=300&fit=crop",
            "specs": {
                "Type": "Linear",
                "Top Housing": "Nylon",
                "Stem": "POM",
                "Bottom Housing": "Nylon",
                "Spring": "20mm, Single staged",
                "Pre-travel": "2.0mm",
                "Actuation Force": "50g",
                "Bottom out": "60g"
            }
        },
        {
            "name": "Holy Panda", 
            "price": 10.30, 
            "desc": "Tactile switches with satisfying bump", 
            "stock": "Limited", 
            "unit": 10,
            "image": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=400&h=300&fit=crop",
            "specs": {
                "Type": "Tactile",
                "Top Housing": "Polycarbonate",
                "Stem": "POM",
                "Bottom Housing": "Nylon",
                "Spring": "20mm, Single staged",
                "Pre-travel": "2.0mm",
                "Actuation Force": "67g",
                "Bottom out": "78g"
            }
        },
        {
            "name": "Glorious Panda", 
            "price": 8.50, 
            "desc": "Tactile switches, Holy Panda alternative", 
            "stock": "In Stock", 
            "unit": 10,
            "image": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400&h=300&fit=crop",
            "specs": {
                "Type": "Tactile",
                "Top Housing": "Polycarbonate",
                "Stem": "POM",
                "Bottom Housing": "Nylon PA66",
                "Spring": "20mm, Two staged",
                "Pre-travel": "2.0mm",
                "Actuation Force": "67g",
                "Bottom out": "80g"
            }
        },
        {
            "name": "Cherry MX Brown", 
            "price": 5.50, 
            "desc": "Popular tactile switches", 
            "stock": "In Stock", 
            "unit": 10,
            "image": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=400&h=300&fit=crop",
            "specs": {
                "Type": "Tactile",
                "Top Housing": "Nylon",
                "Stem": "POM",
                "Bottom Housing": "Nylon",
                "Spring": "20mm, Single staged",
                "Pre-travel": "2.0mm",
                "Actuation Force": "45g",
                "Bottom out": "55g"
            }
        },
        {
            "name": "Kailh Box White", 
            "price": 3.50, 
            "desc": "Clicky switches with crisp sound", 
            "stock": "In Stock", 
            "unit": 10,
            "image": "https://images.unsplash.com/photo-1601524909162-ae8725290836?w=400&h=300&fit=crop",
            "specs": {
                "Type": "Clicky",
                "Top Housing": "Polycarbonate",
                "Stem": "POM with Click Bar",
                "Bottom Housing": "Nylon",
                "Spring": "18mm, Single staged",
                "Pre-travel": "1.8mm",
                "Actuation Force": "50g",
                "Bottom out": "60g"
            }
        },
        {
            "name": "Kailh Box Jade", 
            "price": 5.50, 
            "desc": "Heavy clicky switches", 
            "stock": "Limited", 
            "unit": 10,
            "image": "https://images.unsplash.com/photo-1595044426077-d36d9236d54a?w=400&h=300&fit=crop",
            "specs": {
                "Type": "Clicky",
                "Top Housing": "Polycarbonate",
                "Stem": "POM with Click Bar",
                "Bottom Housing": "Nylon",
                "Spring": "18mm, Single staged",
                "Pre-travel": "1.8mm",
                "Actuation Force": "60g",
                "Bottom out": "70g"
            }
        },
    ],
    "prebuilt": [
        {"name": "GMMK Pro", "price": 169, "desc": "75% gasket-mounted keyboard kit", "stock": "In Stock", "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=300&fit=crop"},
        {"name": "Keychron Q1", "price": 149, "desc": "Premium 75% aluminum keyboard", "stock": "In Stock", "image": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=400&h=300&fit=crop"},
        {"name": "Mode Sixty Five", "price": 399, "desc": "High-end 65% keyboard", "stock": "Limited", "image": "https://images.unsplash.com/photo-1595225476474-87563907a212?w=400&h=300&fit=crop"},
        {"name": "Tofu65", "price": 139, "desc": "Popular 65% aluminum case kit", "stock": "In Stock", "image": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=400&h=300&fit=crop"},
        {"name": "NK65 Entry", "price": 95, "desc": "Entry-level 65% hot-swap board", "stock": "In Stock", "image": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=400&h=300&fit=crop"},
    ],
    "keycaps": [
        {"name": "GMK Olivia++", "price": 139, "desc": "Premium ABS keycaps, pink/cream colorway", "stock": "Limited", "image": "https://images.unsplash.com/photo-1607332758123-e3e0b0b6ee30?w=400&h=300&fit=crop"},
        {"name": "PBT Islander", "price": 89, "desc": "Double-shot PBT, tropical theme", "stock": "In Stock", "image": "https://images.unsplash.com/photo-1595044426077-d36d9236d54a?w=400&h=300&fit=crop"},
        {"name": "ePBT Simple JA", "price": 79, "desc": "Minimalist Japanese sublegends", "stock": "In Stock", "image": "https://images.unsplash.com/photo-1560253023-3ec5d502959f?w=400&h=300&fit=crop"},
        {"name": "NicePBT Sugarplum", "price": 69, "desc": "Purple and cream PBT keycaps", "stock": "In Stock", "image": "https://images.unsplash.com/photo-1601524909162-ae8725290836?w=400&h=300&fit=crop"},
        {"name": "Drop + Matt3o MT3", "price": 99, "desc": "High-profile sculpted keycaps", "stock": "In Stock", "image": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400&h=300&fit=crop"},
        {"name": "Akko ASA", "price": 49, "desc": "Budget-friendly ASA profile", "stock": "In Stock", "image": "https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?w=400&h=300&fit=crop"},
    ],
    "accessories": [
        {"name": "Lube Station Kit", "price": 15, "desc": "Professional switch lubing tools", "stock": "In Stock", "image": "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=400&h=300&fit=crop"},
        {"name": "Krytox 205g0", "price": 15, "desc": "Premium switch lubricant, 5ml", "stock": "In Stock", "image": "https://images.unsplash.com/photo-1585839086076-9d991d8f2519?w=400&h=300&fit=crop"},
        {"name": "Switch Puller", "price": 5, "desc": "Aluminum switch removal tool", "stock": "In Stock", "image": "https://images.unsplash.com/photo-1572297794879-e8c6e8e0c7e2?w=400&h=300&fit=crop"},
        {"name": "Keycap Puller", "price": 5, "desc": "Wire keycap removal tool", "stock": "In Stock", "image": "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=400&h=300&fit=crop"},
        {"name": "Coiled Cable", "price": 20, "desc": "Custom aviator USB-C cable", "stock": "Limited", "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop"},
        {"name": "Desk Mat", "price": 25, "desc": "Extended gaming mouse pad", "stock": "In Stock", "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=300&fit=crop"},
        {"name": "Switch Films", "price": 12, "desc": "Reduce wobble, 120 pack", "stock": "In Stock", "image": "https://images.unsplash.com/photo-1565106430482-8f6e74349ca1?w=400&h=300&fit=crop"},
        {"name": "Durock Stabilizers", "price": 22, "desc": "Screw-in stabilizers, set", "stock": "In Stock", "image": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=400&h=300&fit=crop"},
    ]
}


# ==========================
# 🔧 HELPER FUNCTIONS
# ==========================
def get_custom_builder_options():
    """
    Generates custom builder options dynamically from PRODUCT_CATALOG.
    Switches and keycaps prices are derived from the catalog.
    Cases, stabilizers, and plates are unique to custom builds.
    """
    
    # Generate switches for custom builder (70 pieces = 7 units of 10)
    custom_switches = []
    switch_mapping = {
        "Gateron Oil King": "Linear, factory lubed",
        "Cherry MX Red": "Linear, classic feel",
        "Gateron Yellow": "Linear, budget option",
        "Holy Panda": "Tactile, premium feel",
        "Cherry MX Brown": "Tactile, popular choice",
        "Kailh Box White": "Clicky, crisp sound",
    }
    
    for switch in PRODUCT_CATALOG['switches']:
        if switch['name'] in switch_mapping:
            custom_switches.append({
                "name": f"{switch['name']} (x70)",
                "price": round(switch['price'] * 7, 3),
                "desc": switch_mapping[switch['name']],
                "image": switch['image']
            })
    
    # Generate keycaps for custom builder
    custom_keycaps = []
    keycap_mapping = {
        "GMK Olivia++": "ABS, pink/cream theme",
        "PBT Islander": "PBT, tropical colors",
        "ePBT Simple JA": "PBT, minimalist Japanese",
        "NicePBT Sugarplum": "PBT, purple/cream",
        "Drop + Matt3o MT3": "High profile, sculpted",
        "Akko ASA": "Budget ASA profile",
    }
    
    for keycap in PRODUCT_CATALOG['keycaps']:
        if keycap['name'] in keycap_mapping:
            custom_keycaps.append({
                "name": keycap['name'],
                "price": keycap['price'],
                "desc": keycap_mapping[keycap['name']],
                "image": keycap['image']
            })
    
    return {
        "cases": [
            {"name": "Aluminum 60%", "price": 120, "desc": "CNC machined aluminum, 60% layout", "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=300&fit=crop"},
            {"name": "Aluminum 65%", "price": 140, "desc": "CNC machined aluminum, 65% layout", "image": "https://images.unsplash.com/photo-1595225476474-87563907a212?w=400&h=300&fit=crop"},
            {"name": "Aluminum 75%", "price": 160, "desc": "CNC machined aluminum, 75% layout", "image": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=400&h=300&fit=crop"},
            {"name": "Acrylic 60%", "price": 80, "desc": "Frosted acrylic, 60% layout", "image": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=400&h=300&fit=crop"},
            {"name": "Acrylic 65%", "price": 90, "desc": "Frosted acrylic, 65% layout", "image": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=400&h=300&fit=crop"},
            {"name": "Wooden 60%", "price": 150, "desc": "Walnut wood case, 60% layout", "image": "https://images.unsplash.com/photo-1560253023-3ec5d502959f?w=400&h=300&fit=crop"},
            {"name": "Wooden 65%", "price": 170, "desc": "Walnut wood case, 65% layout", "image": "https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?w=400&h=300&fit=crop"},
        ],
        "switches": custom_switches,
        "stabilizers": [
            {"name": "Durock V2", "price": 22, "desc": "Screw-in, premium stabilizers", "image": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=400&h=300&fit=crop"},
            {"name": "Cherry Clip-In", "price": 12, "desc": "PCB mount, reliable", "image": "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=400&h=300&fit=crop"},
            {"name": "C3 Equalz", "price": 28, "desc": "Screw-in, gold-plated", "image": "https://images.unsplash.com/photo-1572297794879-e8c6e8e0c7e2?w=400&h=300&fit=crop"},
            {"name": "TX Stabilizers", "price": 35, "desc": "Premium, minimal rattle", "image": "https://images.unsplash.com/photo-1585839086076-9d991d8f2519?w=400&h=300&fit=crop"},
        ],
        "plates": [
            {"name": "Brass Plate", "price": 40, "desc": "Heavy, deep sound", "image": "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=400&h=300&fit=crop"},
            {"name": "Aluminum Plate", "price": 30, "desc": "Balanced sound and flex", "image": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=400&h=300&fit=crop"},
            {"name": "FR4 Plate", "price": 25, "desc": "Flexible, muted sound", "image": "https://images.unsplash.com/photo-1565106430482-8f6e74349ca1?w=400&h=300&fit=crop"},
            {"name": "Carbon Fiber", "price": 45, "desc": "Stiff, high-pitched sound", "image": "https://images.unsplash.com/photo-1572297794879-e8c6e8e0c7e2?w=400&h=300&fit=crop"},
            {"name": "Polycarbonate", "price": 35, "desc": "Flexible, bouncy feel", "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=300&fit=crop"},
        ],
        "keycaps": custom_keycaps
    }


# ==========================
# 💾 STORAGE FUNCTIONS
# ==========================
def load_json(filename, default=[]):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return default
    return default


def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


# ==========================
# 🧠 SESSION STATE
# ==========================
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "cart" not in st.session_state:
    st.session_state.cart = load_json(CART_FILE)
if "shop_category" not in st.session_state:
    st.session_state.shop_category = "switches"
if "custom_build" not in st.session_state:
    st.session_state.custom_build = {
        "case": None,
        "switches": None,
        "stabilizers": None,
        "plate": None,
        "keycaps": None
    }


# ==========================
# 🎨 CUSTOM STYLES
# ==========================
st.markdown("""
<style>
    .block-container { 
        padding-top: 1rem; 
        max-width: 1400px;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-align: center;
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        text-align: center;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    .badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .badge-default {
        background-color: #667eea;
        color: white;
    }
    
    .badge-secondary {
        background-color: #e0e0e0;
        color: #333;
    }
    
    .badge-destructive {
        background-color: #dc3545;
        color: white;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #667eea;
    }
    
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    /* Add spacing between containers */
    div[data-testid="stVerticalBlock"] > div {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ==========================
# 🧭 NAVIGATION
# ==========================
def render_header():
    st.markdown("""
    <div class="main-header">
        <h1 class="header-title">⌨️ Thockaholics</h1>
        <p class="header-subtitle">Premium Mechanical Keyboards & Accessories</p>
    </div>
    """, unsafe_allow_html=True)
    
    cart_count = len(st.session_state.cart)
    
    # Create navigation buttons
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
    
    with col2:
        if st.button("🛍️ Shop", use_container_width=True):
            st.session_state.page = "Shop"
            st.rerun()
    
    with col3:
        if st.button("🔧 Custom Builder", use_container_width=True):
            st.session_state.page = "Custom Builder"
            st.rerun()
    
    with col4:
        cart_label = f"🛒 Cart ({cart_count})" if cart_count > 0 else "🛒 Cart"
        if st.button(cart_label, use_container_width=True):
            st.session_state.page = "Cart"
            st.rerun()
    
    with col5:
        if st.button("💳 Checkout", use_container_width=True):
            st.session_state.page = "Checkout"
            st.rerun()
    
    with col6:
        if st.button("ℹ️ About", use_container_width=True):
            st.session_state.page = "About"
            st.rerun()
    
    with col7:
        if st.button("📞 Contact", use_container_width=True):
            st.session_state.page = "Contact"
            st.rerun()
    
    st.markdown("---")


# ==========================
# 📄 PAGE: HOME
# ==========================
def home_page():
    st.markdown("### Welcome to Thockaholics! 🎉")
    st.write("Discover premium mechanical keyboards, switches, and accessories crafted for enthusiasts.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Products",
            value="50+",
            delta="Premium items in stock"
        )
    
    with col2:
        st.metric(
            label="Happy Customers",
            value="1,000+",
            delta="5-star reviews"
        )
    
    with col3:
        st.metric(
            label="Fast Shipping",
            value="2-3 Days",
            delta="Average delivery time"
        )
    
    st.markdown("---")
    
    st.markdown("### ✨ Shop by Category")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔘 Switches", key="home_switches", use_container_width=True):
            st.session_state.page = "Shop"
            st.session_state.shop_category = "switches"
            st.rerun()
    
    with col2:
        if st.button("⌨️ Prebuilt Keyboards", key="home_prebuilt", use_container_width=True):
            st.session_state.page = "Shop"
            st.session_state.shop_category = "prebuilt"
            st.rerun()
    
    with col3:
        if st.button("🎨 Keycaps", key="home_keycaps", use_container_width=True):
            st.session_state.page = "Shop"
            st.session_state.shop_category = "keycaps"
            st.rerun()
    
    with col4:
        if st.button("🛠️ Accessories", key="home_accessories", use_container_width=True):
            st.session_state.page = "Shop"
            st.session_state.shop_category = "accessories"
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 🔧 Build Your Dream Keyboard")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("#### Custom Keyboard Builder")
        st.write("Create your perfect keyboard from scratch. Choose your case, switches, plate, stabilizers, and keycaps!")
    with col2:
        st.write("")  # Spacer
        if st.button("Start Building →", key="start_builder", use_container_width=True):
            st.session_state.page = "Custom Builder"
            st.rerun()


# ==========================
# 📄 PAGE: SHOP
# ==========================
def shop_page():
    st.markdown("### 🛍️ Shop")
    
    # Category selector using columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔘 Switches", key="cat_switches", use_container_width=True):
            st.session_state.shop_category = "switches"
            st.rerun()
    
    with col2:
        if st.button("⌨️ Prebuilt Keyboards", key="cat_prebuilt", use_container_width=True):
            st.session_state.shop_category = "prebuilt"
            st.rerun()
    
    with col3:
        if st.button("🎨 Keycaps", key="cat_keycaps", use_container_width=True):
            st.session_state.shop_category = "keycaps"
            st.rerun()
    
    with col4:
        if st.button("🛠️ Accessories", key="cat_accessories", use_container_width=True):
            st.session_state.shop_category = "accessories"
            st.rerun()
    
    st.markdown("---")
    
    # Display products
    products = PRODUCT_CATALOG[st.session_state.shop_category]
    
    # Display in grid layout
    cols_per_row = 2
    for i in range(0, len(products), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(products):
                item = products[i + j]
                idx = i + j
                
                with cols[j]:
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    
                    # Display image
                    if 'image' in item:
                        st.image(item['image'], use_container_width=True)
                    
                    st.markdown(f"### {item['name']}")
                    st.write(item['desc'])
                    
                    # Show detailed specs for switches
                    if st.session_state.shop_category == "switches" and 'specs' in item:
                        with st.expander("📋 View Detailed Specifications"):
                            st.markdown("---")
                            for spec_label, spec_value in item['specs'].items():
                                col_a, col_b = st.columns([1.5, 2])
                                with col_a:
                                    st.markdown(f"**{spec_label}:**")
                                with col_b:
                                    st.markdown(f"`{spec_value}`")
                            st.markdown("---")
                    
                    # Show price with badges
                    if st.session_state.shop_category == "switches":
                        price_text = f"${item['price']}/10 pcs"
                    else:
                        price_text = f"${item['price']}"
                    
                    if item['stock'] == "In Stock":
                        st.markdown(f'<span class="badge badge-default">In Stock</span><span class="badge badge-secondary">{price_text}</span>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<span class="badge badge-destructive">Limited Stock</span><span class="badge badge-secondary">{price_text}</span>', unsafe_allow_html=True)
                    
                    # Add quantity selector for switches
                    if st.session_state.shop_category == "switches":
                        st.markdown("---")
                        quantity = st.number_input(
                            "Units (10 switches/unit)",
                            min_value=1,
                            max_value=20,
                            value=1,
                            step=1,
                            key=f"qty_{st.session_state.shop_category}_{idx}"
                        )
                        total_switches = quantity * 10
                        total_price = quantity * item['price']
                        st.caption(f"Total: {total_switches} switches = ${total_price}")
                    else:
                        quantity = 1
                        total_price = item['price']
                    
                    if st.button("Add to Cart 🛒", key=f"add_btn_{st.session_state.shop_category}_{idx}", use_container_width=True):
                        item_copy = item.copy()
                        item_copy['category'] = st.session_state.shop_category
                        item_copy['quantity'] = quantity
                        item_copy['total_price'] = total_price
                        
                        if st.session_state.shop_category == "switches":
                            item_copy['total_switches'] = quantity * 10
                            item_copy['display_name'] = f"{item['name']} ({quantity * 10} pcs)"
                        
                        st.session_state.cart.append(item_copy)
                        save_json(CART_FILE, st.session_state.cart)
                        st.success(f"✅ Added to cart!")
                        st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)


# ==========================
# 📄 PAGE: CUSTOM BUILDER
# ==========================
def custom_builder_page():
    st.markdown("### 🔧 Custom Keyboard Builder")
    st.write("Build your dream keyboard by selecting each component below.")
    
    CUSTOM_KB_OPTIONS = get_custom_builder_options()
    
    col_main, col_summary = st.columns([2, 1])
    
    with col_main:
        # Case Selection
        st.markdown("#### 1️⃣ Choose Your Case")
        with st.container():
            case_options = [f"{c['name']} - ${c['price']}" for c in CUSTOM_KB_OPTIONS['cases']]
            case_names = [c['name'] for c in CUSTOM_KB_OPTIONS['cases']]
            
            default_case_idx = 0
            if st.session_state.custom_build['case']:
                try:
                    default_case_idx = case_names.index(st.session_state.custom_build['case'])
                except ValueError:
                    pass
            
            selected_case_idx = st.radio(
                "Select a case:",
                range(len(case_options)),
                format_func=lambda x: case_options[x],
                index=default_case_idx,
                key="case_selector"
            )
            st.session_state.custom_build['case'] = case_names[selected_case_idx]
            st.caption(CUSTOM_KB_OPTIONS['cases'][selected_case_idx]['desc'])
        
        st.markdown("---")
        
        # Switches Selection
        st.markdown("#### 2️⃣ Choose Your Switches")
        with st.container():
            switch_options = [f"{s['name']} - ${s['price']}" for s in CUSTOM_KB_OPTIONS['switches']]
            switch_names = [s['name'] for s in CUSTOM_KB_OPTIONS['switches']]
            
            default_switch_idx = 0
            if st.session_state.custom_build['switches']:
                try:
                    default_switch_idx = switch_names.index(st.session_state.custom_build['switches'])
                except ValueError:
                    pass
            
            selected_switch_idx = st.radio(
                "Select switches:",
                range(len(switch_options)),
                format_func=lambda x: switch_options[x],
                index=default_switch_idx,
                key="switches_selector"
            )
            st.session_state.custom_build['switches'] = switch_names[selected_switch_idx]
            st.caption(CUSTOM_KB_OPTIONS['switches'][selected_switch_idx]['desc'])
        
        st.markdown("---")
        
        # Stabilizers Selection
        st.markdown("#### 3️⃣ Choose Your Stabilizers")
        with st.container():
            stab_options = [f"{s['name']} - ${s['price']}" for s in CUSTOM_KB_OPTIONS['stabilizers']]
            stab_names = [s['name'] for s in CUSTOM_KB_OPTIONS['stabilizers']]
            
            default_stab_idx = 0
            if st.session_state.custom_build['stabilizers']:
                try:
                    default_stab_idx = stab_names.index(st.session_state.custom_build['stabilizers'])
                except ValueError:
                    pass
            
            selected_stab_idx = st.radio(
                "Select stabilizers:",
                range(len(stab_options)),
                format_func=lambda x: stab_options[x],
                index=default_stab_idx,
                key="stabs_selector"
            )
            st.session_state.custom_build['stabilizers'] = stab_names[selected_stab_idx]
            st.caption(CUSTOM_KB_OPTIONS['stabilizers'][selected_stab_idx]['desc'])
        
        st.markdown("---")
        
        # Plate Selection
        st.markdown("#### 4️⃣ Choose Your Plate Material")
        with st.container():
            plate_options = [f"{p['name']} - ${p['price']}" for p in CUSTOM_KB_OPTIONS['plates']]
            plate_names = [p['name'] for p in CUSTOM_KB_OPTIONS['plates']]
            
            default_plate_idx = 0
            if st.session_state.custom_build['plate']:
                try:
                    default_plate_idx = plate_names.index(st.session_state.custom_build['plate'])
                except ValueError:
                    pass
            
            selected_plate_idx = st.radio(
                "Select plate:",
                range(len(plate_options)),
                format_func=lambda x: plate_options[x],
                index=default_plate_idx,
                key="plate_selector"
            )
            st.session_state.custom_build['plate'] = plate_names[selected_plate_idx]
            st.caption(CUSTOM_KB_OPTIONS['plates'][selected_plate_idx]['desc'])
        
        st.markdown("---")
        
        # Keycaps Selection
        st.markdown("#### 5️⃣ Choose Your Keycaps")
        with st.container():
            keycap_options = [f"{k['name']} - ${k['price']}" for k in CUSTOM_KB_OPTIONS['keycaps']]
            keycap_names = [k['name'] for k in CUSTOM_KB_OPTIONS['keycaps']]
            
            default_keycap_idx = 0
            if st.session_state.custom_build['keycaps']:
                try:
                    default_keycap_idx = keycap_names.index(st.session_state.custom_build['keycaps'])
                except ValueError:
                    pass
            
            selected_keycap_idx = st.radio(
                "Select keycaps:",
                range(len(keycap_options)),
                format_func=lambda x: keycap_options[x],
                index=default_keycap_idx,
                key="keycaps_selector"
            )
            st.session_state.custom_build['keycaps'] = keycap_names[selected_keycap_idx]
            st.caption(CUSTOM_KB_OPTIONS['keycaps'][selected_keycap_idx]['desc'])
    
    with col_summary:
        st.markdown("### 📦 Build Summary")
        
        with st.container():
            # Calculate total
            total = 0
            
            st.markdown("#### Your Configuration")
            
            if st.session_state.custom_build['case']:
                for c in CUSTOM_KB_OPTIONS['cases']:
                    if c['name'] == st.session_state.custom_build['case']:
                        st.write(f"**Case:** {c['name']}")
                        st.caption(f"${c['price']}")
                        total += c['price']
            
            if st.session_state.custom_build['switches']:
                for s in CUSTOM_KB_OPTIONS['switches']:
                    if s['name'] == st.session_state.custom_build['switches']:
                        st.write(f"**Switches:** {s['name']}")
                        st.caption(f"${s['price']}")
                        total += s['price']
            
            if st.session_state.custom_build['stabilizers']:
                for s in CUSTOM_KB_OPTIONS['stabilizers']:
                    if s['name'] == st.session_state.custom_build['stabilizers']:
                        st.write(f"**Stabilizers:** {s['name']}")
                        st.caption(f"${s['price']}")
                        total += s['price']
            
            if st.session_state.custom_build['plate']:
                for p in CUSTOM_KB_OPTIONS['plates']:
                    if p['name'] == st.session_state.custom_build['plate']:
                        st.write(f"**Plate:** {p['name']}")
                        st.caption(f"${p['price']}")
                        total += p['price']
            
            if st.session_state.custom_build['keycaps']:
                for k in CUSTOM_KB_OPTIONS['keycaps']:
                    if k['name'] == st.session_state.custom_build['keycaps']:
                        st.write(f"**Keycaps:** {k['name']}")
                        st.caption(f"${k['price']}")
                        total += k['price']
            
            st.markdown("---")
            st.markdown(f"### Total: ${total}")
            
            if st.button("🛒 Add to Cart", key="add_custom_build", use_container_width=True):
                custom_item = {
                    "name": "Custom Keyboard Build",
                    "price": total,
                    "desc": "Custom built keyboard",
                    "category": "custom",
                    "components": {
                        "case": st.session_state.custom_build['case'],
                        "switches": st.session_state.custom_build['switches'],
                        "stabilizers": st.session_state.custom_build['stabilizers'],
                        "plate": st.session_state.custom_build['plate'],
                        "keycaps": st.session_state.custom_build['keycaps']
                    }
                }
                st.session_state.cart.append(custom_item)
                save_json(CART_FILE, st.session_state.cart)
                st.success("✅ Custom build added to cart!")
                st.rerun()


# ==========================
# 📄 PAGE: CART
# ==========================
def cart_page():
    st.markdown("### 🛒 Your Shopping Cart")
    
    if st.session_state.cart:
        total = sum(item.get("total_price", item["price"]) for item in st.session_state.cart)
        
        st.write(f"**{len(st.session_state.cart)} item(s) in cart**")
        
        for i, item in enumerate(st.session_state.cart):
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    display_name = item.get('display_name', item['name'])
                    st.markdown(f"**{display_name}**")
                    
                    if 'desc' in item:
                        st.caption(item['desc'])
                    
                    if 'quantity' in item and item.get('category') == 'switches':
                        st.caption(f"Quantity: {item['quantity']} unit(s) × 10 switches = {item.get('total_switches', 0)} switches")
                    
                    if 'components' in item:
                        with st.expander("View Build Details"):
                            for comp_type, comp_name in item['components'].items():
                                st.write(f"• **{comp_type.title()}:** {comp_name}")
                
                with col2:
                    price_to_display = item.get('total_price', item['price'])
                    st.markdown(f"**${price_to_display}**")
                
                with col3:
                    if st.button("Remove ❌", key=f"remove_{i}", use_container_width=True):
                        st.session_state.cart.pop(i)
                        save_json(CART_FILE, st.session_state.cart)
                        st.rerun()
                
                st.markdown("---")
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("🗑️ Clear Cart", key="clear_cart", use_container_width=True):
                st.session_state.cart.clear()
                save_json(CART_FILE, st.session_state.cart)
                st.rerun()
        
        with col2:
            st.markdown(f"### Total: ${total}")
            if st.button("Proceed to Checkout 💳", key="checkout_btn", use_container_width=True):
                st.session_state.page = "Checkout"
                st.rerun()
    
    else:
        st.info("🛒 Your cart is empty. Visit the shop to add items!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Go to Shop 🛍️", key="goto_shop", use_container_width=True):
                st.session_state.page = "Shop"
                st.rerun()
        with col2:
            if st.button("Build Custom Keyboard 🔧", key="goto_builder", use_container_width=True):
                st.session_state.page = "Custom Builder"
                st.rerun()


# ==========================
# 📄 PAGE: CHECKOUT
# ==========================
def checkout_page():
    st.markdown("### 💳 Checkout")
    
    if not st.session_state.cart:
        st.warning("⚠️ Your cart is empty. Add some items first.")
        if st.button("Go to Shop", key="checkout_goto_shop", use_container_width=True):
            st.session_state.page = "Shop"
            st.rerun()
        return
    
    total = sum(item.get("total_price", item["price"]) for item in st.session_state.cart)
    
    with st.container():
        st.markdown("#### 📦 Order Summary")
        for item in st.session_state.cart:
            display_name = item.get('display_name', item['name'])
            price_display = item.get('total_price', item['price'])
            st.write(f"• {display_name} - ${price_display}")
        st.markdown("---")
        st.markdown(f"### Total: ${total}")
    
    st.markdown("---")
    
    st.markdown("#### 📝 Billing Information")
    
    with st.form("checkout_form", clear_on_submit=False):
        name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email Address", placeholder="your.email@example.com")
        address = st.text_area("Shipping Address", placeholder="Street, City, State, ZIP")
        
        payment_method = st.radio(
            "Payment Method",
            ["💳 Credit Card", "🅿️ PayPal", "🏦 Bank Transfer"],
            index=0
        )
        
        st.markdown("---")
        
        confirm = st.form_submit_button("✅ Complete Purchase", use_container_width=True)
        
        if confirm:
            if not all([name, email, address]):
                st.error("⚠️ Please fill in all fields.")
            else:
                order = {
                    "name": name,
                    "email": email,
                    "address": address,
                    "payment_method": payment_method,
                    "items": st.session_state.cart,
                    "total": total,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                orders = load_json(ORDERS_FILE, [])
                orders.append(order)
                save_json(ORDERS_FILE, orders)
                
                st.session_state.cart.clear()
                save_json(CART_FILE, st.session_state.cart)
                
                st.success(f"🎉 Thank you for your purchase, {name}!")
                st.balloons()
                st.info("📧 A confirmation email has been sent (simulated).")


# ==========================
# 📄 PAGE: ABOUT
# ==========================
def about_page():
    st.markdown("### ℹ️ About Thockaholics")
    
    with st.container():
        st.write("""
        We're a collective of mechanical keyboard enthusiasts obsessed with the **thock**. 
        Every product we sell is hand-picked, tested, and community-approved.
        
        Founded in 2020, Thockaholics has grown from a small Discord community to a 
        trusted source for premium mechanical keyboard components and accessories.
        """)
    
    st.markdown("---")
    
    st.markdown("#### 🎯 Our Mission")
    st.write("""
    To provide keyboard enthusiasts with the highest quality components and the 
    knowledge to build their dream setup.
    """)
    
    st.markdown("#### 🌟 Our Values")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<span class="badge badge-default">Quality First</span>', unsafe_allow_html=True)
        st.write("We never compromise on quality")
        st.markdown("")
        
        st.markdown('<span class="badge badge-secondary">Community Driven</span>', unsafe_allow_html=True)
        st.write("Built by enthusiasts, for enthusiasts")
    
    with col2:
        st.markdown('<span class="badge badge-default">Customer Focused</span>', unsafe_allow_html=True)
        st.write("Your satisfaction is our priority")
        st.markdown("")
        
        st.markdown('<span class="badge badge-secondary">Innovation</span>', unsafe_allow_html=True)
        st.write("Always exploring new products")


# ==========================
# 📄 PAGE: CONTACT
# ==========================
def contact_page():
    st.markdown("### 📞 Contact Us")
    st.write("Have questions? We'd love to hear from you!")
    
    with st.form("contact_form", clear_on_submit=True):
        name = st.text_input("Your Name", placeholder="Enter your name")
        email = st.text_input("Your Email", placeholder="your.email@example.com")
        message = st.text_area("Your Message", placeholder="Type your message here...")
        
        submit = st.form_submit_button("📧 Send Message", use_container_width=True)
        
        if submit:
            if name and email and message:
                st.success(f"✅ Thanks, {name}! We'll reach out to {email} soon.")
            else:
                st.error("⚠️ Please fill in all fields.")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown("#### 📧 Email")
            st.write("support@thockaholics.com")
    
    with col2:
        with st.container():
            st.markdown("#### 💬 Discord")
            st.write("discord.gg/thockaholics")
    
    with col3:
        with st.container():
            st.markdown("#### 🕐 Hours")
            st.write("Mon-Fri: 9AM - 6PM")


# ==========================
# 🚀 MAIN APP
# ==========================
def main():
    render_header()
    
    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Shop":
        shop_page()
    elif st.session_state.page == "Custom Builder":
        custom_builder_page()
    elif st.session_state.page == "Cart":
        cart_page()
    elif st.session_state.page == "Checkout":
        checkout_page()
    elif st.session_state.page == "About":
        about_page()
    elif st.session_state.page == "Contact":
        contact_page()
    else:
        st.error("❌ Page not found.")


if __name__ == "__main__":
    main()
