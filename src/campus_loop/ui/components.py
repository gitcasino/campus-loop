"""Reusable HTML building blocks for the CampusLoop glass UI.

Every custom block is emitted as one self-contained HTML string so Streamlit
never leaves unclosed markup behind (which previously leaked into the page).
"""

from __future__ import annotations

import html
import re
from typing import Iterable, Sequence

import pandas as pd
import streamlit as st

from .theme import img_data_uri

_ICONS = {
    "listings": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
    "activities": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>',
    "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "value": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>',
    "swap": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
}

_AVATAR_GRADIENTS = [
    "linear-gradient(135deg, #8CFF66, #38D996)",
    "linear-gradient(135deg, #E8C9A0, #D6A84F)",
    "linear-gradient(135deg, #7FE9BC, #38D996)",
    "linear-gradient(135deg, #FFB4A0, #E07A5F)",
    "linear-gradient(135deg, #8FDBFF, #38D996)",
    "linear-gradient(135deg, #B8FF9A, #D6A84F)",
]

_KIND_BY_STATUS = {
    "AVAILABLE": "ok",
    "ACTIVE": "ok",
    "COMPLETED": "ok",
    "ON_TIME": "ok",
    "RETURNED": "ok",
    "BORROWED": "info",
    "RESERVED": "warn",
    "PROCESSING": "info",
    "PENDING": "warn",
    "OVERDUE": "danger",
    "LATE": "danger",
    "CANCELLED": "danger",
    "INACTIVE": "muted",
    "NA": "muted",
}

_MODE_CLASS = {"BORROW": "borrow", "SWAP": "swap", "GIVEAWAY": "giveaway", "SELL": "sell"}


_WHITESPACE = re.compile(r"\s+")


def compact(markup: str) -> str:
    """Collapse an HTML block onto one line.

    Streamlit's Markdown renderer ends an HTML block at a blank line and treats
    four-space-indented lines as code, so indented multi-line markup leaks its
    tags to the page. One-line markup is always parsed as a single HTML block.
    """
    return _WHITESPACE.sub(" ", markup).strip()


def esc_attr(value: object) -> str:
    """Escape an HTML attribute, preserving intentionally empty strings."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return html.escape(str(value))


def esc(value: object) -> str:
    """Escape any value for safe HTML interpolation."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "—"
    text = str(value)
    if text.strip() == "" or text.lower() == "nan":
        return "—"
    return html.escape(text)


def fmt_inr(value: object) -> str:
    """Format a rupee value compactly."""
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return "₹0"
    if amount >= 10_000_000:
        return f"₹{amount / 10_000_000:.2f}Cr"
    if amount >= 100_000:
        return f"₹{amount / 100_000:.2f}L"
    if amount >= 1_000:
        return f"₹{amount / 1_000:.1f}k"
    return f"₹{amount:,.0f}"


def initials(name: str) -> str:
    clean = str(name or "?").strip()
    if not clean:
        return "?"
    parts = [p for p in clean.replace(".", " ").split() if p]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def avatar(name: str) -> str:
    gradient = _AVATAR_GRADIENTS[sum(ord(c) for c in str(name)) % len(_AVATAR_GRADIENTS)]
    return f'<div class="cl-avatar" style="background:{gradient}">{esc(initials(name))}</div>'


def mode_tag(mode: object) -> str:
    text = str(mode or "").upper()
    css = _MODE_CLASS.get(text, "swap")
    return f'<span class="cl-tag {css}">{esc(text)}</span>'


def badge(status: object) -> str:
    text = str(status or "").upper()
    kind = _KIND_BY_STATUS.get(text, "muted")
    return f'<span class="cl-badge {kind}">{esc(text)}</span>'


def page_header(title: str, subtitle: str = "", section: str = "") -> str:
    crumb = f'<span class="sep">/</span><span class="current">{esc(section or title)}</span>' if (section or title) else ""
    sub = f'<p class="cl-section-sub" style="margin-top:6px">{esc(subtitle)}</p>' if subtitle else ""
    return compact(f"""
    <div class="cl-page-head">
        <div>
            <div class="cl-page-kicker">CampusLoop</div>
            <h1 class="cl-page-title">{esc(title)}</h1>
            <div class="cl-breadcrumb"><span>CampusLoop</span>{crumb}</div>
            {sub}
        </div>
    </div>
    """)


