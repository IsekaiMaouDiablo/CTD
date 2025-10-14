import streamlit as st
import streamlit_shadcn_ui as ui
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

# Custom Keyboard Builder Options
CUSTOM_KB_OPTIONS = {
    "cases": [
        {"name": "Aluminum 60%", "price": 120, "desc": "CNC machined aluminum, 60% layout", "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=300&fit=crop"},
        {"name": "Aluminum 65%", "price": 140, "desc": "CNC machined aluminum, 65% layout", "image": "https://images.unsplash.com/photo-1595225476474-87563907a212?w=400&h=300&fit=crop"},
        {"name": "Aluminum 75%", "price": 160, "desc": "CNC machined aluminum, 75% layout", "image": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=400&h=300&fit=crop"},
        {"name": "Acrylic 60%", "price": 80, "desc": "Frosted acrylic, 60% layout", "image": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=400&h=300&fit=crop"},
        {"name": "Acrylic 65%", "price": 90, "desc": "Frosted acrylic, 65% layout", "image": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=400&h=300&fit=crop"},
        {"name": "Wooden 60%", "price": 150, "desc": "Walnut wood case, 60% layout", "image": "https://images.unsplash.com/photo-1560253023-3ec5d502959f?w=400&h=300&fit=crop"},
        {"name": "Wooden 65%", "price": 170, "desc": "Walnut wood case, 65% layout", "image": "https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?w=400&h=300&fit=crop"},
    ],
    "switches": [
        {"name": "Gateron Oil King (x70)", "price": 45, "desc": "Linear, factory lubed", "image": "https://images.unsplash.com/photo-1595225476474-87563907a212?w=400&h=300&fit=crop"},
        {"name": "Cherry MX Red (x70)", "price": 35, "desc": "Linear, classic feel", "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=300&fit=crop"},
        {"name": "Gateron Yellow (x70)", "price": 25, "desc": "Linear, budget option", "image": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=400&h=300&fit=crop"},
        {"name": "Holy Panda (x70)", "price": 65, "desc": "Tactile, premium feel", "image": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=400&h=300&fit=crop"},
        {"name": "Cherry MX Brown (x70)", "price": 40, "desc": "Tactile, popular choice", "image": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=400&h=300&fit=crop"},
        {"name": "Kailh Box White (x70)", "price": 30, "desc": "Clicky, crisp sound", "image": "https://images.unsplash.com/photo-1601524909162-ae8725290836?w=400&h=300&fit=crop"},
    ],
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
    "keycaps": [
        {"name": "GMK Olivia++", "price": 139, "desc": "ABS, pink/cream theme", "image": "https://images.unsplash.com/photo-1607332758123-e3e0b0b6ee30?w=400&h=300&fit=crop"},
        {"name": "PBT Islander", "price": 89, "desc": "PBT, tropical colors", "image": "https://images.unsplash.com/photo-1595044426077-d36d9236d54a?w=400&h=300&fit=crop"},
        {"name": "ePBT Simple JA", "price": 79, "desc": "PBT, minimalist Japanese", "image": "https://images.unsplash.com/photo-1560253023-3ec5d502959f?w=400&h=300&fit=crop"},
        {"name": "NicePBT Sugarplum", "price": 69, "desc": "PBT, purple/cream", "image": "https://images.unsplash.com/photo-1601524909162-ae8725290836?w=400&h=300&fit=crop"},
        {"name": "Drop MT3", "price": 99, "desc": "High profile, sculpted", "image": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400&h=300&fit=crop"},
        {"name": "Akko ASA", "price": 49, "desc": "Budget ASA profile", "image": "https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?w=400&h=300&fit=crop"},
    ]
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
    
    .product-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    
    .switch-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .specs-box {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
        font-size: 0.9rem;
    }
    
    .spec-row {
        display: flex;
        justify-content: space-between;
        padding: 0.3rem 0;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .spec-row:last-child {
        border-bottom: none;
    }
    
    .spec-label {
        font-weight: 600;
        color: #555;
    }
    
    .spec-value {
        color: #667eea;
        font-weight: 500;
    }
    
    .category-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem 0.5rem 0.5rem 0;
    }
    
    .builder-section {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .build-summary {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        position: sticky;
        top: 1rem;
    }
    
    .price-tag {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
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
    cart_label = f"🛒 Cart ({cart_count})" if cart_count > 0 else "🛒 Cart"
    
    selected_tab = ui.tabs(
        options=['🏠 Home', '🛍️ Shop', '🔧 Custom Builder', cart_label, '💳 Checkout', 'ℹ️ About', '📞 Contact'],
        default_value=(
            '🏠 Home' if st.session_state.page == 'Home' else
            '🛍️ Shop' if st.session_state.page == 'Shop' else
            '🔧 Custom Builder' if st.session_state.page == 'Custom Builder' else
            cart_label if st.session_state.page == 'Cart' else
            '💳 Checkout' if st.session_state.page == 'Checkout' else
            'ℹ️ About' if st.session_state.page == 'About' else
            '📞 Contact'
        ),
        key="main_nav"
    )
    
    if selected_tab == '🏠 Home':
        st.session_state.page = "Home"
    elif selected_tab == '🛍️ Shop':
        st.session_state.page = "Shop"
    elif selected_tab == '🔧 Custom Builder':
        st.session_state.page = "Custom Builder"
    elif '🛒 Cart' in selected_tab:
        st.session_state.page = "Cart"
    elif selected_tab == '💳 Checkout':
        st.session_state.page = "Checkout"
    elif selected_tab == 'ℹ️ About':
        st.session_state.page = "About"
    elif selected_tab == '📞 Contact':
        st.session_state.page = "Contact"


# ==========================
# 📄 PAGE: HOME
# ==========================
def home_page():
    st.markdown("### Welcome to Thockaholics! 🎉")
    st.write("Discover premium mechanical keyboards, switches, and accessories crafted for enthusiasts.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ui.metric_card(
            title="Products",
            content="50+",
            description="Premium items in stock",
            key="metric1"
        )
    
    with col2:
        ui.metric_card(
            title="Happy Customers",
            content="1,000+",
            description="5-star reviews",
            key="metric2"
        )
    
    with col3:
        ui.metric_card(
            title="Fast Shipping",
            content="2-3 Days",
            description="Average delivery time",
            key="metric3"
        )
    
    st.markdown("---")
    
    st.markdown("### ✨ Shop by Category")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if ui.button(text="🔘 Switches", key="home_switches", className="w-full"):
            st.session_state.page = "Shop"
            st.session_state.shop_category = "switches"
            st.rerun()
    
    with col2:
        if ui.button(text="⌨️ Prebuilt Keyboards", key="home_prebuilt", className="w-full"):
            st.session_state.page = "Shop"
            st.session_state.shop_category = "prebuilt"
            st.rerun()
    
    with col3:
        if ui.button(text="🎨 Keycaps", key="home_keycaps", className="w-full"):
            st.session_state.page = "Shop"
            st.session_state.shop_category = "keycaps"
            st.rerun()
    
    with col4:
        if ui.button(text="🛠️ Accessories", key="home_accessories", className="w-full"):
            st.session_state.page = "Shop"
            st.session_state.shop_category = "accessories"
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 🔧 Build Your Dream Keyboard")
    with ui.card(key="custom_builder_cta"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("#### Custom Keyboard Builder")
            st.write("Create your perfect keyboard from scratch. Choose your case, switches, plate, stabilizers, and keycaps!")
        with col2:
            if ui.button(text="Start Building →", key="start_builder"):
                st.session_state.page = "Custom Builder"
                st.rerun()


# ==========================
# 📄 PAGE: SHOP
# ==========================
def shop_page():
    st.markdown("### 🛍️ Shop")
    
    # Category selector
    categories = {
        "switches": "🔘 Switches",
        "prebuilt": "⌨️ Prebuilt Keyboards",
        "keycaps": "🎨 Keycaps",
        "accessories": "🛠️ Accessories"
    }
    
    selected_category = ui.tabs(
        options=list(categories.values()),
        default_value=categories[st.session_state.shop_category],
        key="category_tabs"
    )
    
    # Update category based on selection
    for key, value in categories.items():
        if selected_category == value:
            st.session_state.shop_category = key
            break
    
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
                    with ui.card(key=f"product_card_{st.session_state.shop_category}_{idx}"):
                        # Display image for all products that have one
                        if 'image' in item:
                            st.markdown(f'<img src="{item["image"]}" class="switch-image" alt="{item["name"]}">', unsafe_allow_html=True)
                        
                        st.markdown(f"### {item['name']}")
                        st.write(item['desc'])
                        
                        # Show detailed specs for switches
                        if st.session_state.shop_category == "switches" and 'specs' in item:
                            with st.expander("📋 View Detailed Specifications"):
                                # Display specs in a clean, readable format
                                st.markdown("---")
                                for spec_label, spec_value in item['specs'].items():
                                    col1, col2 = st.columns([1.5, 2])
                                    with col1:
                                        st.markdown(f"**{spec_label}:**")
                                    with col2:
                                        st.markdown(f"`{spec_value}`")
                                st.markdown("---")
                        
                        # Show price with unit information for switches
                        if st.session_state.shop_category == "switches":
                            price_text = f"${item['price']}/10 pcs"
                        else:
                            price_text = f"${item['price']}"
                        
                        if item['stock'] == "In Stock":
                            ui.badges(
                                badge_list=[("In Stock", "default"), (price_text, "secondary")],
                                class_name="flex gap-2",
                                key=f"badge_{st.session_state.shop_category}_{idx}"
                            )
                        else:
                            ui.badges(
                                badge_list=[("Limited Stock", "destructive"), (price_text, "secondary")],
                                class_name="flex gap-2",
                                key=f"badge_{st.session_state.shop_category}_{idx}"
                            )
                        
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
                        
                        if ui.button(text="Add to Cart 🛒", key=f"add_btn_{st.session_state.shop_category}_{idx}"):
                            item_copy = item.copy()
                            item_copy['category'] = st.session_state.shop_category
                            item_copy['quantity'] = quantity
                            item_copy['total_price'] = total_price
                            
                            # For switches, add info about total count
                            if st.session_state.shop_category == "switches":
                                item_copy['total_switches'] = quantity * 10
                                item_copy['display_name'] = f"{item['name']} ({quantity * 10} pcs)"
                            
                            st.session_state.cart.append(item_copy)
                            save_json(CART_FILE, st.session_state.cart)
                            st.success(f"✅ Added to cart!")
                            st.rerun()


# ==========================
# 📄 PAGE: CUSTOM BUILDER
# ==========================
def custom_builder_page():
    st.markdown("### 🔧 Custom Keyboard Builder")
    st.write("Build your dream keyboard by selecting each component below.")
    
    col_main, col_summary = st.columns([2, 1])
    
    with col_main:
        # Case Selection
        st.markdown("#### 1️⃣ Choose Your Case")
        with ui.card(key="case_section"):
            case_options = [{"label": f"{c['name']} - ${c['price']}", "value": c['name'], "id": f"case_{i}"} 
                           for i, c in enumerate(CUSTOM_KB_OPTIONS['cases'])]
            
            selected_case = ui.radio_group(
                options=case_options,
                default_value=st.session_state.custom_build['case'] if st.session_state.custom_build['case'] else case_options[0]['value'],
                key="case_selector"
            )
            st.session_state.custom_build['case'] = selected_case
            
            # Show description
            for c in CUSTOM_KB_OPTIONS['cases']:
                if c['name'] == selected_case:
                    st.caption(c['desc'])
        
        st.markdown("---")
        
        # Switches Selection
        st.markdown("#### 2️⃣ Choose Your Switches")
        with ui.card(key="switches_section"):
            switch_options = [{"label": f"{s['name']} - ${s['price']}", "value": s['name'], "id": f"switch_{i}"} 
                             for i, s in enumerate(CUSTOM_KB_OPTIONS['switches'])]
            
            selected_switches = ui.radio_group(
                options=switch_options,
                default_value=st.session_state.custom_build['switches'] if st.session_state.custom_build['switches'] else switch_options[0]['value'],
                key="switches_selector"
            )
            st.session_state.custom_build['switches'] = selected_switches
            
            for s in CUSTOM_KB_OPTIONS['switches']:
                if s['name'] == selected_switches:
                    st.caption(s['desc'])
        
        st.markdown("---")
        
        # Stabilizers Selection
        st.markdown("#### 3️⃣ Choose Your Stabilizers")
        with ui.card(key="stabs_section"):
            stab_options = [{"label": f"{s['name']} - ${s['price']}", "value": s['name'], "id": f"stab_{i}"} 
                           for i, s in enumerate(CUSTOM_KB_OPTIONS['stabilizers'])]
            
            selected_stabs = ui.radio_group(
                options=stab_options,
                default_value=st.session_state.custom_build['stabilizers'] if st.session_state.custom_build['stabilizers'] else stab_options[0]['value'],
                key="stabs_selector"
            )
            st.session_state.custom_build['stabilizers'] = selected_stabs
            
            for s in CUSTOM_KB_OPTIONS['stabilizers']:
                if s['name'] == selected_stabs:
                    st.caption(s['desc'])
        
        st.markdown("---")
        
        # Plate Selection
        st.markdown("#### 4️⃣ Choose Your Plate Material")
        with ui.card(key="plate_section"):
            plate_options = [{"label": f"{p['name']} - ${p['price']}", "value": p['name'], "id": f"plate_{i}"} 
                            for i, p in enumerate(CUSTOM_KB_OPTIONS['plates'])]
            
            selected_plate = ui.radio_group(
                options=plate_options,
                default_value=st.session_state.custom_build['plate'] if st.session_state.custom_build['plate'] else plate_options[0]['value'],
                key="plate_selector"
            )
            st.session_state.custom_build['plate'] = selected_plate
            
            for p in CUSTOM_KB_OPTIONS['plates']:
                if p['name'] == selected_plate:
                    st.caption(p['desc'])
        
        st.markdown("---")
        
        # Keycaps Selection
        st.markdown("#### 5️⃣ Choose Your Keycaps")
        with ui.card(key="keycaps_section"):
            keycap_options = [{"label": f"{k['name']} - ${k['price']}", "value": k['name'], "id": f"keycap_{i}"} 
                             for i, k in enumerate(CUSTOM_KB_OPTIONS['keycaps'])]
            
            selected_keycaps = ui.radio_group(
                options=keycap_options,
                default_value=st.session_state.custom_build['keycaps'] if st.session_state.custom_build['keycaps'] else keycap_options[0]['value'],
                key="keycaps_selector"
            )
            st.session_state.custom_build['keycaps'] = selected_keycaps
            
            for k in CUSTOM_KB_OPTIONS['keycaps']:
                if k['name'] == selected_keycaps:
                    st.caption(k['desc'])
    
    with col_summary:
        st.markdown("### 📦 Build Summary")
        
        with ui.card(key="build_summary"):
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
            
            if ui.button(text="🛒 Add to Cart", key="add_custom_build", className="w-full"):
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
        # Calculate total using total_price if available, otherwise use price
        total = sum(item.get("total_price", item["price"]) for item in st.session_state.cart)
        
        st.write(f"**{len(st.session_state.cart)} item(s) in cart**")
        
        for i, item in enumerate(st.session_state.cart):
            with ui.card(key=f"cart_item_{i}"):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    # Use display_name if available (for switches with quantity)
                    display_name = item.get('display_name', item['name'])
                    st.markdown(f"**{display_name}**")
                    
                    if 'desc' in item:
                        st.caption(item['desc'])
                    
                    # Show quantity info for items with quantity
                    if 'quantity' in item and item.get('category') == 'switches':
                        st.caption(f"Quantity: {item['quantity']} unit(s) × 10 switches = {item.get('total_switches', 0)} switches")
                    
                    # Show custom build components
                    if 'components' in item:
                        with st.expander("View Build Details"):
                            for comp_type, comp_name in item['components'].items():
                                st.write(f"• **{comp_type.title()}:** {comp_name}")
                
                with col2:
                    # Display total_price if available, otherwise price
                    price_to_display = item.get('total_price', item['price'])
                    st.markdown(f"**${price_to_display}**")
                
                with col3:
                    if ui.button(text="Remove ❌", key=f"remove_{i}", variant="destructive"):
                        st.session_state.cart.pop(i)
                        save_json(CART_FILE, st.session_state.cart)
                        st.rerun()
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if ui.button(text="🗑️ Clear Cart", key="clear_cart", variant="outline"):
                st.session_state.cart.clear()
                save_json(CART_FILE, st.session_state.cart)
                st.rerun()
        
        with col2:
            st.markdown(f"### Total: ${total}")
            if ui.button(text="Proceed to Checkout 💳", key="checkout_btn"):
                st.session_state.page = "Checkout"
                st.rerun()
    
    else:
        st.info("🛒 Your cart is empty. Visit the shop to add items!")
        
        col1, col2 = st.columns(2)
        with col1:
            if ui.button(text="Go to Shop 🛍️", key="goto_shop"):
                st.session_state.page = "Shop"
                st.rerun()
        with col2:
            if ui.button(text="Build Custom Keyboard 🔧", key="goto_builder"):
                st.session_state.page = "Custom Builder"
                st.rerun()


# ==========================
# 📄 PAGE: CHECKOUT
# ==========================
def checkout_page():
    st.markdown("### 💳 Checkout")
    
    if not st.session_state.cart:
        st.warning("⚠️ Your cart is empty. Add some items first.")
        if ui.button(text="Go to Shop", key="checkout_goto_shop"):
            st.session_state.page = "Shop"
            st.rerun()
        return
    
    total = sum(item.get("total_price", item["price"]) for item in st.session_state.cart)
    
    with ui.card(key="order_summary"):
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
        name = ui.input(
            default_value="",
            type="text",
            placeholder="Full Name",
            key="checkout_name"
        )
        
        email = ui.input(
            default_value="",
            type="email",
            placeholder="Email Address",
            key="checkout_email"
        )
        
        address = ui.textarea(
            default_value="",
            placeholder="Shipping Address (Street, City, State, ZIP)",
            key="checkout_address"
        )
        
        payment_options = [
            {"label": "💳 Credit Card", "value": "Credit Card", "id": "cc"},
            {"label": "🅿️ PayPal", "value": "PayPal", "id": "pp"},
            {"label": "🏦 Bank Transfer", "value": "Bank Transfer", "id": "bt"}
        ]
        
        payment_method = ui.radio_group(
            options=payment_options,
            default_value="Credit Card",
            key="payment_method"
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
    
    with ui.card(key="about_card"):
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
        ui.badges(badge_list=[("Quality First", "default")], class_name="mb-2", key="value1")
        st.write("We never compromise on quality")
        
        ui.badges(badge_list=[("Community Driven", "secondary")], class_name="mb-2", key="value2")
        st.write("Built by enthusiasts, for enthusiasts")
    
    with col2:
        ui.badges(badge_list=[("Customer Focused", "default")], class_name="mb-2", key="value3")
        st.write("Your satisfaction is our priority")
        
        ui.badges(badge_list=[("Innovation", "secondary")], class_name="mb-2", key="value4")
        st.write("Always exploring new products")


# ==========================
# 📄 PAGE: CONTACT
# ==========================
def contact_page():
    st.markdown("### 📞 Contact Us")
    st.write("Have questions? We'd love to hear from you!")
    
    with st.form("contact_form", clear_on_submit=True):
        name = ui.input(
            default_value="",
            type="text",
            placeholder="Your Name",
            key="contact_name"
        )
        
        email = ui.input(
            default_value="",
            type="email",
            placeholder="Your Email",
            key="contact_email"
        )
        
        message = ui.textarea(
            default_value="",
            placeholder="Your Message",
            key="contact_message"
        )
        
        submit = st.form_submit_button("📧 Send Message", use_container_width=True)
        
        if submit:
            if name and email and message:
                st.success(f"✅ Thanks, {name}! We'll reach out to {email} soon.")
            else:
                st.error("⚠️ Please fill in all fields.")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with ui.card(key="contact_email_card"):
            st.markdown("#### 📧 Email")
            st.write("support@thockaholics.com")
    
    with col2:
        with ui.card(key="contact_discord_card"):
            st.markdown("#### 💬 Discord")
            st.write("discord.gg/thockaholics")
    
    with col3:
        with ui.card(key="contact_hours_card"):
            st.markdown("#### 🕐 Hours")
            st.write("Mon-Fri: 9AM - 6PM EST")


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
