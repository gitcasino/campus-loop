"""CampusLoop theme — template-derived dark glass UI.

Keeps glass surfaces, deep-forest ambient background, emerald / gold luxury
palette, Outfit + Space Mono typography and spacing rhythm, while retargeting
the CSS variables to CampusLoop's brand palette.
"""

from __future__ import annotations

import base64
import os

import streamlit as st

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

:root {
    --emerald: #38D996;
    --emerald-light: #8CFF66;
    --gold: #D6A84F;
    --gold-light: #E8C9A0;
    --amber: #B45309;
    --coral: #E07A5F;
    --glass-bg: rgba(255, 255, 255, 0.05);
    --glass-border: rgba(255, 255, 255, 0.09);
    --glass-shadow: rgba(0, 0, 0, 0.35);
    --glass-hover: rgba(255, 255, 255, 0.075);
    --bg-dark: #050A0A;
    --bg-gradient-1: #061210;
    --bg-gradient-2: #0A1B16;
    --bg-gradient-3: #0D241C;
    --text-primary: #F4F7F5;
    --text-secondary: rgba(244, 247, 245, 0.72);
    --text-muted: rgba(244, 247, 245, 0.42);
    --success: #38D996;
    --warning: #E0B84F;
    --danger: #FF7A7A;
    --info: #5EC8FF;
    --border-radius: 20px;
    --card-padding: 22px;
    --transition-fast: 0.2s ease;
    --transition-normal: 0.3s ease;
}

html, body, [class*="css"], .stApp, .stMarkdown, .stButton, input, textarea, select {
    font-family: 'Outfit', system-ui, -apple-system, 'Segoe UI', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse 70% 50% at 18% 6%, rgba(56, 217, 150, 0.14), transparent 62%),
        radial-gradient(ellipse 58% 44% at 84% 74%, rgba(214, 168, 79, 0.10), transparent 62%),
        radial-gradient(ellipse 55% 40% at 44% 108%, rgba(140, 255, 102, 0.07), transparent 60%),
        linear-gradient(135deg, var(--bg-gradient-1) 0%, var(--bg-gradient-2) 48%, var(--bg-gradient-3) 100%);
    background-attachment: fixed;
    color: var(--text-primary);
}

/* Ambient floating orbs (template .orb system, kept lightweight: 3 elements) */
.cl-orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(95px);
    opacity: 0.30;
    z-index: -1;
    pointer-events: none;
    animation: cl-float 24s ease-in-out infinite;
}
.cl-orb-1 { width: 420px; height: 420px; background: var(--emerald); top: 4%; left: 16%; }
.cl-orb-2 { width: 360px; height: 360px; background: var(--gold); bottom: 2%; right: 6%; animation-delay: -8s; }
.cl-orb-3 { width: 320px; height: 320px; background: var(--coral); bottom: 18%; left: 34%; opacity: 0.16; animation-delay: -15s; }

@keyframes cl-float {
    0%, 100% { transform: translate(0, 0) scale(1); }
    25% { transform: translate(28px, -26px) scale(1.05); }
    50% { transform: translate(-22px, 18px) scale(0.96); }
    75% { transform: translate(16px, 10px) scale(1.02); }
}

/* ---------- Streamlit chrome ---------- */
[data-testid="stHeader"] { background: transparent; height: 0; }
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
#MainMenu, footer { display: none !important; }

.block-container {
    padding: 1.5rem 2.2rem 4rem;
    max-width: 1500px;
}
@media (max-width: 768px) {
    .block-container { padding: 1rem 0.9rem 3rem; }
}

[data-testid="stSidebar"] {
    width: 272px !important;
    min-width: 272px !important;
    background: rgba(9, 20, 17, 0.62) !important;
    border-right: 1px solid var(--glass-border);
    backdrop-filter: blur(26px);
    -webkit-backdrop-filter: blur(26px);
}
[data-testid="stSidebarContent"] { padding: 0.9rem 0.85rem 1rem; }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 0.18rem; }
[data-testid="stSidebarCollapsedControl"] {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    color: var(--text-primary);
}
[data-testid="stSidebar"]::-webkit-scrollbar { width: 6px; }
[data-testid="stSidebar"]::-webkit-scrollbar-thumb { background: var(--glass-border); border-radius: 3px; }