def hero(image_uri: str) -> str:
    return compact(f"""
    <section class="cl-hero">
        <div class="cl-hero-grid">
            <div>
                <div class="cl-eyebrow">Campus circular economy</div>
                <h1>Everything on campus, already in circulation.</h1>
                <p>Borrow what you need, lend what you don't, swap what you've outgrown and give away what
                someone else can use. CampusLoop keeps useful items moving through your campus community.</p>
                <div class="cl-chips">
                    <span class="cl-chip"><em>Borrow</em> &middot; Lend</span>
                    <span class="cl-chip"><em>Swap</em> &middot; Exchange</span>
                    <span class="cl-chip"><em>Give away</em> &middot; Reuse</span>
                </div>
            </div>
            <div class="cl-hero-art">
                <img class="cl-hero-photo" src="{image_uri}"
                     alt="CampusLoop community sharing everyday campus items" />
            </div>
        </div>
    </section>
    """)


def stat_cards(items: Sequence[tuple]) -> str:
    """Static stat cards. Each item: (label, value, sub, tone, icon)."""
    cards = []
    for label, value, sub, tone, icon in items:
        cards.append(
            f"""
            <div class="cl-stat">
                <div class="cl-stat-row">
                    <div>
                        <div class="cl-stat-label">{esc(label)}</div>
                        <div class="cl-stat-value">{esc(value)}</div>
                        <div class="cl-stat-sub">{esc(sub)}</div>
                    </div>
                    <div class="cl-stat-icon {esc(tone)}">{_ICONS.get(icon, _ICONS['listings'])}</div>
                </div>
            </div>
            """
        )
    return compact(f'<div class="cl-stat-grid">{"".join(cards)}</div>')


