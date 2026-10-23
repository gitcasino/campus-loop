"""CampusLoop — premium campus circular-consumption platform.

The presentation layer is a complete rebuild on top of the TemplateMo 607
Glass Admin visual system (deep forest ambient background, glass surfaces,
emerald/gold palette, Outfit + Space Mono typography, 3D depth). The data layer
in ``src/campus_loop`` and the CSV files remain the source of truth.
"""

from __future__ import annotations

import math
import os
import sys
from datetime import date

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

import campus_loop as cl
from campus_loop.ui import (
    activity_feed,
    badge,
    bar_chart,
    compact,
    data_table,
    detail_card,
    donut_chart,
    empty_state,
    esc,
    fmt_inr,
    hero,
    histogram_chart,
    img_data_uri,
    inject_css,
    line_chart,
    listing_cards,
    mode_tag,
    page_header,
    stat_cards,
    stat_grid_frame,
    user_rows,
)

# ---------------------------------------------------------------------------
# Page config + data layer
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="CampusLoop",
    page_icon=os.path.join(BASE_DIR, "assets", "favicon.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

cl.init_managers(BASE_DIR)

DATA_DIR = os.path.join(BASE_DIR, "data")
PATHS = {
    "listings": os.path.join(DATA_DIR, "item_listings.csv"),
    "activities": os.path.join(DATA_DIR, "sharing_activities.csv"),
    "users": os.path.join(DATA_DIR, "users.csv"),
    "impact": os.path.join(DATA_DIR, "impact.csv"),
}

CATEGORIES = [
    "Accessory", "Electronics", "Equipment", "Book", "Stationery", "Clothing",
    "Lab Equipment", "Cable", "Storage", "Bag", "Academic", "Safety Equipment",
]
MODES = ["BORROW", "SWAP", "GIVEAWAY", "SELL"]
CONDITIONS = ["NEW", "EXCELLENT", "GOOD", "FAIR"]
ITEM_STATUSES = ["AVAILABLE", "RESERVED", "BORROWED", "RETURNED", "INACTIVE"]

DEFAULTS = {
    "page": "Home",
    "page_size": 12,
    "reduce_motion": False,
    "d_page": 1,
    "ml_page": 1,
    "sh_page": 1,
    "u_page": 1,
    "match_ready": False,
}
for _key, _value in DEFAULTS.items():
    st.session_state.setdefault(_key, _value)


def _mtime(path: str) -> float:
    try:
        return os.path.getmtime(path)
    except OSError:
        return 0.0


@st.cache_data(show_spinner=False)
def _cached_items(sig: float) -> pd.DataFrame:
    return cl.item_listings_manager.load()


@st.cache_data(show_spinner=False)
def _cached_activities(sig: float) -> pd.DataFrame:
    return cl.sharing_activities_manager.load()


@st.cache_data(show_spinner=False)
def _cached_users(sig: float) -> pd.DataFrame:
    return cl.user_manager.load()


@st.cache_data(show_spinner=False)
def _cached_impact(sig: float) -> pd.DataFrame:
    return cl.impact_manager.load()


def all_items() -> pd.DataFrame:
    return _cached_items(_mtime(PATHS["listings"]))


def all_activities() -> pd.DataFrame:
    return _cached_activities(_mtime(PATHS["activities"]))


def all_users() -> pd.DataFrame:
    return _cached_users(_mtime(PATHS["users"]))


def all_impact() -> pd.DataFrame:
    return _cached_impact(_mtime(PATHS["impact"]))


def invalidate() -> None:
    st.cache_data.clear()


def col(df: pd.DataFrame, name: str) -> pd.Series:
    return df[name] if name in df.columns else pd.Series(dtype="object")


def options(series: pd.Series) -> list[str]:
    if series is None or len(series) == 0:
        return []
    return sorted({str(v) for v in series.dropna().tolist() if str(v).strip()})


def flash(message: str, kind: str = "success") -> None:
    st.session_state["_flash"] = (kind, message)


def md(markup: str, **_: object) -> None:
    """Render a compacted HTML block so Streamlit cannot leak raw tags."""
    st.markdown(compact(markup), unsafe_allow_html=True)


def smd(markup: str, **_: object) -> None:
    st.sidebar.markdown(compact(markup), unsafe_allow_html=True)


def render_flash() -> None:
    pending = st.session_state.pop("_flash", None)
    if pending:
        kind, message = pending
        getattr(st, kind, st.info)(message)


def section(title: str, sub: str = "") -> None:
    sub_html = f'<p class="cl-section-sub">{esc(sub)}</p>' if sub else ""
    md(
        f'<div class="cl-section-head"><div><h2 class="cl-section-title">{esc(title)}</h2>{sub_html}</div></div>',
        unsafe_allow_html=True,
    )


def pager(page: int, pages: int, total: int, key_prefix: str, page_key: str) -> int:
    left, mid, right = st.columns([1, 2, 1])
    with left:
        if st.button("← Previous", key=f"{key_prefix}_prev", width="stretch", disabled=page <= 1):
            st.session_state[page_key] = page - 1
            st.rerun()
    with mid:
        md(
            f'<div class="cl-pager-text">Page {page} of {pages} &nbsp;·&nbsp; {total:,} records</div>',
            unsafe_allow_html=True,
        )
    with right:
        if st.button("Next →", key=f"{key_prefix}_next", width="stretch", disabled=page >= pages):
            st.session_state[page_key] = page + 1
            st.rerun()
    return page


def window(df: pd.DataFrame, page_key: str, size: int) -> tuple[pd.DataFrame, int, int]:
    pages = max(1, math.ceil(len(df) / size))
    page = int(min(max(st.session_state.get(page_key, 1), 1), pages))
    st.session_state[page_key] = page
    start = (page - 1) * size
    return df.iloc[start:start + size], page, pages


# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------
BRAND_LOGO = img_data_uri(os.path.join(BASE_DIR, "assets", "campusloop-logo-white.png"))
HERO_LOGO = img_data_uri(os.path.join(BASE_DIR, "assets", "campusloop-logo-full-white.png"))

NAV = [
    ("Main menu", ["Home", "Discover", "My Listings", "Sharing"]),
    ("Community", ["Users"]),
    ("Insights", ["Impact", "Analytics", "Smart Match"]),
    ("System", ["Settings"]),
]


def render_sidebar() -> None:
    smd(
        f"""
        <div class="cl-brand">
            <img class="cl-brand-logo" src="{BRAND_LOGO}" alt="CampusLoop" />
            <div class="cl-brand-sub">Share &middot; Reuse &middot; Save</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    current = st.session_state.page
    for title, pages in NAV:
        smd(f'<div class="cl-nav-section">{esc(title)}</div>', unsafe_allow_html=True)
        for page in pages:
            if st.sidebar.button(
                page,
                key=f"nav_{page}",
                width="stretch",
                type="primary" if page == current else "secondary",
            ):
                st.session_state.page = page
                st.rerun()

    member_count = len(all_users())
    smd(
        f"""
        <div class="cl-side-foot">
            <div class="cl-user">
                <div class="cl-avatar" style="background:linear-gradient(135deg,#8CFF66,#38D996)">CL</div>
                <div>
                    <div class="cl-user-name">CampusLoop</div>
                    <div class="cl-user-email">{member_count:,} campus members</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------
def home_page() -> None:
    listings = all_items()
    activities = all_activities()
    members = all_users()
    impacts = all_impact()

    md(page_header("Home", "Your campus circulation dashboard", "Overview"), unsafe_allow_html=True)
    md(hero(HERO_LOGO), unsafe_allow_html=True)

    c1, c2, c3, _ = st.columns([1.05, 1.05, 1.05, 1.85])
    with c1:
        if st.button("Discover items", key="home_discover", type="primary", width="stretch"):
            st.session_state.page = "Discover"
            st.rerun()
    with c2:
        if st.button("List an item", key="home_list", width="stretch"):
            st.session_state.page = "My Listings"
            st.rerun()
    with c3:
        if st.button("Find a match", key="home_match", width="stretch"):
            st.session_state.page = "Smart Match"
            st.rerun()

    st.write("")

    available = int((col(listings, "status") == "AVAILABLE").sum())
    completed = int((col(activities, "activity_status") == "COMPLETED").sum())
    value_saved = float(col(impacts, "estimated_value_saved_inr").sum()) if "estimated_value_saved_inr" in impacts else 0.0
    departments = int(col(members, "department").nunique())

    try:
        import streamlit as _st
        if hasattr(_st, "iframe"):
            _st.iframe(stat_grid_frame(
                [
                    ("Listings", len(listings), f"{available:,} available now", "", "listings", "", "", 0),
                    ("Sharing activities", len(activities), f"{completed:,} completed", "info", "activities", "", "", 0),
                    ("Campus members", len(members), f"{departments} departments", "gold", "users", "", "", 0),
                    ("Value retained", int(value_saved), "estimated savings", "coral", "value", "₹", "", 0),
                ]
            ), height=178, scrolling=False)
        else:
            components.html(
                stat_grid_frame(
                    [
                        ("Listings", len(listings), f"{available:,} available now", "", "listings", "", "", 0),
                        ("Sharing activities", len(activities), f"{completed:,} completed", "info", "activities", "", "", 0),
                        ("Campus members", len(members), f"{departments} departments", "gold", "users", "", "", 0),
                        ("Value retained", int(value_saved), "estimated savings", "coral", "value", "₹", "", 0),
                    ]
                ),
                height=178,
                scrolling=False,
            )
    except Exception:
        components.html(
            stat_grid_frame(
                [
                    ("Listings", len(listings), f"{available:,} available now", "", "listings", "", "", 0),
                    ("Sharing activities", len(activities), f"{completed:,} completed", "info", "activities", "", "", 0),
                    ("Campus members", len(members), f"{departments} departments", "gold", "users", "", "", 0),
                    ("Value retained", int(value_saved), "estimated savings", "coral", "value", "₹", "", 0),
                ]
            ),
            height=178,
            scrolling=False,
        )

    section("Fresh on campus", "The newest listings available to your community")
    recent = listings[col(listings, "status") == "AVAILABLE"] if not listings.empty else listings
    if not recent.empty and "listed_date" in recent:
        recent = recent.sort_values("listed_date", ascending=False)
    recent = recent.head(6)

    left, right = st.columns([1.62, 1.0], gap="large")
    with left:
        md(listing_cards(recent, cols=2), unsafe_allow_html=True)
    with right:
        section("Recent activity")
        latest = activities.sort_values("start_date", ascending=False).head(7) if not activities.empty else activities
        md(activity_feed(latest), unsafe_allow_html=True)

    section("How items move", "Live breakdown of the sharing modes on CampusLoop")
    counts = {mode: int((col(listings, "sharing_mode") == mode).sum()) for mode in MODES}
    md(
        stat_cards(
            [
                ("Borrow", f"{counts['BORROW']:,}", "items available to borrow", "info", "clock"),
                ("Swap", f"{counts['SWAP']:,}", "items open to exchange", "", "swap"),
                ("Give away", f"{counts['GIVEAWAY']:,}", "items offered for free", "gold", "leaf"),
                ("Sell", f"{counts['SELL']:,}", "items listed for sale", "coral", "value"),
            ]
        ),
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Discover
# ---------------------------------------------------------------------------
def discover_page() -> None:
    md(page_header("Discover", "Find what you need before buying it new", "Discover"), unsafe_allow_html=True)
    listings = all_items()
    if listings.empty:
        md(empty_state("No listings yet", "Create the first listing to start the campus loop."), unsafe_allow_html=True)
        return

    f1, f2, f3, f4 = st.columns([1.6, 1, 1, 1])
    with f1:
        query = st.text_input("Search", placeholder="Keyboard, backpack, camera…", key="disc_q")
    with f2:
        category = st.selectbox("Category", ["All"] + options(col(listings, "category")), key="disc_cat")
    with f3:
        mode = st.selectbox("Sharing mode", ["All"] + options(col(listings, "sharing_mode")), key="disc_mode")
    with f4:
        condition = st.selectbox("Condition", ["All"] + options(col(listings, "condition")), key="disc_cond")

    s1, s2 = st.columns(2)
    with s1:
        sort_by = st.selectbox(
            "Sort by",
            ["Newest", "Oldest", "Title A–Z", "Title Z–A", "Value: low to high", "Value: high to low"],
            key="disc_sort",
        )
    with s2:
        status = st.selectbox("Status", ["All"] + options(col(listings, "status")), key="disc_status")

    filtered = listings
    if query.strip():
        needle = query.strip()
        mask = (
            col(filtered, "title").astype(str).str.contains(needle, case=False, na=False)
            | col(filtered, "category").astype(str).str.contains(needle, case=False, na=False)
            | col(filtered, "pickup_location").astype(str).str.contains(needle, case=False, na=False)
        )
        filtered = filtered[mask]
    if category != "All":
        filtered = filtered[col(filtered, "category") == category]
    if mode != "All":
        filtered = filtered[col(filtered, "sharing_mode") == mode]
    if condition != "All":
        filtered = filtered[col(filtered, "condition") == condition]
    if status != "All":
        filtered = filtered[col(filtered, "status") == status]

    if sort_by == "Newest" and "listed_date" in filtered:
        filtered = filtered.sort_values("listed_date", ascending=False)
    elif sort_by == "Oldest" and "listed_date" in filtered:
        filtered = filtered.sort_values("listed_date", ascending=True)
    elif sort_by == "Title A–Z" and "title" in filtered:
        filtered = filtered.sort_values("title", ascending=True)
    elif sort_by == "Title Z–A" and "title" in filtered:
        filtered = filtered.sort_values("title", ascending=False)
    elif sort_by == "Value: low to high" and "estimated_value_inr" in filtered:
        filtered = filtered.sort_values("estimated_value_inr", ascending=True)
    elif sort_by == "Value: high to low" and "estimated_value_inr" in filtered:
        filtered = filtered.sort_values("estimated_value_inr", ascending=False)

    if filtered.empty:
        md(empty_state("Nothing matches those filters", "Try a broader search or clear a filter."), unsafe_allow_html=True)
        return

    size = int(st.session_state.page_size)
    page_df, page, pages = window(filtered, "d_page", size)
    md(
        f'<p class="cl-note" style="margin:0 0 14px">Showing {(page - 1) * size + 1:,}–'
        f'{min(page * size, len(filtered)):,} of {len(filtered):,} listings</p>',
        unsafe_allow_html=True,
    )
    md(listing_cards(page_df, cols=3), unsafe_allow_html=True)

    pager(page, pages, len(filtered), "discover", "d_page")

    section("Listing detail", "Inspect any listing on this page")
    selected = st.selectbox("Choose a listing", page_df["item_id"].tolist(), key="disc_selected")
    match = page_df[page_df["item_id"] == selected]
    if not match.empty:
        md(detail_card(match.iloc[0]), unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# My Listings
# ---------------------------------------------------------------------------
def _owner_default() -> str:
    members = all_users()
    if not members.empty and "user_id" in members:
        return str(members.iloc[0]["user_id"])
    return "U0001"


def my_listings_page() -> None:
    md(page_header("My Listings", "Create, inspect and manage the item catalogue", "My Listings"), unsafe_allow_html=True)
    listings = all_items()
    tab_create, tab_browse, tab_update, tab_delete = st.tabs(["Create", "Browse", "Update", "Delete"])

    with tab_create:
        with st.form("create_listing_form", clear_on_submit=True):
            r1 = st.columns(2)
            owner = r1[0].text_input("Owner user ID", value=_owner_default())
            title = r1[1].text_input("Title", placeholder="Bluetooth keyboard")
            r2 = st.columns(3)
            category = r2[0].selectbox("Category", options(col(listings, "category")) or CATEGORIES)
            item_type = r2[1].text_input("Item type", placeholder="Keyboard")
            brand = r2[2].text_input("Brand", placeholder="Logitech")
            r3 = st.columns(3)
            condition = r3[0].selectbox("Condition", options(col(listings, "condition")) or CONDITIONS)
            mode = r3[1].selectbox("Sharing mode", options(col(listings, "sharing_mode")) or MODES)
            status = r3[2].selectbox("Status", options(col(listings, "status")) or ITEM_STATUSES)
            r4 = st.columns(3)
            value = r4[0].number_input("Estimated value (₹)", min_value=0, value=500, step=50)
            listed = r4[1].date_input("Listed on", value=date.today())
            until = r4[2].date_input("Available until", value=date.today() + pd.Timedelta(days=90))
            location = st.text_input("Pickup location", value="Central Library")
            submitted = st.form_submit_button("Publish listing", type="primary")

        if submitted:
            if not title.strip():
                st.error("A title is required.")
            elif until < listed:
                st.error("Available-until must be on or after the listed date.")
            else:
                try:
                    cl.item_listings_manager.add(
                        owner_user_id=owner.strip() or _owner_default(),
                        title=title.strip(),
                        category=category,
                        item_type=item_type.strip() or category,
                        brand=brand.strip(),
                        condition=condition,
                        sharing_mode=mode,
                        status=status,
                        estimated_value_inr=int(value),
                        listed_date=listed.strftime("%Y-%m-%d"),
                        available_until=until.strftime("%Y-%m-%d"),
                        pickup_location=location.strip(),
                    )
                    invalidate()
                    flash(f"Listing “{title.strip()}” published.")
                    st.rerun()
                except Exception as exc:  # noqa: BLE001 - surface data errors to the user
                    st.error(f"Could not create listing: {exc}")

    with tab_browse:
        b1, b2, b3 = st.columns([1.6, 1, 1])
        with b1:
            needle = st.text_input("Search listings", placeholder="Title, category or location", key="ml_q")
        with b2:
            bcat = st.selectbox("Category", ["All"] + options(col(listings, "category")), key="ml_cat")
        with b3:
            bstatus = st.selectbox("Status", ["All"] + options(col(listings, "status")), key="ml_status")

        shown = listings
        if needle.strip():
            mask = (
                col(shown, "title").astype(str).str.contains(needle.strip(), case=False, na=False)
                | col(shown, "category").astype(str).str.contains(needle.strip(), case=False, na=False)
                | col(shown, "pickup_location").astype(str).str.contains(needle.strip(), case=False, na=False)
                | col(shown, "item_id").astype(str).str.contains(needle.strip(), case=False, na=False)
            )
            shown = shown[mask]
        if bcat != "All":
            shown = shown[col(shown, "category") == bcat]
        if bstatus != "All":
            shown = shown[col(shown, "status") == bstatus]
        shown = shown.sort_values("item_id")

        if shown.empty:
            md(empty_state("No listings match", "Adjust the search or filters."), unsafe_allow_html=True)
        else:
            page_df, page, pages = window(shown, "ml_page", int(st.session_state.page_size))
            rows = []
            for _, row in page_df.iterrows():
                title_cell = (
                    f'<div class="cl-user-name">{esc(row.get("title"))}</div>'
                    f'<div class="cl-mono">{esc(row.get("item_id"))}</div>'
                )
                rows.append([
                    title_cell,
                    esc(row.get("category")),
                    mode_tag(row.get("sharing_mode")),
                    esc(row.get("condition")),
                    f'<span class="num">{fmt_inr(row.get("estimated_value_inr"))}</span>',
                    badge(row.get("status")),
                    esc(row.get("pickup_location")),
                ])
            md(
                data_table(["Item", "Category", "Mode", "Condition", "Value", "Status", "Pickup"], rows),
                unsafe_allow_html=True,
            )
            pager(page, pages, len(shown), "mylist", "ml_page")

    with tab_update:
        update_id = st.text_input("Item ID to update", placeholder="I00001", key="ml_update_id")
        if update_id.strip():
            target = listings[listings["item_id"] == update_id.strip()] if "item_id" in listings else listings.iloc[0:0]
            if target.empty:
                st.warning(f"No listing found with ID {update_id.strip()}.")
            else:
                row = target.iloc[0]
                md(detail_card(row), unsafe_allow_html=True)
                sid = str(row.get("item_id"))
                with st.form(f"update_listing_{sid}"):
                    r1 = st.columns(2)
                    new_title = r1[0].text_input("Title", value=str(row.get("title", "")), key=f"upd_title_{sid}")
                    new_location = r1[1].text_input("Pickup location", value=str(row.get("pickup_location", "")), key=f"upd_loc_{sid}")
                    r2 = st.columns(3)
                    cats = options(col(listings, "category")) or CATEGORIES
                    new_category = r2[0].selectbox(
                        "Category", cats,
                        index=cats.index(row.get("category")) if row.get("category") in cats else 0,
                        key=f"upd_cat_{sid}",
                    )
                    conds = options(col(listings, "condition")) or CONDITIONS
                    new_condition = r2[1].selectbox(
                        "Condition", conds,
                        index=conds.index(row.get("condition")) if row.get("condition") in conds else 0,
                        key=f"upd_cond_{sid}",
                    )
                    modes = options(col(listings, "sharing_mode")) or MODES
                    new_mode = r2[2].selectbox(
                        "Sharing mode", modes,
                        index=modes.index(row.get("sharing_mode")) if row.get("sharing_mode") in modes else 0,
                        key=f"upd_mode_{sid}",
                    )
                    r3 = st.columns(3)
                    stats_list = options(col(listings, "status")) or ITEM_STATUSES
                    new_status = r3[0].selectbox(
                        "Status", stats_list,
                        index=stats_list.index(row.get("status")) if row.get("status") in stats_list else 0,
                        key=f"upd_status_{sid}",
                    )
                    new_value = r3[1].number_input(
                        "Estimated value (₹)", min_value=0,
                        value=int(row.get("estimated_value_inr", 0) or 0), step=50,
                        key=f"upd_value_{sid}",
                    )
                    new_until = r3[2].date_input(
                        "Available until",
                        value=pd.to_datetime(row.get("available_until"), errors="coerce").date()
                        if pd.notna(pd.to_datetime(row.get("available_until"), errors="coerce")) else date.today(),
                        key=f"upd_until_{sid}",
                    )
                    save = st.form_submit_button("Save changes", type="primary")
                if save:
                    try:
                        cl.item_listings_manager.update(sid, {
                            "title": new_title.strip() or str(row.get("title")),
                            "pickup_location": new_location.strip(),
                            "category": new_category,
                            "condition": new_condition,
                            "sharing_mode": new_mode,
                            "status": new_status,
                            "estimated_value_inr": int(new_value),
                            "available_until": new_until.strftime("%Y-%m-%d"),
                        })
                        invalidate()
                        flash(f"Listing {sid} updated.")
                        st.rerun()
                    except Exception as exc:  # noqa: BLE001
                        st.error(f"Could not update listing: {exc}")

    with tab_delete:
        delete_id = st.text_input("Item ID to delete", placeholder="I00001", key="ml_delete_id")
        if delete_id.strip():
            target = listings[listings["item_id"] == delete_id.strip()] if "item_id" in listings else listings.iloc[0:0]
            if target.empty:
                st.warning(f"No listing found with ID {delete_id.strip()}.")
            else:
                row = target.iloc[0]
                md(detail_card(row), unsafe_allow_html=True)
                confirmed = st.checkbox("I understand this permanently removes the listing.", key="ml_confirm_delete")
                if st.button("Delete listing", key="ml_delete_btn", type="primary", disabled=not confirmed):
                    try:
                        cl.item_listings_manager.delete(str(row.get("item_id")))
                        invalidate()
                        flash(f"Listing {row.get('item_id')} deleted.", "warning")
                        st.rerun()
                    except Exception as exc:  # noqa: BLE001
                        st.error(f"Could not delete listing: {exc}")


# ---------------------------------------------------------------------------
# Sharing
# ---------------------------------------------------------------------------
def sharing_page() -> None:
    md(page_header("Sharing", "Borrows, swaps, giveaways and sales in motion", "Sharing"), unsafe_allow_html=True)
    activities = all_activities()
    listings = all_items()

    total = len(activities)
    active = int((col(activities, "activity_status") == "ACTIVE").sum())
    completed = int((col(activities, "activity_status") == "COMPLETED").sum())
    overdue = int((col(activities, "activity_status") == "OVERDUE").sum())
    md(
        stat_cards(
            [
                ("Activities", f"{total:,}", "recorded on campus", "", "activities"),
                ("Active", f"{active:,}", "currently in progress", "info", "clock"),
                ("Completed", f"{completed:,}", "successfully returned", "", "swap"),
                ("Overdue", f"{overdue:,}", "needs attention", "coral", "leaf"),
            ]
        ),
        unsafe_allow_html=True,
    )

    q1, q2, q3 = st.columns([1.6, 1, 1])
    with q1:
        needle = st.text_input("Search activity", placeholder="Activity, item, borrower or owner ID", key="sh_q")
    with q2:
        activity_type = st.selectbox("Activity type", ["All"] + options(col(activities, "activity_type")), key="sh_type")
    with q3:
        activity_status = st.selectbox("Status", ["All"] + options(col(activities, "activity_status")), key="sh_status")

    shown = activities
    if needle.strip():
        n = needle.strip()
        mask = (
            col(shown, "activity_id").astype(str).str.contains(n, case=False, na=False)
            | col(shown, "item_id").astype(str).str.contains(n, case=False, na=False)
            | col(shown, "borrower_user_id").astype(str).str.contains(n, case=False, na=False)
            | col(shown, "owner_user_id").astype(str).str.contains(n, case=False, na=False)
        )
        shown = shown[mask]
    if activity_type != "All":
        shown = shown[col(shown, "activity_type") == activity_type]
    if activity_status != "All":
        shown = shown[col(shown, "activity_status") == activity_status]
    if "start_date" in shown:
        shown = shown.sort_values("start_date", ascending=False)

    if shown.empty:
        md(empty_state("No activities match", "Adjust the filters or record a new activity."), unsafe_allow_html=True)
    else:
        page_df, page, pages = window(shown, "sh_page", int(st.session_state.page_size))
        rows = []
        for _, row in page_df.iterrows():
            rows.append([
                f'<span class="cl-mono">{esc(row.get("activity_id"))}</span>',
                mode_tag(row.get("activity_type")),
                f'<span class="cl-mono">{esc(row.get("item_id"))}</span>',
                esc(row.get("borrower_user_id")),
                esc(row.get("owner_user_id")),
                f'{esc(row.get("start_date"))} → {esc(row.get("due_date"))}',
                badge(row.get("activity_status")),
                f'<span class="num">{fmt_inr(row.get("estimated_value_inr"))}</span>',
                badge(row.get("return_status")),
            ])
        md(
            data_table(["Activity", "Type", "Item", "Borrower", "Owner", "Window", "Status", "Value", "Return"], rows),
            unsafe_allow_html=True,
        )
        pager(page, pages, len(shown), "sharing", "sh_page")

    with st.expander("Record a new activity"):
        item_ids = set(col(listings, "item_id").astype(str).tolist()) if not listings.empty else set()
        sample_item = next(iter(item_ids)) if item_ids else "I00001"
        with st.form("create_activity_form", clear_on_submit=True):
            r1 = st.columns(3)
            item_id = r1[0].text_input("Item ID", value=sample_item)
            atype = r1[1].selectbox("Activity type", MODES)
            astatus = r1[2].selectbox("Activity status", ["ACTIVE", "COMPLETED", "CANCELLED", "OVERDUE"])
            r2 = st.columns(3)
            borrower = r2[0].text_input("Borrower user ID", value="U0726")
            owner = r2[1].text_input("Owner user ID", value="U0490")
            value = r2[2].number_input("Estimated value (₹)", min_value=0, value=1000, step=50)
            r3 = st.columns(3)
            start = r3[0].date_input("Start date", value=date.today())
            due = r3[1].date_input("Due date", value=date.today() + pd.Timedelta(days=14))
            duration = r3[2].number_input("Duration (days)", min_value=0, value=14)
            r4 = st.columns(2)
            resolution = r4[0].selectbox("Resolution", ["PENDING", "COMPLETED", "CANCELLED"])
            return_status = r4[1].selectbox("Return status", ["NA", "ON_TIME", "LATE", "RETURNED"])
            submitted = st.form_submit_button("Record activity", type="primary")

        if submitted:
            if item_id.strip() not in item_ids:
                st.error("That item ID does not exist in the catalogue.")
            elif borrower.strip() == owner.strip():
                st.error("Borrower and owner must be different users.")
            elif due < start:
                st.error("Due date must be on or after the start date.")
            else:
                try:
                    cl.sharing_activities_manager.add(
                        item_id=item_id.strip(),
                        borrower_user_id=borrower.strip(),
                        owner_user_id=owner.strip(),
                        activity_type=atype,
                        start_date=start.strftime("%Y-%m-%d"),
                        request_date=date.today().strftime("%Y-%m-%d"),
                        due_date=due.strftime("%Y-%m-%d"),
                        activity_status=astatus,
                        duration_days=int(duration),
                        estimated_value_inr=int(value),
                        resolution_status=resolution,
                        return_status=return_status,
                    )
                    invalidate()
                    flash("Sharing activity recorded.")
                    st.rerun()
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Could not record activity: {exc}")

    with st.expander("Manage an existing activity"):
        manage_id = st.text_input("Activity ID", placeholder="A000001", key="sh_manage_id")
        if manage_id.strip():
            target = activities[activities["activity_id"] == manage_id.strip()] if "activity_id" in activities else activities.iloc[0:0]
            if target.empty:
                st.warning(f"No activity found with ID {manage_id.strip()}.")
            else:
                row = target.iloc[0]
                with st.form(f"update_activity_{row.get('activity_id')}"):
                    u1 = st.columns(3)
                    new_status = u1[0].selectbox(
                        "Activity status", ["ACTIVE", "COMPLETED", "CANCELLED", "OVERDUE"],
                        index=["ACTIVE", "COMPLETED", "CANCELLED", "OVERDUE"].index(row.get("activity_status"))
                        if row.get("activity_status") in ["ACTIVE", "COMPLETED", "CANCELLED", "OVERDUE"] else 0,
                    )
                    resolution_options = ["PENDING", "COMPLETED", "CANCELLED"]
                    new_resolution = u1[1].selectbox(
                        "Resolution", resolution_options,
                        index=resolution_options.index(row.get("resolution_status"))
                        if row.get("resolution_status") in resolution_options else 0,
                    )
                    return_options = ["NA", "ON_TIME", "LATE", "RETURNED"]
                    new_return = u1[2].selectbox(
                        "Return", return_options,
                        index=return_options.index(row.get("return_status"))
                        if row.get("return_status") in return_options else 0,
                    )
                    save = st.form_submit_button("Update activity", type="primary")
                c1, c2 = st.columns([1, 1])
                with c2:
                    confirmed = st.checkbox("Confirm permanent deletion", key="sh_confirm")
                    if st.button("Delete activity", key="sh_delete", disabled=not confirmed):
                        try:
                            cl.sharing_activities_manager.delete(str(row.get("activity_id")))
                            invalidate()
                            flash(f"Activity {row.get('activity_id')} deleted.", "warning")
                            st.rerun()
                        except Exception as exc:  # noqa: BLE001
                            st.error(f"Could not delete activity: {exc}")
                if save:
                    try:
                        cl.sharing_activities_manager.update(str(row.get("activity_id")), {
                            "activity_status": new_status,
                            "resolution_status": new_resolution,
                            "return_status": new_return,
                        })
                        invalidate()
                        flash(f"Activity {row.get('activity_id')} updated.")
                        st.rerun()
                    except Exception as exc:  # noqa: BLE001
                        st.error(f"Could not update activity: {exc}")


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------
def users_page() -> None:
    md(page_header("Users", "The campus community behind every exchange", "Users"), unsafe_allow_html=True)
    members = all_users()
    if members.empty:
        md(empty_state("No member data", "users.csv is empty or unavailable."), unsafe_allow_html=True)
        return

    active = int((col(members, "account_status") == "ACTIVE").sum())
    inactive = int((col(members, "account_status") == "INACTIVE").sum())
    departments = int(col(members, "department").nunique())
    md(
        stat_cards(
            [
                ("Members", f"{len(members):,}", "campus accounts", "", "users"),
                ("Active", f"{active:,}", "in good standing", "info", "users"),
                ("Inactive", f"{inactive:,}", "not currently active", "coral", "clock"),
                ("Departments", f"{departments}", "represented on campus", "gold", "activities"),
            ]
        ),
        unsafe_allow_html=True,
    )

    q1, q2, q3 = st.columns([1.6, 1, 1])
    with q1:
        needle = st.text_input("Search members", placeholder="Name, email or user ID", key="u_q")
    with q2:
        department = st.selectbox("Department", ["All"] + options(col(members, "department")), key="u_dept")
    with q3:
        account_status = st.selectbox("Status", ["All"] + options(col(members, "account_status")), key="u_status")

    shown = members
    if needle.strip():
        n = needle.strip()
        mask = (
            col(shown, "name").astype(str).str.contains(n, case=False, na=False)
            | col(shown, "email").astype(str).str.contains(n, case=False, na=False)
            | col(shown, "user_id").astype(str).str.contains(n, case=False, na=False)
        )
        shown = shown[mask]
    if department != "All":
        shown = shown[col(shown, "department") == department]
    if account_status != "All":
        shown = shown[col(shown, "account_status") == account_status]

    if shown.empty:
        md(empty_state("No members match", "Try a different search or department."), unsafe_allow_html=True)
        return

    shown = shown.sort_values("name")
    page_df, page, pages = window(shown, "u_page", 20)
    md(user_rows(page_df), unsafe_allow_html=True)
    pager(page, pages, len(shown), "users", "u_page")


# ---------------------------------------------------------------------------
# Impact
# ---------------------------------------------------------------------------
def _monthly_sum(df: pd.DataFrame, date_col: str, value_col: str) -> pd.DataFrame:
    if df.empty or date_col not in df or value_col not in df:
        return pd.DataFrame(columns=["month", "value"])
    working = df[[date_col, value_col]].copy()
    working[date_col] = pd.to_datetime(working[date_col], errors="coerce")
    working = working.dropna(subset=[date_col])
    if working.empty:
        return pd.DataFrame(columns=["month", "value"])
    working["month"] = working[date_col].dt.to_period("M").astype(str)
    grouped = (
        working.groupby("month", as_index=False)[value_col]
        .sum()
        .rename(columns={value_col: "value"})
    )
    return grouped.sort_values("month").tail(18)


def impact_page() -> None:
    md(page_header("Impact", "What sharing keeps in circulation", "Impact"), unsafe_allow_html=True)
    impact = all_impact()
    if impact.empty:
        md(empty_state("No impact data", "impact.csv is empty or unavailable."), unsafe_allow_html=True)
        return

    impact_categories = options(col(impact, "impact_category"))
    chosen = st.selectbox("Impact category", ["All"] + impact_categories, key="imp_cat")
    data = impact if chosen == "All" else impact[col(impact, "impact_category") == chosen]

    value_saved = float(col(data, "estimated_value_saved_inr").sum())
    items_reused = int(col(data, "items_reused").sum())
    avg_factor = float(col(data, "estimated_material_reuse_factor").mean() or 0)
    md(
        stat_cards(
            [
                ("Activities", f"{len(data):,}", "with recorded impact", "", "activities"),
                ("Value saved", fmt_inr(value_saved), "estimated value retained", "gold", "value"),
                ("Items reused", f"{items_reused:,}", "kept in circulation", "", "leaf"),
                ("Avg reuse factor", f"{avg_factor:.2f}", "material reuse indicator", "info", "swap"),
            ]
        ),
        unsafe_allow_html=True,
    )

    by_category = (
        data.groupby("item_category", as_index=False)
        .agg(activities=("impact_id", "count"),
             value_saved=("estimated_value_saved_inr", "sum"),
             items_reused=("items_reused", "sum"),
             avg_factor=("estimated_material_reuse_factor", "mean"))
        .sort_values("value_saved", ascending=False)
    )
    by_type = data["activity_type"].value_counts() if "activity_type" in data else pd.Series(dtype=int)

    c1, c2 = st.columns(2)
    with c1:
        top = by_category.head(10).sort_values("value_saved")
        fig = bar_chart(top["item_category"].tolist(), top["value_saved"].tolist(), horizontal=True, height=330)
        fig.update_layout(title=dict(text="Value saved by category", font=dict(size=14)))
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    with c2:
        fig = donut_chart(by_type.index.tolist(), by_type.values.tolist(),
                          center_value=f"{len(data):,}", center_label="IMPACT RECORDS", height=330)
        fig.update_layout(title=dict(text="Impact by activity type", font=dict(size=14)))
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    c3, c4 = st.columns(2)
    with c3:
        monthly = _monthly_sum(data, "impact_date", "estimated_value_saved_inr")
        fig = line_chart(monthly["month"].tolist(), monthly["value"].tolist(), height=310)
        fig.update_layout(title=dict(text="Monthly value saved", font=dict(size=14)))
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    with c4:
        factors = pd.to_numeric(col(data, "estimated_material_reuse_factor"), errors="coerce").dropna()
        if factors.empty:
            md(empty_state("No reuse factors", "No numeric reuse factor data available."), unsafe_allow_html=True)
        else:
            counts, edges = np.histogram(factors.clip(0, 1), bins=np.linspace(0, 1, 11))
            centers = [round(float((edges[i] + edges[i + 1]) / 2), 2) for i in range(len(counts))]
            fig = histogram_chart(centers, counts.tolist(), height=310)
            fig.update_layout(title=dict(text="Reuse factor distribution", font=dict(size=14)))
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    section("Category breakdown", "Aggregated with Pandas from impact.csv")
    top_categories = by_category.head(12)
    rows = []
    for _, row in top_categories.iterrows():
        rows.append([
            esc(row.get("item_category")),
            f'<span class="num">{int(row.get("activities", 0)):,}</span>',
            f'<span class="num">{fmt_inr(row.get("value_saved", 0))}</span>',
            f'<span class="num">{int(row.get("items_reused", 0)):,}</span>',
            f'<span class="num">{float(row.get("avg_factor", 0) or 0):.2f}</span>',
        ])
    md(data_table(["Category", "Activities", "Value saved", "Items reused", "Avg factor"], rows), unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------
def analytics_page() -> None:
    md(page_header("Analytics", "Catalogue and circulation intelligence", "Analytics"), unsafe_allow_html=True)
    listings = all_items()
    activities = all_activities()
    if listings.empty:
        md(empty_state("Nothing to analyse", "Add listings to unlock analytics."), unsafe_allow_html=True)
        return

    f1, f2 = st.columns(2)
    with f1:
        category = st.selectbox("Category focus", ["All"] + options(col(listings, "category")), key="an_cat")
    with f2:
        mode = st.selectbox("Sharing mode focus", ["All"] + options(col(listings, "sharing_mode")), key="an_mode")

    data = listings
    if category != "All":
        data = data[col(data, "category") == category]
    if mode != "All":
        data = data[col(data, "sharing_mode") == mode]

    avg_value = float(pd.to_numeric(col(data, "estimated_value_inr"), errors="coerce").mean() or 0)
    available = int((col(data, "status") == "AVAILABLE").sum())
    active_activities = int((col(activities, "activity_status") == "ACTIVE").sum())
    md(
        stat_cards(
            [
                ("Listings", f"{len(data):,}", "in the current focus", "", "listings"),
                ("Average value", fmt_inr(avg_value), "per listing", "gold", "value"),
                ("Available now", f"{available:,}", "ready to circulate", "info", "clock"),
                ("Active activities", f"{active_activities:,}", "currently in progress", "coral", "activities"),
            ]
        ),
        unsafe_allow_html=True,
    )

    mode_counts = data["sharing_mode"].value_counts() if "sharing_mode" in data else pd.Series(dtype=int)
    cat_counts = data["category"].value_counts().head(10) if "category" in data else pd.Series(dtype=int)

    c1, c2 = st.columns(2)
    with c1:
        fig = donut_chart(mode_counts.index.tolist(), mode_counts.values.tolist(),
                          center_value=f"{len(data):,}", center_label="LISTINGS", height=320)
        fig.update_layout(title=dict(text="Sharing mode mix", font=dict(size=14)))
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    with c2:
        ordered = cat_counts.sort_values()
        fig = bar_chart(ordered.index.tolist(), ordered.values.tolist(), horizontal=True, height=320)
        fig.update_layout(title=dict(text="Top categories", font=dict(size=14)))
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    c3, c4 = st.columns(2)
    with c3:
        if "listed_date" in data:
            dates = pd.to_datetime(data["listed_date"], errors="coerce").dropna()
            monthly = dates.dt.to_period("M").astype(str).value_counts().sort_index().tail(18)
            fig = line_chart(monthly.index.tolist(), monthly.values.tolist(), height=310, name="Listings")
            fig.update_layout(title=dict(text="Listing volume by month", font=dict(size=14)))
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    with c4:
        values = pd.to_numeric(col(data, "estimated_value_inr"), errors="coerce").dropna()
        if not values.empty:
            counts, edges = np.histogram(values, bins=16)
            centers = [round(float((edges[i] + edges[i + 1]) / 2)) for i in range(len(counts))]
            fig = histogram_chart(centers, counts.tolist(), height=310)
            fig.update_layout(title=dict(text="Value distribution", font=dict(size=14)))
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    c5, c6 = st.columns(2)
    with c5:
        status_counts = activities["activity_status"].value_counts() if "activity_status" in activities else pd.Series(dtype=int)
        fig = donut_chart(status_counts.index.tolist(), status_counts.values.tolist(),
                          center_value=f"{len(activities):,}", center_label="ACTIVITIES", height=310)
        fig.update_layout(title=dict(text="Activity status", font=dict(size=14)))
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    with c6:
        if "pickup_location" in data:
            locations = data["pickup_location"].value_counts().head(8).sort_values()
            fig = bar_chart(locations.index.tolist(), locations.values.tolist(), horizontal=True, height=310)
            fig.update_layout(title=dict(text="Pickup hotspots", font=dict(size=14)))
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


# ---------------------------------------------------------------------------
# Smart Match
# ---------------------------------------------------------------------------
def _score_listing(row: pd.Series, prefs: dict) -> tuple[int, list[tuple[str, str]]]:
    score = 0
    reasons: list[tuple[str, str]] = []
    if prefs["category"] != "All" and row.get("category") == prefs["category"]:
        score += 25
        reasons.append(("Category", str(row.get("category"))))
    if prefs["mode"] != "All" and row.get("sharing_mode") == prefs["mode"]:
        score += 20
        reasons.append(("Mode", str(row.get("sharing_mode"))))
    if prefs["condition"] != "Any":
        order = {"NEW": 4, "EXCELLENT": 3, "GOOD": 2, "FAIR": 1}
        if order.get(str(row.get("condition")), 0) >= order.get(prefs["condition"], 0):
            score += 10
            reasons.append(("Condition", str(row.get("condition"))))
    if str(row.get("status")) == "AVAILABLE":
        score += 25
        reasons.append(("Status", "available"))
    avail = pd.to_datetime(row.get("available_until"), errors="coerce")
    if pd.notna(avail) and avail.date() >= prefs["available_from"]:
        score += 20
        reasons.append(("Availability", f"until {avail.date()}"))
    return min(score, 100), reasons


def _match_cards(results: list[tuple[pd.Series, int, list[tuple[str, str]]]]) -> str:
    cards = []
    for row, score, reasons in results:
        reason_html = "".join(
            f'<span class="cl-reason"><b>{esc(label)}</b> {esc(value)}</span>' for label, value in reasons
        ) or '<span class="cl-reason">General compatibility</span>'
        cards.append(
            f"""
            <article class="cl-listing">
                <div class="cl-listing-top">
                    <span class="cl-eyebrow">{esc(row.get('category'))}</span>
                    <span class="cl-match-score">{score}%</span>
                </div>
                <h3 class="cl-listing-title">{esc(row.get('title'))}</h3>
                <div class="cl-bar"><div class="cl-bar-fill" style="width:{score}%"></div></div>
                <div class="cl-reasons">{reason_html}</div>
                <div class="cl-listing-foot">
                    <span class="cl-price">{fmt_inr(row.get('estimated_value_inr'))}</span>
                    {mode_tag(row.get('sharing_mode'))}
                </div>
                <div class="cl-listing-sub">Owner {esc(row.get('owner_user_id'))} &middot; {esc(row.get('condition'))} &middot; until {esc(row.get('available_until'))}</div>
            </article>
            """
        )
    return f'<div class="cl-grid cl-grid-3">{"".join(cards)}</div>'


def smart_match_page() -> None:
    md(page_header("Smart Match", "Deterministic, explainable item matching", "Smart Match"), unsafe_allow_html=True)
    listings = all_items()
    members = all_users()
    if listings.empty:
        md(empty_state("No items to match", "Add listings before using Smart Match."), unsafe_allow_html=True)
        return

    default_user = str(members.iloc[0]["user_id"]) if not members.empty and "user_id" in members else "U0726"
    stored = st.session_state.get("match_prefs", {
        "category": "All",
        "mode": "All",
        "condition": "Any",
        "available_from": date.today(),
        "user_id": default_user,
    })

    cats = ["All"] + options(col(listings, "category"))
    modes = ["All"] + options(col(listings, "sharing_mode"))
    conditions = ["Any"] + options(col(listings, "condition"))
    with st.form("match_prefs_form"):
        r1 = st.columns(3)
        user_id = r1[0].text_input("Your user ID", value=stored.get("user_id", default_user))
        category = r1[1].selectbox("Preferred category", cats,
                                   index=cats.index(stored["category"]) if stored.get("category") in cats else 0)
        mode = r1[2].selectbox("Preferred sharing mode", modes,
                               index=modes.index(stored["mode"]) if stored.get("mode") in modes else 0)
        r2 = st.columns(3)
        condition = r2[0].selectbox("Minimum condition", conditions,
                                    index=conditions.index(stored["condition"]) if stored.get("condition") in conditions else 0)
        available_from = r2[1].date_input("Available from", value=stored.get("available_from", date.today()))
        submitted = r2[2].form_submit_button("Find matches", type="primary")

    if submitted:
        st.session_state.match_prefs = {
            "category": category,
            "mode": mode,
            "condition": condition,
            "available_from": available_from,
            "user_id": user_id.strip() or default_user,
        }
        st.session_state.match_ready = True

    if not st.session_state.get("match_ready"):
        md(
            '<p class="cl-note" style="margin-top:14px">Set your preferences and run Smart Match. '
            'Scoring is rule-based and fully explainable — no external AI service is used.</p>',
            unsafe_allow_html=True,
        )
        return

    prefs = st.session_state.match_prefs
    candidates = listings[col(listings, "owner_user_id") != prefs["user_id"]]
    scored: list[tuple[pd.Series, int, list[tuple[str, str]]]] = []
    for _, row in candidates.iterrows():
        score, reasons = _score_listing(row, prefs)
        if score >= 45:
            scored.append((row, score, reasons))
    scored.sort(key=lambda item: (-item[1], str(item[0].get("title", ""))))
    scored = scored[:12]

    if not scored:
        md(
            empty_state("No strong matches yet", "Broaden your category, mode or condition preference."),
            unsafe_allow_html=True,
        )
        return

    md(
        f'<p class="cl-note" style="margin:16px 0 14px">Top {len(scored)} matches, ranked from the full catalogue '
        f'using category, mode, condition, status and availability rules.</p>',
        unsafe_allow_html=True,
    )
    md(_match_cards(scored), unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
def _csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def settings_page() -> None:
    md(page_header("Settings", "Workspace, data and presentation controls", "Settings"), unsafe_allow_html=True)

    listings = all_items()
    activities = all_activities()
    members = all_users()
    impact = all_impact()

    section("Data overview", "CSV remains the single source of truth for CampusLoop")
    rows = []
    for label, path, df in [
        ("Item listings", PATHS["listings"], listings),
        ("Sharing activities", PATHS["activities"], activities),
        ("Users", PATHS["users"], members),
        ("Impact", PATHS["impact"], impact),
    ]:
        modified = pd.Timestamp(_mtime(path), unit="s").strftime("%d %b %Y, %H:%M") if os.path.exists(path) else "missing"
        rows.append([
            esc(label),
            f'<span class="num">{len(df):,}</span>',
            f'<span class="cl-mono">{esc(os.path.relpath(path, BASE_DIR))}</span>',
            esc(modified),
        ])
    md(data_table(["Dataset", "Rows", "Path", "Last modified"], rows), unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        section("Presentation", "Applies immediately across the app")
        st.selectbox("Rows per page", [12, 16, 20, 24], key="page_size")
        st.checkbox("Reduce motion", key="reduce_motion", help="Disables ambient and hover animation.")
        md(
            '<p class="cl-note">CampusLoop renders in dark mode only by design. '
            'The template light theme is intentionally not exposed.</p>',
            unsafe_allow_html=True,
        )
        if st.button("Refresh cached data", key="settings_refresh", width="stretch"):
            invalidate()
            flash("Cache cleared — data reloaded from CSV.")
            st.rerun()

    with right:
        section("Export", "Download the current CSV datasets")
        e1, e2 = st.columns(2)
        with e1:
            st.download_button(
                "Listings CSV", _csv_bytes(listings), file_name="campusloop_item_listings.csv",
                mime="text/csv", key="dl_items", width="stretch",
            )
            st.download_button(
                "Users CSV", _csv_bytes(members), file_name="campusloop_users.csv",
                mime="text/csv", key="dl_users", width="stretch",
            )
        with e2:
            st.download_button(
                "Activities CSV", _csv_bytes(activities), file_name="campusloop_sharing_activities.csv",
                mime="text/csv", key="dl_acts", width="stretch",
            )
            st.download_button(
                "Impact CSV", _csv_bytes(impact), file_name="campusloop_impact.csv",
                mime="text/csv", key="dl_impact", width="stretch",
            )
        md(
            '<p class="cl-note">Exports are generated from the same Pandas frames rendered by the app.</p>',
            unsafe_allow_html=True,
        )

    section("About CampusLoop", "Share · Reuse · Save · Together")
    md(
        """
        <div class="cl-card cl-card-3d">
            <p style="margin:0 0 8px;color:var(--text-secondary)">
                CampusLoop is a campus resource-sharing platform for borrowing, lending, swapping and giving away
                items. Listings and sharing activities are owned by this student; users and impact datasets are
                read-only inputs.
            </p>
            <div class="cl-kv"><span class="k">Stack</span><span class="v">Python · Streamlit · Pandas · NumPy · Plotly</span></div>
            <div class="cl-kv"><span class="k">Persistence</span><span class="v">CSV files in data/</span></div>
            <div class="cl-kv"><span class="k">Visual system</span><span class="v">Template-derived glass UI, rebranded to CampusLoop</span></div>
            <div class="cl-kv"><span class="k">Matching</span><span class="v">Deterministic, rule-based, explainable</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
PAGES = {
    "Home": home_page,
    "Discover": discover_page,
    "My Listings": my_listings_page,
    "Sharing": sharing_page,
    "Users": users_page,
    "Impact": impact_page,
    "Analytics": analytics_page,
    "Smart Match": smart_match_page,
    "Settings": settings_page,
}


def main() -> None:
    inject_css(st.session_state.get("reduce_motion", False))
    md(
        '<div class="cl-orb cl-orb-1"></div>'
        '<div class="cl-orb cl-orb-2"></div>'
        '<div class="cl-orb cl-orb-3"></div>',
        unsafe_allow_html=True,
    )
    render_sidebar()
    render_flash()
    page = st.session_state.get("page", "Home")
    PAGES.get(page, home_page)()


if __name__ == "__main__":
    main()