/* ---------- Sidebar brand + nav ---------- */
.cl-brand {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 0.35rem 0.55rem 1rem;
    margin-bottom: 0.7rem;
    border-bottom: 1px solid var(--glass-border);
}
.cl-brand-logo { width: 100%; max-width: 178px; height: auto; display: block; }
.cl-brand-sub {
    font-size: 9.5px;
    letter-spacing: 0.26em;
    text-transform: uppercase;
    color: var(--text-muted);
}

.cl-nav-section {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 0.9rem 0.8rem 0.35rem;
}

[data-testid="stSidebar"] .stButton { margin: 0; }
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    justify-content: flex-start;
    text-align: left;
    background: transparent;
    border: 1px solid transparent;
    color: var(--text-secondary);
    border-radius: 11px;
    padding: 0.58rem 0.8rem;
    font-size: 13.5px;
    font-weight: 500;
    box-shadow: none;
    transition: background var(--transition-fast), color var(--transition-fast), border-color var(--transition-fast);
}
[data-testid="stSidebar"] .stButton > button p {
    font-size: 13.5px;
    font-weight: 500;
    color: inherit;
    margin: 0;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--glass-hover);
    border-color: var(--glass-border);
    color: var(--text-primary);
    transform: none;
    box-shadow: none;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(90deg, rgba(140, 255, 102, 0.13), rgba(255, 255, 255, 0.04));
    border: 1px solid rgba(140, 255, 102, 0.22);
    color: var(--text-primary);
    box-shadow: inset 2px 0 0 var(--emerald-light);
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] p { color: var(--text-primary); }

.cl-side-foot {
    margin-top: 1.1rem;
    padding: 0.85rem 0.7rem 0.2rem;
    border-top: 1px solid var(--glass-border);
}
.cl-side-foot .cl-user-name { font-size: 13px; font-weight: 600; }
.cl-side-foot .cl-user-email { font-size: 11px; color: var(--text-muted); }

/* ---------- Typography ---------- */
h1, h2, h3, h4, h5, h6 { color: var(--text-primary); font-weight: 600; }
p, li, span, label { color: var(--text-secondary); }
a { color: var(--emerald-light); }
hr { border-color: var(--glass-border); }

/* ---------- Page header ---------- */
.cl-page-head {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 18px;
    margin: 0.2rem 0 1.4rem;
}
.cl-page-title { font-size: 30px; line-height: 1.1; font-weight: 600; margin: 0 0 6px; }
.cl-breadcrumb {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12.5px;
    color: var(--text-muted);
}
.cl-breadcrumb .sep { opacity: 0.5; }
.cl-breadcrumb .current { color: var(--text-secondary); }
.cl-page-kicker {
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--emerald-light);
    font-weight: 600;
    margin-bottom: 8px;
}

/* ---------- Hero ---------- */
.cl-hero {
    position: relative;
    overflow: hidden;
    border: 1px solid var(--glass-border);
    border-radius: 26px;
    padding: 36px 38px;
    margin-bottom: 1.3rem;
    background:
        radial-gradient(ellipse 70% 90% at 12% 10%, rgba(56, 217, 150, 0.18), transparent 60%),
        radial-gradient(ellipse 60% 80% at 92% 88%, rgba(214, 168, 79, 0.14), transparent 62%),
        linear-gradient(135deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.025));
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);
    box-shadow: 0 30px 70px -40px rgba(0, 0, 0, 0.9);
}
.cl-hero::before {
    content: '';
    position: absolute;
    inset: 0 auto auto 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.24), transparent);
}
.cl-hero-grid {
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 30px;
    align-items: center;
    position: relative;
    z-index: 1;
}
.cl-hero h1 {
    font-size: 42px;
    line-height: 1.06;
    margin: 10px 0 14px;
    background: linear-gradient(120deg, #FFFFFF 5%, #B8FF9A 52%, #E8C9A0 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
}
.cl-hero p { font-size: 15.5px; line-height: 1.65; max-width: 56ch; margin: 0; }
.cl-hero-art {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 26px;
    border-radius: 20px;
    border: 1px solid var(--glass-border);
    background: linear-gradient(135deg, rgba(56, 217, 150, 0.10), rgba(214, 168, 79, 0.08));
    transform: rotate(-1.5deg);
    box-shadow: 0 24px 50px -28px rgba(0, 0, 0, 0.85);
}
.cl-hero-art img { width: 100%; max-width: 330px; height: auto; display: block; }
.cl-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 18px; }
.cl-chip {
    font-size: 10.5px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-weight: 600;
    color: var(--text-secondary);
    padding: 7px 12px;
    border-radius: 999px;
    border: 1px solid var(--glass-border);
    background: rgba(255, 255, 255, 0.04);
}
.cl-chip em { color: var(--emerald-light); font-style: normal; }