_STAT_FRAME_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600&family=Space+Mono:wght@400;700&display=swap');
* { box-sizing: border-box; }
html, body {
    margin: 0;
    background: transparent;
    font-family: 'Outfit', system-ui, sans-serif;
    color: #F4F7F5;
}
.stats {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
}
.stat {
    position: relative;
    overflow: hidden;
    padding: 14px 16px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.09);
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(18px);
    transition: background .3s ease, border-color .3s ease, transform .35s ease;
    transform-style: preserve-3d;
    min-height: 118px;
}
.stat:hover {
    background: rgba(255, 255, 255, 0.075);
    border-color: rgba(140, 255, 102, 0.22);
    box-shadow: 0 18px 36px -18px rgba(0, 0, 0, 0.85);
}
.label {
    font-size: 9.5px;
    letter-spacing: .14em;
    text-transform: uppercase;
    font-weight: 600;
    color: rgba(244, 247, 245, 0.42);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.value {
    font-family: 'Space Mono', monospace;
    font-size: 22px;
    font-weight: 700;
    margin: 7px 0 3px;
    background: linear-gradient(135deg, #FFFFFF, rgba(244, 247, 245, 0.7));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    white-space: nowrap;
}
.sub {
    font-size: 10.5px;
    color: rgba(244, 247, 245, 0.42);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.icon {
    position: absolute;
    top: 12px;
    right: 12px;
    width: 30px;
    height: 30px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #8CFF66;
    background: rgba(56, 217, 150, 0.12);
}
.icon.gold { color: #E8C9A0; background: rgba(214, 168, 79, 0.14); }
.icon.coral { color: #FFB4A0; background: rgba(224, 122, 95, 0.14); }
.icon.info { color: #5EC8FF; background: rgba(94, 200, 255, 0.14); }
.icon svg { width: 15px; height: 15px; }
@media (max-width: 760px) {
    .stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .value { font-size: 19px; }
}
@media (prefers-reduced-motion: reduce) {
    .stat { transition: none; }
}
"""

_LIGHT_STAT_FRAME_CSS = """
html, body { color: #10241C; }
.stat {
    background: rgba(255, 255, 255, 0.56);
    border-color: rgba(18, 66, 48, 0.13);
}
.stat:hover {
    background: rgba(255, 255, 255, 0.82);
    border-color: rgba(14, 159, 110, 0.30);
    box-shadow: 0 20px 40px -22px rgba(22, 52, 40, 0.4);
}
.label, .sub { color: rgba(16, 36, 28, 0.52); }
.value {
    background: linear-gradient(135deg, #10241C 16%, #0B7A52 78%, #A9791F 108%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.icon { color: #0B7A52; background: rgba(14, 159, 110, 0.12); }
.icon.gold { color: #8A6218; background: rgba(169, 121, 31, 0.13); }
.icon.coral { color: #C0563D; background: rgba(192, 86, 61, 0.12); }
.icon.info { color: #1D7FB8; background: rgba(29, 127, 184, 0.12); }
"""


_STAT_FRAME_JS = """
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var values = document.querySelectorAll('.value');
  values.forEach(function (el) {
    var target = parseFloat(el.dataset.target || '0');
    var prefix = el.dataset.prefix || '';
    var suffix = el.dataset.suffix || '';
    var decimals = parseInt(el.dataset.decimals || '0', 10);
    if (reduce || !isFinite(target)) {
      el.textContent = prefix + Number(target).toLocaleString(undefined, {minimumFractionDigits: decimals, maximumFractionDigits: decimals}) + suffix;
      return;
    }
    var start = performance.now();
    var duration = 1400;
    function tick(now) {
      var p = Math.min((now - start) / duration, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      var current = target * eased;
      el.textContent = prefix + current.toLocaleString(undefined, {minimumFractionDigits: decimals, maximumFractionDigits: decimals}) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
  if (!reduce && window.matchMedia('(pointer: fine)').matches) {
    document.querySelectorAll('.stat').forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var r = card.getBoundingClientRect();
        var rx = ((e.clientY - r.top) - r.height / 2) / 24;
        var ry = (r.width / 2 - (e.clientX - r.left)) / 24;
        card.style.transform = 'perspective(900px) rotateX(' + rx + 'deg) rotateY(' + ry + 'deg) translateZ(6px)';
      });
      card.addEventListener('mouseleave', function () {
        card.style.transform = 'perspective(900px) rotateX(0deg) rotateY(0deg) translateZ(0)';
      });
    });
  }
})();
"""


def stat_grid_frame(items: Sequence[tuple]) -> str:
    """Animated, 3D-tilting stat grid for a components.html iframe.

    Each item: (label, numeric_target, sub, tone, icon, prefix, suffix, decimals)
    """
    cards = []
    for label, target, sub, tone, icon, prefix, suffix, decimals in items:
        cards.append(
            f"""
            <div class="stat">
                <div class="label">{esc(label)}</div>
                <div class="value" data-target="{esc_attr(target)}" data-prefix="{esc_attr(prefix)}"
                     data-suffix="{esc_attr(suffix)}" data-decimals="{int(decimals)}">0</div>
                <div class="sub">{esc_attr(sub)}</div>
                <div class="icon {esc_attr(tone)}">{_ICONS.get(icon, _ICONS['listings'])}</div>
            </div>
            """
        )
    try:
        light = st.session_state.get("theme", "dark") == "light"
    except Exception:
        light = False
    frame_css = _STAT_FRAME_CSS + (_LIGHT_STAT_FRAME_CSS if light else "")
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'><style>"
        + frame_css
        + "</style></head><body><div class='stats'>"
        + "".join(cards)
        + "</div><script>"
        + _STAT_FRAME_JS
        + "</script></body></html>"
    )


def listing_cards(df: pd.DataFrame, cols: int = 3) -> str:
    if df is None or df.empty:
        return empty_state("No listings found", "Try widening your filters or create a new listing.")
    cards = []
    for _, row in df.iterrows():
        cards.append(
            f"""
            <article class="cl-listing">
                <div class="cl-listing-top">
                    <span class="cl-eyebrow">{esc(row.get('category'))}</span>
                    {mode_tag(row.get('sharing_mode'))}
                </div>
                <h3 class="cl-listing-title">{esc(row.get('title'))}</h3>
                <div class="cl-listing-meta">
                    <span>{esc(row.get('condition'))} condition</span>
                    <span>&middot;</span>
                    <span>{esc(row.get('pickup_location'))}</span>
                </div>
                <div class="cl-listing-foot">
                    <span class="cl-price">{fmt_inr(row.get('estimated_value_inr'))}</span>
                    {badge(row.get('status'))}
                </div>
                <div class="cl-listing-sub">Owner {esc(row.get('owner_user_id'))} &middot; until {esc(row.get('available_until'))}</div>
                <div class="cl-listing-id">{esc(row.get('item_id'))}</div>
            </article>
            """
        )
    return compact(f'<div class="cl-grid cl-grid-{max(1, min(cols, 4))}">{"".join(cards)}</div>')


def activity_feed(df: pd.DataFrame) -> str:
    if df is None or df.empty:
        return empty_state("No activity yet", "Recorded sharing activity will appear here.")
    items = []
    for _, row in df.iterrows():
        items.append(
            f"""
            <div class="cl-feed-item">
                {avatar(row.get('borrower_user_id'))}
                <div>
                    <div class="cl-feed-text"><strong>{esc(row.get('borrower_user_id'))}</strong>
                        {esc(str(row.get('activity_type', '')).title())} &middot; {mode_tag(row.get('activity_type'))}
                        &middot; item {esc(row.get('item_id'))}</div>
                    <span class="cl-feed-time">{esc(row.get('start_date'))} &rarr; {esc(row.get('due_date'))} &middot; {esc(row.get('activity_status'))}</span>
                </div>
            </div>
            """
        )
    return compact(f'<div class="cl-feed">{"".join(items)}</div>')


def data_table(headers: Sequence[str], rows: Iterable[Sequence[str]]) -> str:
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return compact(f'<div class="cl-table-wrap"><table class="cl-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')


def user_rows(df: pd.DataFrame) -> str:
    rows = []
    for _, row in df.iterrows():
        user_cell = (
            f'<div class="cl-user">{avatar(row.get("name"))}<div>'
            f'<div class="cl-user-name">{esc(row.get("name"))}</div>'
            f'<div class="cl-user-email">{esc(row.get("email"))}</div></div></div>'
        )
        rows.append([
            user_cell,
            esc(row.get("department")),
            esc(row.get("year")),
            esc(row.get("joined_date")),
            badge(row.get("account_status")),
            f'<span class="cl-mono">{esc(row.get("user_id"))}</span>',
        ])
    return data_table(["User", "Department", "Year", "Joined", "Status", "ID"], rows)


def detail_card(row: pd.Series) -> str:
    return compact(f"""
    <div class="cl-detail">
        <div class="cl-detail-head">
            <div>
                <div class="cl-eyebrow">{esc(row.get('category'))} &middot; {esc(row.get('item_type'))}</div>
                <h3>{esc(row.get('title'))}</h3>
                <div class="cl-note">{esc(row.get('brand')) if str(row.get('brand', '')).strip() else 'Unbranded'} &middot; {esc(row.get('pickup_location'))}</div>
            </div>
            <div style="display:flex;gap:8px;align-items:center">{mode_tag(row.get('sharing_mode'))}{badge(row.get('status'))}</div>
        </div>
        <div class="cl-meta-grid">
            <div class="cl-meta"><span>Item ID</span><strong>{esc(row.get('item_id'))}</strong></div>
            <div class="cl-meta"><span>Owner</span><strong>{esc(row.get('owner_user_id'))}</strong></div>
            <div class="cl-meta"><span>Condition</span><strong>{esc(row.get('condition'))}</strong></div>
            <div class="cl-meta"><span>Value</span><strong>{fmt_inr(row.get('estimated_value_inr'))}</strong></div>
            <div class="cl-meta"><span>Listed</span><strong>{esc(row.get('listed_date'))}</strong></div>
            <div class="cl-meta"><span>Available until</span><strong>{esc(row.get('available_until'))}</strong></div>
            <div class="cl-meta"><span>Sharing mode</span><strong>{esc(row.get('sharing_mode'))}</strong></div>
            <div class="cl-meta"><span>Pickup</span><strong>{esc(row.get('pickup_location'))}</strong></div>
        </div>
    </div>
    """)


def empty_state(title: str, message: str) -> str:
    return compact(f'<div class="cl-empty"><h4>{esc(title)}</h4><p>{esc(message)}</p></div>')


def logo_uri(path: str) -> str:
    return img_data_uri(path)
