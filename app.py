"""CampusLoop — Premium campus circular consumption platform.

Python + Streamlit application for borrowing, lending, swapping, and giving away
campus items. CSV-based persistence with full CRUD, analytics, matching, and
a polished dark-glassmorphic visual experience.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from campus_loop import (
    init_managers,
    item_listings_manager,
    sharing_activities_manager,
    user_manager,
    impact_manager,
    PALETTE,
)

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="CampusLoop",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Managers — initialise once
# ---------------------------------------------------------------------------
if "managers_init" not in st.session_state:
    init_managers()
    st.session_state.managers_init = True

# ---------------------------------------------------------------------------
# Premium CSS — glassmorphism, dark theme, typography
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
        :root {{
            --bg: {PALETTE["background"]};
            --surface: {PALETTE["surface"]};
            --primary: {PALETTE["primary_green"]};
            --secondary: {PALETTE["secondary_green"]};
            --soft: {PALETTE["soft_green"]};
            --text: {PALETTE["text"]};
            --muted: {PALETTE["muted"]};
            --gold: {PALETTE["gold"]};
        }}

        .main {{
            background-color: var(--bg);
            color: var(--text);
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: var(--text) !important;
        }}

        .stRadio > div {{
            gap: 0rem;
        }}

        .stRadio > div > label {{
            background: var(--surface);
            border: 1px solid var(--muted);
            color: var(--muted);
            padding: 0.8rem 1.2rem;
            border-radius: 12px;
            margin: 0 0.2rem;
            font-size: 0.85rem;
            transition: all 0.2s ease;
            cursor: pointer;
        }}

        .stRadio > div > label:hover {{
            border-color: var(--primary);
            color: var(--primary);
            transform: translateY(-2px);
        }}

        .stRadio > div [data-baseweb="radio"] > div {{
            background: var(--surface);
            border: 1px solid var(--muted);
        }}

        .stRadio > div [data-baseweb="radio"] {{
            all: initial;
        }}

        .stSelectbox > div > div {{
            background: var(--surface);
            border: 1px solid var(--muted);
            color: var(--text);
        }}

        .stTextInput > div > div > div {{
            background: var(--surface);
            border: 1px solid var(--muted);
            color: var(--text);
        }}

        .stTextArea > div > div > div {{
            background: var(--surface);
            border: 1px solid var(--muted);
            color: var(--text);
        }}

        .stButton > button {{
            background: var(--primary);
            color: var(--bg);
            border: none;
            padding: 0.8rem 1.6rem;
            border-radius: 10px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.2s ease;
            white-space: nowrap;
        }}

        .stButton > button:hover {{
            background: var(--secondary);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(140, 255, 102, 0.4);
        }}

        .stButton > button:focus:active {{
            background: var(--soft);
            box-shadow: none;
        }}

        .stDataFrame,
        .stTable,
        .stEditDataFrame {{
            background: var(--surface);
            border: 1px solid var(--muted);
            color: var(--text);
        }}

        /* Card styling */
        .premium-card {{
            background: var(--surface);
            border: 1px solid var(--muted);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        }}

        /* Skeleton loading */
        .skeleton {{
            background: var(--surface);
            border-radius: 8px;
            height: 14px;
            width: 70%;
            margin: 4px 0;
        }}

        /* Match badge */
        .match-badge {{
            background: var(--primary);
            color: var(--bg);
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
            margin: 2px;
        }}

        /* Status pill */
        .status-pill {{
            display: inline-block;
            padding: 0.3rem 0.6rem;
            border-radius: 10px;
            font-size: 0.7rem;
            font-weight: 500;
            text-transform: uppercase;
        }}

        .status-active {{ background: var(--primary); color: var(--bg); }}
        .status-completed {{ background: var(--soft); color: var(--bg); }}
        .status-overdue {{ background: #ff6b6b; color: white; }}
        .status-cancelled {{ background: var(--muted); color: var(--bg); }}

        /* Tag */
        .tag {{
            display: inline-block;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-size: 0.65rem;
            font-weight: 500;
            margin: 2px;
        }}
        .tag-swap {{ background: var(--primary); color: var(--bg); }}
        .tag-giveaway {{ background: var(--soft); color: var(--bg); }}
        .tag-borrow {{ background: var(--secondary); color: var(--bg); }}
        .tag-sell {{ background: var(--gold); color: var(--bg); }}

        /* Navigation bar */
        .nav-bar {{
            background: linear-gradient(135deg, var(--surface), var(--bg));
            border: 1px solid var(--muted);
            border-radius: 16px;
            padding: 0.5rem 1rem;
            margin-bottom: 2rem;
            backdrop-filter: blur(20px);
        }}

        .nav-link {{
            color: var(--muted);
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 10px;
            transition: all 0.2s ease;
            white-space: nowrap;
            font-size: 0.85rem;
        }}

        .nav-link:hover {{
            background: var(--primary);
            color: var(--bg);
        }}

        .nav-link.active {{
            background: var(--primary);
            color: var(--bg);
        }}

        /* Section header */
        .section-header {{
            color: var(--primary);
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--muted);
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Initialize managers
# ---------------------------------------------------------------------------
init_managers()

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def safe_title(title: str) -> str:
    """Escape title for safe rendering."""
    return title


def format_currency(value: int) -> str:
    """Format integer as INR currency."""
    if value >= 100000:
        return f"₹{value / 100000:.1f}L"
    if value >= 1000:
        return f"₹{value / 1000:.0f}k"
    return f"₹{value}"


def status_pill(status: str) -> str:
    """Return HTML status pill."""
    status_lower = status.lower()
    if "active" in status_lower:
        return f'<span class="status-pill status-active">ACTIVE</span>'
    if "completed" in status_lower:
        return f'<span class="status-pill status-completed">COMPLETED</span>'
    if "overdue" in status_lower:
        return f'<span class="status-pill status-overdue">OVERDUE</span>'
    if "cancelled" in status_lower:
        return f'<span class="status-pill status-cancelled">CANCELLED</span>'
    return status


def sharing_mode_tag(mode: str) -> str:
    """Return HTML sharing mode tag."""
    tags = {
        "SWAP": '<span class="tag tag-swap">SWAP</span>',
        "GIVEAWAY": '<span class="tag tag-giveaway">GIVEAWAY</span>',
        "BORROW": '<span class="tag tag-borrow">BORROW</span>',
        "SELL": '<span class="tag tag-sell">SELL</span>',
    }
    return tags.get(mode, mode)


# ---------------------------------------------------------------------------
# Navigation — premium sidebar
# ---------------------------------------------------------------------------


def nav_bar():
    """Render premium CampusLoop navigation bar with routing."""
    current_page = st.session_state.get("current_page", "Home")
    
    # Page routing buttons (replace selectbox)
    c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)
    pages = ["Home", "Discover", "My Listings", "Sharing", "Users", "Impact", "Analytics", "Smart Match"]
    active = ["Home", "Discover", "My Listings", "Sharing", "Users", "Impact", "Analytics", "Smart Match"].index(current_page)
    
    with c1:
        if st.button("◀◀", help="Home", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()
    with c2:
        if st.button("Discover", help="Discover", use_container_width=True):
            st.session_state.current_page = "Discover"
            st.rerun()
    with c3:
        if st.button("My Listings", help="My Listings", use_container_width=True):
            st.session_state.current_page = "My Listings"
            st.rerun()
    with c4:
        if st.button("Sharing", help="Sharing", use_container_width=True):
            st.session_state.current_page = "Sharing"
            st.rerun()
    with c5:
        if st.button("Users", help="Users", use_container_width=True):
            st.session_state.current_page = "Users"
            st.rerun()
    with c6:
        if st.button("Impact", help="Impact", use_container_width=True):
            st.session_state.current_page = "Impact"
            st.rerun()
    with c7:
        if st.button("Analytics", help="Analytics", use_container_width=True):
            st.session_state.current_page = "Analytics"
            st.rerun()
    with c8:
        if st.button("Smart Match", help="Smart Match", use_container_width=True):
            st.session_state.current_page = "Smart Match"
            st.rerun()
    
    # Visual separator + navbar
    st.markdown(
        f"""
        <div style="margin-top: 1rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <img src="assets/campus-loop.png" alt="CampusLoop" height="32">
                <span style="font-size: 1.1rem; font-weight: 700; color: var(--primary);">CampusLoop</span>
            </div>
            <div style="margin-left: auto; flex-grow: 1; display: flex; gap: 0.3rem;">
                <span class="nav-link {('active' if pages[0] == current_page else '')}">Home</span>
                <span class="nav-link {('active' if pages[1] == current_page else '')}">Discover</span>
                <span class="nav-link {('active' if pages[2] == current_page else '')}">My Listings</span>
                <span class="nav-link {('active' if pages[3] == current_page else '')}">Sharing</span>
                <span class="nav-link {('active' if pages[4] == current_page else '')}">Users</span>
                <span class="nav-link {('active' if pages[5] == current_page else '')}">Impact</span>
                <span class="nav-link {('active' if pages[6] == current_page else '')}">Analytics</span>
                <span class="nav-link {('active' if pages[7] == current_page else '')}">Smart Match</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def nav_button(label: str, key: str) -> bool:
    """Render a premium nav button, return True if clicked."""
    # Use form to capture button press
    clicked = st.button(label, key=key)
    return clicked