/* ---------- Glass primitives ---------- */
.cl-card {
    position: relative;
    overflow: hidden;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: var(--border-radius);
    padding: var(--card-padding);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    transition: background var(--transition-normal), border-color var(--transition-normal), box-shadow var(--transition-normal), transform 0.4s cubic-bezier(0.03, 0.98, 0.52, 0.99);
}
.cl-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
}
.cl-card:hover {
    background: var(--glass-hover);
    border-color: rgba(255, 255, 255, 0.15);
    box-shadow: 0 25px 50px -12px var(--glass-shadow), 0 0 40px rgba(56, 217, 150, 0.08);
}
.cl-card-3d:hover {
    transform: perspective(1000px) rotateX(4deg) rotateY(-4deg) translateZ(8px);
}

.cl-section-head {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 16px;
    margin: 1.6rem 0 0.9rem;
}
.cl-section-title { font-size: 19px; font-weight: 600; margin: 0; }
.cl-section-sub { font-size: 12.5px; color: var(--text-muted); margin: 3px 0 0; }
.cl-grid { display: grid; gap: 16px; margin-bottom: 0.6rem; }
.cl-grid-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.cl-grid-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.cl-grid-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }

/* ---------- Stat cards ---------- */
.cl-stat-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 0.4rem;
}
.cl-stat {
    position: relative;
    overflow: hidden;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 18px;
    padding: 18px 20px;
    backdrop-filter: blur(18px);
    transition: background var(--transition-normal), border-color var(--transition-normal), box-shadow var(--transition-normal);
}
.cl-stat:hover {
    background: var(--glass-hover);
    border-color: rgba(255, 255, 255, 0.16);
    box-shadow: 0 20px 40px -18px var(--glass-shadow);
}
.cl-stat-label {
    font-size: 10.5px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-muted);
    font-weight: 600;
}
.cl-stat-row { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
.cl-stat-value {
    font-family: 'Space Mono', monospace;
    font-size: 26px;
    font-weight: 700;
    line-height: 1.15;
    margin: 8px 0 4px;
    background: linear-gradient(135deg, #FFFFFF, var(--text-secondary));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
}
.cl-stat-sub { font-size: 11.5px; color: var(--text-muted); }
.cl-stat-icon {
    width: 42px; height: 42px;
    border-radius: 13px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    background: rgba(56, 217, 150, 0.12);
    color: var(--emerald-light);
}
.cl-stat-icon.gold { background: rgba(214, 168, 79, 0.14); color: var(--gold-light); }
.cl-stat-icon.coral { background: rgba(224, 122, 95, 0.14); color: #FFB4A0; }
.cl-stat-icon.info { background: rgba(94, 200, 255, 0.14); color: var(--info); }
.cl-stat-icon svg { width: 20px; height: 20px; }

/* ---------- Listing cards ---------- */
.cl-listing {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 9px;
    min-height: 196px;
    padding: 18px;
    border-radius: 18px;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(18px);
    transition: background var(--transition-normal), border-color var(--transition-normal), box-shadow var(--transition-normal), transform 0.35s ease;
}
.cl-listing:hover {
    background: var(--glass-hover);
    border-color: rgba(140, 255, 102, 0.24);
    box-shadow: 0 24px 44px -22px rgba(0, 0, 0, 0.9), 0 0 34px rgba(140, 255, 102, 0.07);
    transform: translateY(-3px);
}
.cl-listing-top { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.cl-eyebrow {
    font-size: 10px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-muted);
    font-weight: 600;
}
.cl-listing-title { font-size: 15.5px; font-weight: 600; line-height: 1.32; margin: 0; min-height: 41px; }
.cl-listing-meta { font-size: 12px; color: var(--text-muted); display: flex; flex-wrap: wrap; gap: 6px; }
.cl-listing-foot { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-top: auto; padding-top: 4px; }
.cl-price { font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; color: var(--emerald-light); }
.cl-listing-sub { font-size: 11px; color: var(--text-muted); }
.cl-listing-id { font-family: 'Space Mono', monospace; font-size: 10px; color: rgba(244, 247, 245, 0.28); }

/* ---------- Mode tags + status badges ---------- */
.cl-tag {
    display: inline-flex;
    align-items: center;
    font-size: 9.5px;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    font-weight: 700;
    padding: 4px 9px;
    border-radius: 7px;
    white-space: nowrap;
}
.cl-tag.borrow { background: rgba(94, 200, 255, 0.15); color: #8FDBFF; }
.cl-tag.swap { background: rgba(140, 255, 102, 0.15); color: var(--emerald-light); }
.cl-tag.giveaway { background: rgba(56, 217, 150, 0.15); color: #7FE9BC; }
.cl-tag.sell { background: rgba(214, 168, 79, 0.18); color: var(--gold-light); }

.cl-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    white-space: nowrap;
}
.cl-badge::before {
    content: '';
    width: 5px; height: 5px;
    border-radius: 50%;
    background: currentColor;
    box-shadow: 0 0 8px currentColor;
}
.cl-badge.ok { color: var(--success); background: rgba(56, 217, 150, 0.14); }
.cl-badge.warn { color: var(--gold-light); background: rgba(214, 168, 79, 0.16); }
.cl-badge.info { color: var(--info); background: rgba(94, 200, 255, 0.14); }
.cl-badge.danger { color: var(--danger); background: rgba(255, 122, 122, 0.14); }
.cl-badge.muted { color: var(--text-muted); background: rgba(255, 255, 255, 0.06); }

/* ---------- Tables ---------- */
.cl-table-wrap {
    overflow-x: auto;
    border: 1px solid var(--glass-border);
    border-radius: 18px;
    background: var(--glass-bg);
    backdrop-filter: blur(18px);
    padding: 2px 14px 6px;
    margin-bottom: 0.6rem;
}
.cl-table { width: 100%; min-width: 760px; border-collapse: collapse; }
.cl-table th, .cl-table td { padding: 13px 12px; text-align: left; }
.cl-table th {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    border-bottom: 1px solid var(--glass-border);
    white-space: nowrap;
}
.cl-table td {
    font-size: 12.8px;
    color: var(--text-secondary);
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    vertical-align: middle;
}
.cl-table tbody tr { transition: background var(--transition-fast); }
.cl-table tbody tr:hover { background: var(--glass-hover); }
.cl-table tbody tr:last-child td { border-bottom: none; }
.cl-table .num { font-family: 'Space Mono', monospace; color: var(--text-primary); font-weight: 600; white-space: nowrap; }
.cl-mono { font-family: 'Space Mono', monospace; font-size: 11px; color: var(--text-muted); }
.cl-user { display: flex; align-items: center; gap: 11px; min-width: 0; }
.cl-avatar {
    width: 34px; height: 34px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700;
    font-size: 11.5px;
    color: #04110B;
    flex-shrink: 0;
}
.cl-user-name { color: var(--text-primary); font-weight: 500; font-size: 13px; }
.cl-user-email { color: var(--text-muted); font-size: 11px; }

/* ---------- Activity feed ---------- */
.cl-feed {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: var(--border-radius);
    padding: 10px 20px;
    backdrop-filter: blur(18px);
}
.cl-feed-item {
    display: flex;
    align-items: flex-start;
    gap: 13px;
    padding: 13px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.cl-feed-item:last-child { border-bottom: none; }
.cl-feed-text { font-size: 13px; color: var(--text-secondary); }
.cl-feed-text strong { color: var(--text-primary); font-weight: 500; }
.cl-feed-time { font-size: 11px; color: var(--text-muted); margin-top: 2px; display: block; }

/* ---------- Detail ---------- */
.cl-detail {
    background: linear-gradient(135deg, rgba(56, 217, 150, 0.07), rgba(255, 255, 255, 0.035));
    border: 1px solid var(--glass-border);
    border-radius: var(--border-radius);
    padding: 24px;
    backdrop-filter: blur(20px);
}
.cl-detail h3 { font-size: 21px; margin: 0 0 4px; }
.cl-detail-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 14px; margin-bottom: 6px; }
.cl-meta-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin-top: 16px; }
.cl-meta {
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 10px 12px;
}
.cl-meta span {
    display: block;
    font-size: 9.5px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 4px;
}
.cl-meta strong { font-size: 13px; color: var(--text-primary); font-weight: 500; }

/* ---------- Match cards ---------- */
.cl-match-score {
    font-family: 'Space Mono', monospace;
    font-size: 19px;
    font-weight: 700;
    color: var(--emerald-light);
    white-space: nowrap;
}
.cl-bar { height: 5px; border-radius: 999px; background: rgba(255, 255, 255, 0.09); overflow: hidden; margin: 4px 0 10px; }
.cl-bar-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--emerald), var(--emerald-light)); box-shadow: 0 0 14px rgba(140, 255, 102, 0.4); }
.cl-reasons { display: flex; flex-wrap: wrap; gap: 6px; }
.cl-reason {
    font-size: 10.5px;
    color: var(--text-secondary);
    padding: 4px 9px;
    border-radius: 999px;
    border: 1px solid var(--glass-border);
    background: rgba(255, 255, 255, 0.04);
}
.cl-reason b { color: var(--emerald-light); font-weight: 600; }

/* ---------- Misc ---------- */
.cl-empty {
    border: 1px dashed rgba(255, 255, 255, 0.16);
    border-radius: 18px;
    padding: 42px 22px;
    text-align: center;
    background: rgba(255, 255, 255, 0.02);
}
.cl-empty h4 { margin: 0 0 6px; font-size: 16px; }
.cl-empty p { margin: 0; font-size: 13px; color: var(--text-muted); }
.cl-note { font-size: 12px; color: var(--text-muted); }
.cl-pager-text { font-family: 'Space Mono', monospace; font-size: 12px; color: var(--text-muted); text-align: center; padding-top: 9px; }
.cl-kv { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 11px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05); font-size: 13px; }
.cl-kv:last-child { border-bottom: none; }
.cl-kv .k { color: var(--text-muted); }
.cl-kv .v { color: var(--text-primary); font-weight: 500; text-align: right; }

/* ---------- Native Streamlit widgets ---------- */
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
    border-radius: 12px;
    border: 1px solid var(--glass-border);
    background: var(--glass-bg);
    color: var(--text-primary);
    font-family: 'Outfit', sans-serif;
    font-weight: 500;
    font-size: 13.5px;
    padding: 0.55rem 1.05rem;
    transition: all var(--transition-fast);
    box-shadow: none;
}
.stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
    background: var(--glass-hover);
    border-color: var(--emerald-light);
    color: var(--text-primary);
    transform: translateY(-1px);
}
.stButton > button p, .stDownloadButton > button p, [data-testid="stFormSubmitButton"] > button p {
    color: inherit;
    font-size: 13.5px;
    font-weight: inherit;
}
.stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, var(--emerald), var(--emerald-light));
    border: none;
    color: #04110B;
    font-weight: 600;
    box-shadow: 0 8px 24px rgba(56, 217, 150, 0.26);
}
.stButton > button[kind="primary"]:hover, [data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
    box-shadow: 0 12px 30px rgba(56, 217, 150, 0.36);
    color: #04110B;
}
.stButton > button[kind="primary"] p, [data-testid="stFormSubmitButton"] > button[kind="primary"] p { color: #04110B; }

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stTextArea"] textarea {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 11px !important;
    color: var(--text-primary) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13.5px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stDateInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--emerald-light) !important;
    box-shadow: 0 0 0 1px rgba(140, 255, 102, 0.5), 0 0 20px rgba(140, 255, 102, 0.12) !important;
}
[data-testid="stNumberInput"] button {
    background: rgba(255, 255, 255, 0.04);
    border-color: var(--glass-border);
    color: var(--text-secondary);
}
[data-baseweb="select"] > div {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 11px !important;
    color: var(--text-primary) !important;
    min-height: 42px;
}
[data-baseweb="select"] > div:focus-within {
    border-color: var(--emerald-light) !important;
    box-shadow: 0 0 0 1px rgba(140, 255, 102, 0.4);
}
[data-baseweb="select"] svg { color: var(--text-muted); }
[data-baseweb="popover"] div[role="listbox"] {
    background: #0B1714 !important;
    border: 1px solid var(--glass-border);
    border-radius: 12px;
}
[data-baseweb="popover"] li { color: var(--text-secondary) !important; font-size: 13px; }
[data-baseweb="popover"] li:hover { background: rgba(140, 255, 102, 0.10) !important; }
[data-baseweb="menu"] { background: #0B1714 !important; }

label[data-testid="stWidgetLabel"] p {
    font-size: 12px !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    letter-spacing: 0.01em;
}
[data-testid="stWidgetLabel"] { margin-bottom: 2px; }

[data-testid="stForm"] {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 18px;
    padding: 20px;
    backdrop-filter: blur(18px);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    padding: 5px;
}
.stTabs [data-baseweb="tab"] {
    height: auto;
    padding: 8px 16px;
    border-radius: 10px;
    color: var(--text-muted);
    font-size: 13px;
}
.stTabs [aria-selected="true"] { background: var(--glass-hover); color: var(--text-primary); }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

[data-testid="stExpander"] {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    overflow: hidden;
}
[data-testid="stExpander"] summary { font-size: 13.5px; color: var(--text-secondary); }

[data-testid="stAlert"] {
    border-radius: 14px;
    border: 1px solid var(--glass-border);
    background: var(--glass-bg);
}

[data-testid="stPlotlyChart"] {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 18px;
    padding: 10px 8px 4px;
    backdrop-filter: blur(18px);
}
[data-testid="stPlotlyChart"] .modebar { display: none !important; }

[data-testid="stDataFrame"] {
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    overflow: hidden;
}

.stCheckbox p, .stRadio p { font-size: 13px; color: var(--text-secondary); }
[data-testid="stCaptionContainer"] p { color: var(--text-muted); font-size: 12px; }

/* ---------- Scrollbars ---------- */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.03); }
::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.14); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(140, 255, 102, 0.35); }