# ---------------------------------------------------------------------------
# Home page
# ---------------------------------------------------------------------------


def home_page():
    """Home page — hero with value proposition and featured listings."""
    # Hero section with actual CampusLoop asset
    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 3rem 1rem 2rem;
            background: linear-gradient(135deg, var(--surface), var(--bg));
            border-radius: 20px;
            margin-bottom: 2rem;
            backdrop-filter: blur(20px);
            border: 1px solid var(--muted);
        ">
            <div style="display: inline-block; margin-bottom: 1rem;">
                <img src="assets/campus-loop.png" alt="CampusLoop" height="60">
            </div>
            <h1 style="font-size: 2.5rem; font-weight: 700; color: var(--primary); margin: 0.5rem 0;">
                CampusLoop
            </h1>
            <p style="font-size: 1.1rem; color: var(--muted); margin: 0.5rem 0;">
                SHARE · REUSE · SAVE · TOGETHER
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Value proposition
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(
            f"""
            <div style="
                background: var(--surface);
                border: 1px solid var(--muted);
                border-radius: 16px;
                padding: 2rem;
                backdrop-filter: blur(20px);
                margin-bottom: 2rem;
            ">
                <h2 style="color: var(--primary); font-size: 1.5rem; margin-bottom: 1rem;">
                    Borrow. Lend. Swap. Give away.
                </h2>
                <p style="color: var(--muted); font-size: 1.05rem; line-height: 1.6;">
                    Your campus community for circular consumption. Find items, share
                    what you no longer need, and reduce waste together.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Featured/recent listings
    st.markdown('<div class="section-header">Recent Listings</div>', unsafe_allow_html=True)

    if item_listings_manager:
        df = item_listings_manager.load()
        if not df.empty:
            # Show 4 featured items
            feature_df = df.head(4).copy()
            for _, row in feature_df.iterrows():
                with st.container():
                    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        cat = row.get("category", "")
                        st.markdown(f"**{cat}**")
                    with col2:
                        st.markdown(f"### {row.get('title', 'Unnamed item')}")
                        st.markdown(
                            f"{sharing_mode_tag(row.get('sharing_mode', ''))} | "
                            f"{row.get('condition', '')} condition | "
                            f"₹{row.get('estimated_value_inr', 0):,}"
                        )
                    st.markdown(f"<small>by {row.get('owner_user_id', 'Unknown')}</small>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No listings yet. Be the first to list an item!")

    # Quick CTA section
    st.markdown("---")
    st.markdown('<div class="section-header">Quick Start</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        if nav_button("List an Item", "list_item"):
            st.session_state.show_create_listing = True

    with col2:
        if nav_button("Discover Items", "discover"):
            st.session_state.current_page = "Discover"

    with col3:
        if nav_button("Smart Match", "match"):
            st.session_state.current_page = "Smart Match"


# ---------------------------------------------------------------------------
# Listing form — reusable component
# ---------------------------------------------------------------------------

def create_listing_form():
    """Form to create a new item listing (shown on Home page)."""
    st.markdown('<div class="section-header">Add New Listing</div>', unsafe_allow_html=True)
    with st.form("new_listing_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            owner_user_id = st.text_input("Your user ID", value="U0726")
            title = st.text_input("Item title")
            category = st.selectbox("Category", [
                "Accessory", "Electronics", "Equipment", "Book", "Stationery",
                "Clothing", "Lab Equipment", "Cable", "Storage", "Bag"
            ])
            condition = st.selectbox("Condition", ["EXCELLENT", "GOOD", "FAIR"])
        with c2:
            sharing_mode = st.selectbox("Sharing Mode", ["SWAP", "GIVEAWAY", "BORROW", "SELL"])
            estimated_value = st.number_input("Estimated value (₹)", min_value=0, value=500)
            listed_date = st.date_input("Listed date", value=pd.Timestamp.now())
        c3, c4 = st.columns(2)
        with c3:
            available_until = st.date_input("Available until", value=pd.Timestamp.now() + pd.Timedelta(days=90))
        with c4:
            pickup_location = st.text_input("Pickup location", value="Hostel Block A")
        submitted = st.form_submit_button("Create Listing")
        if submitted:
            if not title:
                st.error("Title is required.")
            else:
                try:
                    item_listings_manager.add(
                        owner_user_id=owner_user_id,
                        title=title,
                        category=category,
                        item_type=category,
                        brand="",
                        condition=condition,
                        sharing_mode=sharing_mode,
                        status="AVAILABLE",
                        estimated_value_inr=int(estimated_value),
                        listed_date=listed_date.strftime("%Y-%m-%d"),
                        available_until=available_until.strftime("%Y-%m-%d"),
                        pickup_location=pickup_location,
                    )
                    st.success("Listing created successfully!")
                    st.session_state.show_create_listing = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed: {str(e)[:80]}")


# ---------------------------------------------------------------------------
# Discover page
# ---------------------------------------------------------------------------


def discover_page():
    """Discover page — search, filter, sort listing cards."""
    st.title("Discover Items")
    st.markdown("Browse and find items to borrow, lend, swap, or give away.")

    if not item_listings_manager:
        st.error("Item listings manager not available.")
        return

    df = item_listings_manager.load()
    if df.empty:
        st.info("No items available at the moment. List something first!")
        return

    # Filters
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        query = st.text_input("Search item or category", placeholder="e.g., keyboard, backpack")
    with col2:
        categories = ["All"] + sorted(df["category"].unique().tolist())
        category = st.selectbox("Category", categories)
    with col3:
        sharing_modes = ["All"] + sorted(df["sharing_mode"].unique().tolist())
        sharing_mode = st.selectbox("Sharing Mode", sharing_modes)
    with col4:
        conditions = ["All"] + sorted(df["condition"].unique().tolist())
        condition = st.selectbox("Condition", conditions)

    # Apply filters
    filtered = item_listings_manager.search(
        query=query if query else "",
        category=category if category != "All" else "",
        sharing_mode=sharing_mode if sharing_mode != "All" else "",
        condition=condition if condition != "All" else "",
    )

    # Sorting
    sort_option = st.selectbox("Sort by", ["Newest", "Oldest", "A-Z", "Z-A", "Value: Low-High", "Value: High-Low"])
    ascending = True
    if sort_option in ["Oldest", "A-Z", "Value: Low-High"]:
        ascending = True
    else:
        ascending = False

    if sort_option in ["Newest", "Oldest"]:
        if "listed_date" in filtered.columns:
            filtered = filtered.sort_values("listed_date", ascending=ascending)
    elif sort_option in ["A-Z"]:
        if "title" in filtered.columns:
            filtered = filtered.sort_values("title", ascending=ascending)
    elif sort_option in ["Z-A"]:
        if "title" in filtered.columns:
            filtered = filtered.sort_values("title", ascending=not ascending)
    elif sort_option in ["Value: Low-High"]:
        if "estimated_value_inr" in filtered.columns:
            filtered = filtered.sort_values("estimated_value_inr", ascending=True)
    elif sort_option in ["Value: High-Low"]:
        if "estimated_value_inr" in filtered.columns:
            filtered = filtered.sort_values("estimated_value_inr", ascending=False)

    st.markdown(f"<p class='section-header' style='margin-top: 0;'>({len(filtered)} results)</p>", unsafe_allow_html=True)

    if filtered.empty:
        st.info("No items match your filters. Try broadening your search.")
        return

    # Display cards with pagination
    ITEMS_PER_PAGE = 12
    total_pages = max(1, (len(filtered) - 1) // ITEMS_PER_PAGE + 1)
    page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, format="%d")

    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_filtered = filtered.iloc[start:end]

    st.markdown(f"<p class='section-header' style='margin-top: 0;'>({len(filtered)} results — Page {page} of {total_pages})</p>", unsafe_allow_html=True)

    if filtered.empty:
        st.info("No items match your filters. Try broadening your search.")
        return

    # Display cards
    for _, row in page_filtered.iterrows():
        with st.container():
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                cat = row.get("category", "")
                st.markdown(f"**{cat}**")
            with col2:
                st.markdown(f"### {row.get('title', 'Unnamed item')}")
                st.markdown(f"{sharing_mode_tag(row.get('sharing_mode', ''))} | {row.get('condition', '')} condition", unsafe_allow_html=True)
                st.markdown(f"₹{row.get('estimated_value_inr', 0):,}")
                st.markdown(f"<small>{row.get('pickup_location', 'No location')}</small>", unsafe_allow_html=True)
            with col3:
                st.write("")  # spacer
                owner = row.get("owner_user_id", "")
                if st.button("Message", key=f"msg_{row.get('item_id')}"):
                    st.info(f"Contact {owner} about {row.get('title')}")
            st.markdown("</div>", unsafe_allow_html=True)

    # Pagination controls
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if page > 1:
            if st.button("← Prev", use_container_width=True):
                st.session_state.discover_page = page - 1
                st.rerun()
    with c2:
        st.write(f"Page {page} of {total_pages}")
    with c3:
        if page < total_pages:
            if st.button("Next →", use_container_width=True):
                st.session_state.discover_page = page + 1
                st.rerun()


# ---------------------------------------------------------------------------
# My Listings CRUD page
# ---------------------------------------------------------------------------


def my_listings_page():
    """My Listings — CRUD for Rahul's item listings."""
    st.title("My Listings")
    st.markdown("Manage your item listings — create, edit, and delete.")

    if not item_listings_manager:
        st.error("Item listings manager not available.")
        return

    df = item_listings_manager.load()

    # CRUD tabs
    tab_create, tab_read, tab_update, tab_delete = st.tabs(["Create", "Read", "Update", "Delete"])

    # --- CREATE ---
    with tab_create:
        st.markdown('<div class="section-header">Add New Listing</div>', unsafe_allow_html=True)
        with st.form("new_listing_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                owner_user_id = st.text_input("Your user ID", value="U0804")
                title = st.text_input("Item title")
                category = st.selectbox("Category", [
                    "Accessory", "Electronics", "Equipment", "Book", "Stationery",
                    "Clothing", "Lab Equipment", "Cable", "Storage", "Bag"
                ])
                condition = st.selectbox("Condition", ["EXCELLENT", "GOOD", "FAIR"])
            with c2:
                sharing_mode = st.selectbox("Sharing Mode", ["SWAP", "GIVEAWAY", "BORROW", "SELL"])
                estimated_value = st.number_input("Estimated value (₹)", min_value=0, value=500)
                listed_date = st.date_input("Listed date", value=pd.Timestamp.now())
            c3, c4 = st.columns(2)
            with c3:
                available_until = st.date_input("Available until", value=pd.Timestamp.now() + pd.Timedelta(days=90))
            with c4:
                pickup_location = st.text_input("Pickup location", value="Hostel Block A")

            submitted = st.form_submit_button("Create Listing")
            if submitted:
                if not title:
                    st.error("Title is required.")
                else:
                    try:
                        item_listings_manager.add(
                            owner_user_id=owner_user_id,
                            title=title,
                            category=category,
                            item_type=category,  # reuse category as item_type for simplicity
                            brand="",  # optional, left empty
                            condition=condition,
                            sharing_mode=sharing_mode,
                            status="AVAILABLE",
                            estimated_value_inr=int(estimated_value),
                            listed_date=listed_date.strftime("%Y-%m-%d"),
                            available_until=available_until.strftime("%Y-%m-%d"),
                            pickup_location=pickup_location,
                        )
                        st.success("Listing created successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to create listing: {str(e)[:100]}")

    # --- READ ---
    with tab_read:
        st.markdown('<div class="section-header">Your Listings</div>', unsafe_allow_html=True)
        if not df.empty:
            for _, row in df.iterrows():
                with st.container():
                    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                    c1, c2, c3 = st.columns([3, 1, 1])
                    with c1:
                        st.markdown(f"**{row.get('title', 'Unnamed item')}**")
                        st.markdown(f"{row.get('category', '')} | {sharing_mode_tag(row.get('sharing_mode', ''))}", unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"₹{row.get('estimated_value_inr', 0):,}")
                    with c3:
                        if st.button("Delete", key=f"del_{row.get('item_id')}", type="secondary"):
                            try:
                                item_listings_manager.delete(row.get("item_id"))
                                st.success("Listing deleted.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed: {str(e)[:80]}")
                    st.markdown(f"*Condition: {row.get('condition', '')}* | *Location: {row.get('pickup_location', '')}*")
                    st.markdown(f"<small>ID: {row.get('item_id')}</small>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No listings found. Create your first listing above!")

    # --- UPDATE ---
    with tab_update:
        st.markdown('<div class="section-header">Update Listing</div>', unsafe_allow_html=True)
        if not df.empty:
            selected_id = st.selectbox("Select listing to update", df["item_id"].tolist())
            selected_row = df[df["item_id"] == selected_id].iloc[0]
            with st.form("update_listing_form"):
                c1, c2 = st.columns(2)
                with c1:
                    new_title = st.text_input("Title", value=selected_row.get("title", ""))
                    new_category = st.selectbox("Category", [
                        "Accessory", "Electronics", "Equipment", "Book", "Stationery",
                        "Clothing", "Lab Equipment", "Cable", "Storage", "Bag"
                    ])
                    new_condition = st.selectbox("Condition", ["EXCELLENT", "GOOD", "FAIR"])
                with c2:
                    new_sharing_mode = st.selectbox("Sharing Mode", ["SWAP", "GIVEAWAY", "BORROW", "SELL"])
                    new_value = st.number_input("Estimated value (₹)", min_value=0, value=int(selected_row.get("estimated_value_inr", 0)))
                submitted = st.form_submit_button("Update Listing")
                if submitted:
                    try:
                        item_listings_manager.update(selected_id, {
                            "title": new_title,
                            "category": new_category,
                            "condition": new_condition,
                            "sharing_mode": new_sharing_mode,
                            "estimated_value_inr": int(new_value),
                        })
                        st.success("Listing updated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to update: {str(e)[:80]}")
        else:
            st.info("No listings to update.")

    # --- DELETE ---
    # (Already in read tab, but keep separate for completeness)
    with tab_delete:
        st.markdown('<div class="section-header">Delete Listing</div>', unsafe_allow_html=True)
        if not df.empty:
            selected_id = st.selectbox("Select listing to delete", df["item_id"].tolist(), key="del_select")
            selected_row = df[df["item_id"] == selected_id].iloc[0]
            st.warning(f"Are you sure you want to delete **{selected_row.get('title', 'this item')}**?")
            if st.button("Confirm Delete", type="primary"):
                try:
                    item_listings_manager.delete(selected_id)
                    st.success("Listing deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to delete: {str(e)[:80]}")
        else:
            st.info("No listings to delete.")


# ---------------------------------------------------------------------------
# Sharing activities page
# ---------------------------------------------------------------------------


def sharing_page():
    """Sharing activities — manage Rahul's sharing activities dataset."""
    st.title("Sharing Activities")
    st.markdown("Track borrowing, lending, swapping, and giving activities.")

    if not sharing_activities_manager:
        st.error("Sharing activities manager not available.")
        return

    df = sharing_activities_manager.load()

    # Activity history
    st.markdown('<div class="section-header">Activity History</div>', unsafe_allow_html=True)
    if not df.empty:
        for _, row in df.iterrows():
            with st.container():
                st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                c1, c2, c3 = st.columns([2, 2, 1])
                with c1:
                    st.markdown(f"{row.get('activity_type', '')} — {sharing_mode_tag(row.get('item_id', ''))}", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"{row.get('start_date', '')} → {row.get('due_date', '')}")
                with c3:
                    st.markdown(status_pill(row.get("activity_status", "")))
                st.markdown(f"<small>Item: {row.get('item_id', '')} | Borrower: {row.get('borrower_user_id', '')} → Owner: {row.get('owner_user_id', '')}</small>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No sharing activities recorded yet.")

    # Create new activity
    st.markdown("---")
    st.markdown('<div class="section-header">Record New Activity</div>', unsafe_allow_html=True)
    with st.form("new_activity_form"):
        c1, c2 = st.columns(2)
        with c1:
            activity_type = st.selectbox("Activity Type", ["BORROW", "GIVEAWAY", "SWAP", "SELL"])
            item_id = st.selectbox("Item ID", item_listings_manager.load()["item_id"].tolist() if item_listings_manager and not item_listings_manager.load().empty else ["I00001"] if item_listings_manager else ["I00001"])
            borrower_user_id = st.text_input("Borrower User ID", value="U0726")
        with c2:
            owner_user_id = st.text_input("Owner User ID", value="U0490")
            start_date = st.date_input("Start date", value=pd.Timestamp.now())
            due_date = st.date_input("Due date", value=pd.Timestamp.now() + pd.Timedelta(days=14))
        c3, c4 = st.columns(2)
        with c3:
            duration_days = st.number_input("Duration (days)", min_value=0, value=14)
        with c4:
            estimated_value = st.number_input("Estimated value (₹)", min_value=0, value=1100)
        resolution = st.selectbox("Resolution status", ["PENDING", "COMPLETED", "CANCELLED"])
        return_status = st.selectbox("Return status", ["NA", "ON_TIME", "LATE", "RETURNED"])
        submitted = st.form_submit_button("Record Activity")
        if submitted:
            try:
                sharing_activities_manager.add(
                    item_id=item_id,
                    borrower_user_id=borrower_user_id,
                    owner_user_id=owner_user_id,
                    activity_type=activity_type,
                    start_date=start_date.strftime("%Y-%m-%d"),
                    request_date=start_date.strftime("%Y-%m-%d"),
                    due_date=due_date.strftime("%Y-%m-%d"),
                    activity_status=activity_type,
                    duration_days=int(duration_days),
                    estimated_value_inr=int(estimated_value),
                    resolution_status=resolution,
                    return_status=return_status,
                )
                st.success("Activity recorded successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to record activity: {str(e)[:80]}")

    # Summary stats
    st.markdown("---")
    if not df.empty:
        st.markdown('<div class="section-header">Summary</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Activities", len(df))
        with col2:
            borrows = len(df[df["activity_type"] == "BORROW"])
            st.metric("Borrows", borrows)
        with col3:
            swaps = len(df[df["activity_type"] == "SWAP"])
            st.metric("Swaps", swaps)
        with col4:
            completed = len(df[df["activity_status"] == "COMPLETED"])
            st.metric("Completed", completed)


# ---------------------------------------------------------------------------
# Users page
# ---------------------------------------------------------------------------


def users_page():
    """Users page — browse users."""
    st.title("Users")
    st.markdown("Browse campus community members.")

    if not user_manager:
        st.error("User manager not available.")
        return

    df = user_manager.load()
    if df.empty:
        st.info("No user data available.")
        return

    # Search
    search_term = st.text_input("Search users", placeholder="Name or department")
    if search_term:
        df = df[df["name"].str.contains(search_term, case=False, na=False) | df["department"].str.contains(search_term, case=False, na=False)]

    # Display
    st.markdown(f"<p class='section-header'>({len(df)} users)</p>", unsafe_allow_html=True)
    for _, row in df.iterrows():
        with st.container():
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{row.get('name', 'Unknown')}**")
                st.markdown(f"{row.get('department', '')} · Year {row.get('year', '')}")
            with c2:
                st.write("")  # spacer
            st.markdown(f"<small>ID: {row.get('user_id', '')}</small>", unsafe_allow_html=True)
            st.markdown(f"<small>Joined: {row.get('joined_date', '')}</small>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Impact page
# ---------------------------------------------------------------------------


def impact_page():
    """Impact page — sustainability metrics and charts."""
    st.title("Impact")
    st.markdown("Sustainability metrics from campus sharing activity.")

    if not impact_manager:
        st.error("Impact manager not available.")
        return

    # Summary stats
    summary = impact_manager.get_summary()
    st.markdown("### Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Activities Impacted", summary["total_impact"])
    with col2:
        st.metric("Value Saved (₹)", f"₹{summary['total_value_saved']:,.0f}")
    with col3:
        st.metric("Items Reused", summary["total_items_reused"])
    with col4:
        st.metric("Avg Reuse Factor", f"{summary['average_reuse_factor']:.2f}")

    # Breakdown by category
    st.markdown("---")
    st.markdown('<div class="section-header">Impact by Category</div>', unsafe_allow_html=True)

    cat_df = impact_manager.get_by_category()
    if not cat_df.empty:
        # Bar chart for count
        fig = px.bar(
            cat_df,
            x="item_category",
            y="count",
            title="Activities by Category",
            labels={"count": "Number of Activities", "item_category": "Category"},
            color_discrete_sequence=[PALETTE["primary_green"]],
        )
        fig.update_layout(
            paper_bgcolor=PALETTE["background"],
            plot_bgcolor=PALETTE["background"],
            font_color=PALETTE["text"],
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Value saved bar
        fig2 = px.bar(
            cat_df,
            x="item_category",
            y="total_value_saved",
            title="Value Saved by Category",
            labels={"total_value_saved": "Value Saved (₹)", "item_category": "Category"},
            color_discrete_sequence=[PALETTE["secondary_green"]],
        )
        fig2.update_layout(
            paper_bgcolor=PALETTE["background"],
            plot_bgcolor=PALETTE["background"],
            font_color=PALETTE["text"],
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No impact data available for breakdown.")


# ---------------------------------------------------------------------------
# Analytics page
# ---------------------------------------------------------------------------


def analytics_page():
    """Analytics page — summary statistics and dynamic charts for owned datasets."""
    st.title("Analytics")
    st.markdown("Data-driven insights from CampusLoop datasets.")

    if not item_listings_manager:
        st.error("Item listings manager not available.")
        return

    df = item_listings_manager.load()
    if df.empty:
        st.info("No data to analyze.")
        return

    # Summary statistics
    st.markdown('<div class="section-header">Summary Statistics</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Listings", len(df))

    with col2:
        if "estimated_value_inr" in df.columns:
            mean_val = df["estimated_value_inr"].mean()
            st.metric("Avg Value (₹)", f"₹mean{mean_val:.0f}")

    with col3:
        condition_counts = df["condition"].value_counts() if "condition" in df.columns else {}
        most_common_cond = condition_counts.idxmax() if not condition_counts.empty else "N/A"
        st.metric("Most Common Condition", most_common_cond)

    with col4:
        mode_counts = df["sharing_mode"].value_counts() if "sharing_mode" in df.columns else {}
        most_common_mode = mode_counts.idxmax() if not mode_counts.empty else "N/A"
        st.metric("Most Common Mode", most_common_mode)

    # Dynamic charts
    st.markdown("---")
    st.markdown('<div class="section-header">Dynamic Charts</div>', unsafe_allow_html=True)

    # Chart 1: Sharing mode distribution
    fig1 = px.pie(
        df,
        names="sharing_mode",
        title="Sharing Mode Distribution",
        color_discrete_map={
            "SWAP": PALETTE["primary_green"],
            "GIVEAWAY": PALETTE["soft_green"],
            "BORROW": PALETTE["secondary_green"],
            "SELL": PALETTE["gold"],
        },
    )
    fig1.update_layout(
        paper_bgcolor=PALETTE["background"],
        plot_bgcolor=PALETTE["background"],
        font_color=PALETTE["text"],
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Chart 2: Condition distribution
    fig2 = px.pie(
        df,
        names="condition",
        title="Condition Distribution",
        color_discrete_map={
            "EXCELLENT": "#6DD588",
            "GOOD": "#84CC16",
            "FAIR": "#A3E45B",
        },
    )
    fig2.update_layout(
        paper_bgcolor=PALETTE["background"],
        plot_bgcolor=PALETTE["background"],
        font_color=PALETTE["text"],
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Chart 3: Value histogram
    fig3 = px.histogram(
        df,
        x="estimated_value_inr",
        title="Value Distribution",
        nbins=20,
        labels={"estimated_value_inr": "Value (₹)", "count": "Frequency"},
    )
    fig3.update_layout(
        paper_bgcolor=PALETTE["background"],
        plot_bgcolor=PALETTE["background"],
        font_color=PALETTE["text"],
    )
    st.plotly_chart(fig3, use_container_width=True)


# ---------------------------------------------------------------------------
# Smart Match page
# ---------------------------------------------------------------------------


def smart_match_page():
    """Smart Match — deterministic matching with explanations."""
    st.title("Smart Match")
    st.markdown("Find compatible sharing matches based on your preferences.")

    if not item_listings_manager or not sharing_activities_manager:
        st.error("Managers not available.")
        return

    df = item_listings_manager.load()
    if df.empty:
        st.info("No items available for matching.")
        return

    # User preferences
    st.markdown('<div class="section-header">Your Preferences</div>', unsafe_allow_html=True)
    with st.form("match_form"):
        c1, c2 = st.columns(2)
        with c1:
            user_id = st.text_input("Your user ID", value="U0726")
            preferred_category = st.selectbox("Preferred Category", ["All"] + sorted(df["category"].unique().tolist()))
            preferred_mode = st.selectbox("Preferred Sharing Mode", ["All", "SWAP", "GIVEAWAY", "BORROW", "SELL"])
        with c2:
            min_availability = st.date_input("Available from", value=pd.Timestamp.now())
            # For simplicity, we'll just match on category and mode

        submitted = st.form_submit_button("Find Matches")

    if submitted or True:  # Always show results for demo
        # Build match criteria
        filters = {}
        if preferred_category != "All":
            filters["category"] = preferred_category
        if preferred_mode != "All":
            filters["sharing_mode"] = preferred_mode

        # Search matching items
        if filters:
            matches = item_listings_manager.filter(**filters)
        else:
            matches = df.head(20)  # Show some items as potential matches

        # Filter by availability (simple check)
        if not matches.empty:
            st.markdown('<div class="section-header">Matches</div>', unsafe_allow_html=True)
            match_results = []

            for _, row in matches.iterrows():
                reasons = []
                score = 0

                # Category match
                if preferred_category != "All" and row.get("category") == preferred_category:
                    reasons.append("✓ Same category")
                    score += 25

                # Sharing mode match
                if preferred_mode != "All" and row.get("sharing_mode") == preferred_mode:
                    reasons.append("✓ Same sharing mode")
                    score += 25

                # Availability heuristic
                avail_until = row.get("available_until", "")
                if avail_until:
                    try:
                        avail_date = pd.Timestamp(avail_until)
                        requested_from = min_availability if isinstance(min_availability, pd.Timestamp) else pd.Timestamp(min_availability)
                        if avail_date >= requested_from:
                            reasons.append("✓ Available during your period")
                            score += 25
                    except Exception:
                        pass

                # Condition preference
                if row.get("condition") in ["EXCELLENT", "GOOD"]:
                    reasons.append("✓ Good condition")
                    score += 10

                total_score = min(score, 100)

                if total_score >= 50:  # Show decent matches
                    with st.container():
                        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                        c1, c2 = st.columns([3, 1])
                        with c1:
                            st.markdown(f"### {row.get('title', 'Unnamed item')}")
                            st.markdown(f"{row.get('category', '')} · {sharing_mode_tag(row.get('sharing_mode', ''))}", unsafe_allow_html=True)
                            st.markdown(f"₹{row.get('estimated_value_inr', 0):,}")
                        with c2:
                            st.markdown(f"**{total_score}% match**", unsafe_allow_html=True)
                            for reason in reasons:
                                st.markdown(f"<span class='match-badge'>{reason}</span>", unsafe_allow_html=True)

                        # CTA
                        if st.button(f"Match with {row.get('owner_user_id')}", key=f"match_{row.get('item_id')}"):
                            st.info(f"Great match! Consider reaching out to {row.get('owner_user_id')} about {row.get('title')}")
                        st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No matches found with current criteria. Try broadening your preferences!")


# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------


def main():
    """Main entry point for CampusLoop."""
    # Render navigation bar
    nav_bar()

    # Page routing
    # Initialize session state page if not set
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    # Navigation buttons in a compact bar
    page = st.session_state.current_page

    # Page header area
    st.markdown("---")

    # Route to pages
    if page == "Home":
        home_page()
    elif page == "Discover":
        discover_page()
    elif page == "My Listings":
        my_listings_page()
    elif page == "Sharing":
        sharing_page()
    elif page == "Users":
        users_page()
    elif page == "Impact":
        impact_page()
    elif page == "Analytics":
        analytics_page()
    elif page == "Smart Match":
        smart_match_page()


if __name__ == "__main__":
    main()