/* ---------- Responsive ---------- */
@media (max-width: 1200px) {
    .cl-stat-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .cl-grid-4 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .cl-grid-3 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .cl-hero-grid { grid-template-columns: 1fr; }
    .cl-hero-art { max-width: 420px; }
    .cl-meta-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 860px) {
    .cl-grid-2, .cl-grid-3 { grid-template-columns: 1fr; }
    .cl-page-title { font-size: 24px; }
    .cl-hero { padding: 26px 22px; }
    .cl-hero h1 { font-size: 33px; }
}
@media (max-width: 640px) {
    .cl-stat-grid { grid-template-columns: 1fr; }
    .cl-grid-4 { grid-template-columns: 1fr; }
    .cl-page-head { flex-direction: column; align-items: flex-start; }
    .cl-meta-grid { grid-template-columns: 1fr; }
    .cl-hero h1 { font-size: 28px; }
    .cl-hero p { font-size: 14px; }
}

/* ---------- Reduced motion ---------- */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.001ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.001ms !important;
    }
}
.cl-reduce-motion *, .cl-reduce-motion *::before, .cl-reduce-motion *::after {
    animation: none !important;
    transition: none !important;
}
"""


def img_data_uri(path: str) -> str:
    """Return a data URI for a local asset so Streamlit always resolves it."""
    try:
        with open(path, "rb") as handle:
            payload = base64.b64encode(handle.read()).decode("ascii")
    except OSError:
        return ""
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = {
        "svg": "image/svg+xml",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "webp": "image/webp",
        "ico": "image/x-icon",
    }.get(ext, "application/octet-stream")
    return f"data:{mime};base64,{payload}"


def inject_css(reduce_motion: bool = False) -> None:
    """Inject the template-derived stylesheet plus optional motion override."""
    extra = ""
    if reduce_motion:
        extra = (
            "<style>.stApp *, .stApp *::before, .stApp *::after"
            " { animation: none !important; transition: none !important; }</style>"
        )
    st.markdown(f"<style>{CSS}</style>{extra}", unsafe_allow_html=True)
