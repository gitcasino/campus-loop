"""CampusLoop theme — dark and light glass UI.

Glass surfaces, deep-forest ambient background, emerald / gold accents,
Outfit + Space Mono typography and a consistent spacing rhythm across themes.
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
    --violet: #A78BFA;
    --teal: #2DD4BF;
    --glass-bg: rgba(255, 255, 255, 0.055);
    --glass-border: rgba(255, 255, 255, 0.10);
    --glass-shadow: rgba(0, 0, 0, 0.38);
    --glass-hover: rgba(255, 255, 255, 0.085);
    --bg-dark: #050A0A;
    --bg-gradient-1: #061210;
    --bg-gradient-2: #0A1C18;
    --bg-gradient-3: #101F1A;
    --text-primary: #F4F7F5;
    --text-secondary: rgba(244, 247, 245, 0.72);
    --text-muted: rgba(244, 247, 245, 0.42);
    --popover-bg: #0B1714;
    --popover-border: rgba(255, 255, 255, 0.12);
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
.stApp [data-testid="stMarkdownContainer"] { font-family: 'Outfit', system-ui, -apple-system, sans-serif !important; }
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li { font-family: 'Outfit', system-ui, -apple-system, sans-serif !important; }
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
    font-family: 'Outfit', system-ui, -apple-system, sans-serif !important;
}

.stApp {
    background:
        radial-gradient(ellipse 62% 48% at 16% 4%, rgba(56, 217, 150, 0.17), transparent 64%),
        radial-gradient(ellipse 48% 42% at 88% 18%, rgba(94, 200, 255, 0.09), transparent 66%),
        radial-gradient(ellipse 52% 46% at 82% 82%, rgba(214, 168, 79, 0.12), transparent 64%),
        radial-gradient(ellipse 46% 38% at 38% 96%, rgba(167, 139, 250, 0.10), transparent 66%),
        radial-gradient(ellipse 40% 34% at 58% 48%, rgba(45, 212, 191, 0.06), transparent 70%),
        linear-gradient(135deg, var(--bg-gradient-1) 0%, var(--bg-gradient-2) 46%, var(--bg-gradient-3) 100%);
    background-attachment: fixed;
    color: var(--text-primary);
}

/* Ambient floating orbs (kept lightweight) */
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
.cl-orb-4 { width: 380px; height: 380px; background: var(--violet); top: 28%; right: 22%; opacity: 0.13; animation-delay: -19s; }

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
    padding: 5.1rem 2.2rem 4rem;
    max-width: 1500px;
}
@media (max-width: 768px) {
    .block-container { padding: 4.2rem 0.9rem 3rem; }
}

[data-testid="stSidebar"] {
    width: 272px !important;
    min-width: 272px !important;
    height: 100vh !important;
    background: rgba(9, 20, 17, 0.62) !important;
    border-right: 1px solid var(--glass-border);
    backdrop-filter: blur(26px);
    -webkit-backdrop-filter: blur(26px);
}
[data-testid="stSidebarContent"] { padding: 0.9rem 0.85rem 1rem; overflow: hidden; }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 0.18rem; }
[data-testid="stSidebarHeader"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebar"] { display: none !important; }

/* ---------- Floating sticky application navbar ---------- */
.st-key-app_topbar {
    position: fixed;
    width: auto !important;
    top: 10px;
    left: 14px;
    right: 14px;
    z-index: 1000;
    padding: 8px 12px;
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 18px;
    background:
        linear-gradient(180deg, rgba(255, 255, 255, 0.075), rgba(255, 255, 255, 0.02)),
        rgba(9, 20, 17, 0.54);
    backdrop-filter: blur(42px) saturate(165%);
    -webkit-backdrop-filter: blur(42px) saturate(165%);
    box-shadow: 0 24px 56px -24px rgba(0, 0, 0, 0.62), inset 0 1px 0 rgba(255, 255, 255, 0.10);
}
.st-key-app_topbar [data-testid="stHorizontalBlock"] { align-items: center; gap: 2px; }
.st-key-app_topbar [data-testid="stButton"] { display: flex; justify-content: center; }
.st-key-app_topbar [data-testid="stButton"] button {
    width: 100% !important;
    min-height: 38px;
    padding: 0.35rem 0.45rem;
    border-radius: 10px;
    border: 1px solid transparent;
    background: transparent;
    color: var(--text-secondary);
    font-size: 12.5px;
    font-weight: 500;
    box-shadow: none;
    white-space: nowrap;
    transition: background var(--transition-fast), border-color var(--transition-fast), color var(--transition-fast), box-shadow 0.25s ease, transform 0.25s ease;
}
.st-key-app_topbar [data-testid="stButton"] button p {
    font-size: 12.5px;
    white-space: nowrap;
}
.st-key-app_topbar [data-testid="stButton"] button:hover {
    background: var(--glass-hover);
    border-color: var(--glass-border);
    color: var(--text-primary);
    transform: translateY(-1px);
    box-shadow: 0 12px 28px -10px rgba(56, 217, 150, 0.70), 0 0 26px rgba(56, 217, 150, 0.28);
}
.st-key-app_topbar [data-testid="stButton"] button[kind="primary"] {
    background: rgba(140, 255, 102, 0.13);
    border-color: rgba(140, 255, 102, 0.30);
    color: var(--text-primary);
    box-shadow: none;
}
.st-key-app_topbar [data-testid="stButton"] button[kind="primary"]:hover {
    background: rgba(140, 255, 102, 0.16);
    border-color: rgba(140, 255, 102, 0.36);
    color: var(--text-primary);
    transform: translateY(-1px);
    box-shadow: 0 12px 30px -10px rgba(56, 217, 150, 0.72), 0 0 28px rgba(140, 255, 102, 0.26);
}
.st-key-app_topbar [data-testid="stButton"] button[kind="primary"] p { color: var(--text-primary); }
.cl-topbar-brand { display: flex; align-items: center; min-height: 38px; padding-left: 4px; transform: translateY(-8px); }
.cl-topbar-logo { height: 32px; width: auto; display: block; }
@media (max-width: 1100px) {
    .st-key-app_topbar [data-testid="stButton"] button { font-size: 11.5px; padding: 0.35rem 0.25rem; }
    .st-key-app_topbar [data-testid="stButton"] button p { font-size: 11.5px; }
}
@media (max-width: 900px) {
    .st-key-app_topbar { left: 8px; right: 8px; top: 8px; overflow-x: auto; }
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

[data-testid="stSidebar"] [data-testid="stButton"] { margin: 0; }
[data-testid="stSidebar"] [data-testid="stButton"] button {
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
    transition: background var(--transition-fast), color var(--transition-fast), border-color var(--transition-fast), transform var(--transition-fast), box-shadow var(--transition-fast);
}
[data-testid="stSidebar"] [data-testid="stButton"] button p {
    font-size: 13.5px;
    font-weight: 500;
    color: inherit;
    margin: 0;
}
[data-testid="stSidebar"] [data-testid="stButton"] button > div {
    justify-content: flex-start;
    width: 100%;
}
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"] > div { justify-content: flex-start; }
[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
    background: var(--glass-hover);
    border-color: var(--glass-border);
    color: var(--text-primary);
    transform: translateX(3px);
    box-shadow: 0 10px 24px -18px var(--glass-shadow);
}
[data-testid="stSidebar"] [data-testid="stButton"] button:active { transform: translateX(1px) scale(0.995); }
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(92deg, rgba(140, 255, 102, 0.16), rgba(56, 217, 150, 0.06) 48%, rgba(167, 139, 250, 0.07));
    border: 1px solid rgba(140, 255, 102, 0.26);
    color: var(--text-primary);
    box-shadow: inset 2px 0 0 var(--emerald-light), 0 4px 16px -14px rgba(140, 255, 102, 0.24);
    transform: none;
}
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"] p { color: var(--text-primary); font-weight: 600; }
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"]:hover {
    background: linear-gradient(92deg, rgba(140, 255, 102, 0.22), rgba(56, 217, 150, 0.08) 48%, rgba(167, 139, 250, 0.10));
    box-shadow: inset 2px 0 0 var(--emerald-light), 0 6px 18px -16px rgba(140, 255, 102, 0.30);
    color: var(--text-primary);
    transform: translateX(2px);
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] { gap: 0.4rem; margin-top: 0.35rem; }
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stButton"] button {
    justify-content: center;
    padding: 0.4rem 0.4rem;
    font-size: 11.5px;
    border-radius: 10px;
    color: var(--text-muted);
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stButton"] button p { font-size: 11.5px; }
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stButton"] button:hover { color: var(--text-primary); transform: translateY(-1px); }

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
.cl-page-title {
    font-size: 31px !important;
    line-height: 1.08 !important;
    font-weight: 600 !important;
    letter-spacing: -0.025em;
    padding: 0 !important;
    margin: 0 0 6px !important;
    background: linear-gradient(110deg, var(--text-primary) 18%, var(--emerald-light) 78%, var(--gold-light) 108%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
}
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
    font-size: 42px !important;
    line-height: 1.06 !important;
    padding: 0 !important;
    margin: 10px 0 14px;
    background: linear-gradient(118deg, #FFFFFF 4%, #B8FF9A 46%, #8FE8D4 70%, #E8C9A0 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
}
.cl-hero p { font-size: 15.5px !important; line-height: 1.65 !important; max-width: 56ch; margin: 0 !important; }
.cl-hero-art {
    position: relative;
    align-self: stretch;
    min-height: 280px;
    border-radius: 20px;
    border: 1px solid var(--glass-border);
    background: linear-gradient(135deg, rgba(56, 217, 150, 0.10), rgba(214, 168, 79, 0.08));
    transform: rotate(-1.5deg);
    box-shadow: 0 24px 50px -28px rgba(0, 0, 0, 0.85);
    overflow: hidden;
}
.cl-hero-photo { width: 100%; height: 100%; min-height: 280px; object-fit: cover; display: block; }
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
.cl-section-title { font-size: 19px !important; font-weight: 600 !important; line-height: 1.3 !important; padding: 0 !important; margin: 0 !important; }
.cl-section-sub { font-size: 12.5px !important; color: var(--text-muted); margin: 3px 0 0 !important; }
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
    background: linear-gradient(135deg, #FFFFFF 20%, var(--emerald-light) 82%, var(--gold-light) 110%);
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
    overflow: hidden;
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
.cl-listing-title { font-size: 15.5px !important; font-weight: 600 !important; line-height: 1.32 !important; padding: 0 !important; margin: 0 !important; min-height: 41px; }
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
.cl-detail h3 { font-size: 21px !important; margin: 0 0 4px; }
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
.cl-empty h4 { margin: 0 0 6px; font-size: 16px !important; }
.cl-empty p { margin: 0; font-size: 13px; color: var(--text-muted); }
.cl-note { font-size: 12px; color: var(--text-muted); }
.cl-pager-text { font-family: 'Space Mono', monospace; font-size: 12px; color: var(--text-muted); text-align: center; padding-top: 9px; }
.cl-kv { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 11px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05); font-size: 13px; }
.cl-kv:last-child { border-bottom: none; }
.cl-kv .k { color: var(--text-muted); }
.cl-kv .v { color: var(--text-primary); font-weight: 500; text-align: right; }

/* ---------- Native Streamlit widgets ---------- */
[data-testid="stButton"] button, [data-testid="stDownloadButton"] > button, [data-testid="stFormSubmitButton"] > button {
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
[data-testid="stButton"] button:hover, [data-testid="stDownloadButton"] > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
    background: var(--glass-hover);
    border-color: var(--emerald-light);
    color: var(--text-primary);
    transform: translateY(-1px);
    box-shadow: 0 12px 28px -12px rgba(56, 217, 150, 0.65), 0 0 24px rgba(56, 217, 150, 0.24);
}
[data-testid="stButton"] button p, [data-testid="stDownloadButton"] > button p, [data-testid="stFormSubmitButton"] > button p {
    color: inherit;
    font-size: 13.5px;
    font-weight: inherit;
}
[data-testid="stButton"] button[kind="primary"], [data-testid="stFormSubmitButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, var(--emerald), var(--emerald-light));
    border: none;
    color: #04110B;
    font-weight: 600;
    box-shadow: 0 8px 24px rgba(56, 217, 150, 0.26);
}
[data-testid="stButton"] button[kind="primary"]:hover, [data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
    box-shadow: 0 16px 36px -8px rgba(56, 217, 150, 0.60), 0 0 28px rgba(56, 217, 150, 0.32);
    color: #04110B;
    transform: translateY(-2px);
}
[data-testid="stButton"] button[kind="primary"] p, [data-testid="stFormSubmitButton"] > button[kind="primary"] p { color: #04110B; }

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

[class*="st-key-chartcard_"] {
    position: relative;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 18px 20px 20px;
    margin-bottom: 0.4rem;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    box-shadow: 0 22px 48px -34px var(--glass-shadow);
    transition: background var(--transition-normal), border-color var(--transition-normal), box-shadow var(--transition-normal);
}
[class*="st-key-chartcard_"]:hover {
    background: var(--glass-hover);
    border-color: rgba(140, 255, 102, 0.22);
    box-shadow: 0 30px 60px -38px var(--glass-shadow), 0 0 40px rgba(56, 217, 150, 0.06);
}
[class*="st-key-chartcard_"] [data-testid="stPlotlyChart"],
[class*="st-key-chartcard_"] [data-testid="stPlotlyChart"]:hover {
    background: transparent !important;
    border: 0 !important;
    border-radius: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    box-shadow: none !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    overflow: visible !important;
    height: auto !important;
}
[class*="st-key-chartcard_"] [data-testid="stPlotlyChart"] .modebar { display: none !important; }

[data-testid="stDataFrame"] {
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    overflow: hidden;
}

.stCheckbox p, .stRadio p { font-size: 13px; color: var(--text-secondary); }
[data-testid="stCheckbox"] label > div:first-of-type {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 5px !important;
    color: var(--emerald-light) !important;
}
[data-testid="stCheckbox"] label:hover > div:first-of-type { border-color: var(--emerald-light) !important; }
[data-testid="stCheckbox"] label > div:first-of-type svg {
    stroke: var(--emerald-light) !important;
    fill: none !important;
    stroke-width: 1.8 !important;
    width: 10px;
    height: 8px;
}
[data-testid="stCheckbox"] label > div:first-of-type:has(svg) {
    background: rgba(56, 217, 150, 0.15) !important;
    border-color: rgba(140, 255, 102, 0.45) !important;
}
[data-testid="stCaptionContainer"] p { color: var(--text-muted); font-size: 12px; }

/* ---------- React Aria inputs, comboboxes and menus ---------- */
[data-testid="stTextInputRootElement"],
[data-testid="stNumberInputContainer"],
[data-testid="stDateInput"] > div,
[data-testid="stSelectbox"] [role="group"] {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 11px !important;
    min-height: 42px;
    box-shadow: none !important;
    transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}
[data-testid="stTextInputRootElement"]:focus-within,
[data-testid="stNumberInputContainer"]:focus-within,
[data-testid="stDateInput"] > div:focus-within,
[data-testid="stSelectbox"] [role="group"]:focus-within {
    border-color: var(--emerald-light) !important;
    box-shadow: 0 0 0 1px rgba(140, 255, 102, 0.4), 0 0 18px rgba(140, 255, 102, 0.10) !important;
}
[data-testid="stTextInput"] [data-testid="stTextInputField"],
[data-testid="stNumberInput"] [data-testid="stNumberInputField"],
[data-testid="stSelectbox"] input[role="combobox"] {
    background: transparent !important;
    color: var(--text-primary) !important;
    font-size: 13.5px !important;
    caret-color: var(--emerald-light);
}
[data-testid="stTextInputField"]::placeholder,
[data-testid="stSelectbox"] input::placeholder { color: var(--text-muted) !important; opacity: 1; }
[data-testid="stSelectbox"] button { color: var(--text-muted) !important; }
[data-testid="stSelectbox"] [role="group"] > div:first-child { padding-left: 2px; }
[data-testid="stSelectboxVirtualDropdown"] {
    background: var(--popover-bg) !important;
    border: 1px solid var(--popover-border) !important;
    border-radius: 13px !important;
    box-shadow: 0 24px 54px -22px rgba(0, 0, 0, 0.5) !important;
    padding: 5px !important;
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
}
[data-testid="stSelectboxVirtualDropdown"] [role="option"],
[data-testid="stSelectboxVirtualDropdown"] [data-item-hl] {
    color: var(--text-secondary) !important;
    border-radius: 8px !important;
}
[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-focused="true"],
[data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover {
    background: var(--glass-hover) !important;
}
[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-focused="true"] [data-item-hl],
[data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover [data-item-hl] { color: var(--text-primary) !important; }
[data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"] [data-item-hl] { color: var(--emerald-light) !important; font-weight: 600; }

/* ---------- React Aria tabs ---------- */
[data-testid="stTabs"] [role="tablist"] {
    display: inline-flex;
    width: fit-content !important;
    max-width: 100%;
    align-items: center;
    gap: 4px;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    padding: 5px;
}
[data-testid="stTab"] {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 8px 17px;
    border-radius: 10px;
    color: var(--text-muted);
    cursor: pointer;
    transition: background var(--transition-fast), color var(--transition-fast);
}
[data-testid="stTab"] [data-testid="stMarkdownContainer"] p {
    color: inherit !important;
    font-size: 13px;
    font-weight: 500;
    margin: 0;
}
[data-testid="stTab"]:hover { background: var(--glass-hover); color: var(--text-primary); }
[data-testid="stTab"][aria-selected="true"] {
    background: var(--glass-hover);
    color: var(--text-primary);
    box-shadow: 0 8px 20px -14px var(--glass-shadow);
}
[data-testid="stTabs"] .react-aria-SelectionIndicator { display: none !important; }
[data-testid="stTabs"] [role="tabpanel"] { padding-top: 1rem; }

/* ---------- React Aria date + number fields ---------- */
[data-testid="stDateInputField"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: var(--text-primary) !important;
}
[data-testid="stDateInputField"] [contenteditable],
[data-testid="stDateInputField"] span { color: var(--text-primary) !important; }
[data-testid="stDateInputField"] svg { color: var(--text-muted) !important; }
[data-testid="stNumberInputField"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: var(--text-primary) !important;
}
[data-testid="stNumberInputStepDown"],
[data-testid="stNumberInputStepUp"] {
    background: transparent !important;
    border: none !important;
    border-left: 1px solid var(--glass-border) !important;
    border-radius: 0 !important;
    color: var(--text-muted) !important;
}
[data-testid="stNumberInputStepDown"]:hover,
[data-testid="stNumberInputStepUp"]:hover {
    background: var(--glass-hover) !important;
    color: var(--text-primary) !important;
}

/* ---------- Scrollbars ---------- */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.03); }
::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.14); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(140, 255, 102, 0.35); }

/* ---------- Motion ---------- */
@keyframes cl-rise {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes cl-fade {
    from { opacity: 0; }
    to { opacity: 1; }
}
@keyframes cl-sheen {
    0% { transform: translateX(-120%); }
    100% { transform: translateX(220%); }
}
.cl-page-head { animation: cl-rise 0.5s cubic-bezier(0.22, 1, 0.36, 1) both; }
.cl-hero { animation: cl-rise 0.62s cubic-bezier(0.22, 1, 0.36, 1) 0.05s both; }
.cl-section-head { animation: cl-rise 0.5s cubic-bezier(0.22, 1, 0.36, 1) both; }
.cl-stat-grid { animation: cl-rise 0.56s cubic-bezier(0.22, 1, 0.36, 1) 0.08s both; }
.cl-feed, [data-testid="stForm"], [data-testid="stTabs"],
[data-testid="stPlotlyChart"], .cl-table-wrap, .cl-detail {
    animation: cl-rise 0.55s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.cl-listing { animation: cl-rise 0.5s cubic-bezier(0.22, 1, 0.36, 1) both; }
.cl-listing:nth-child(2), .cl-grid > *:nth-child(2) { animation-delay: 0.03s; }
.cl-listing:nth-child(3), .cl-grid > *:nth-child(3) { animation-delay: 0.06s; }
.cl-listing:nth-child(4), .cl-grid > *:nth-child(4) { animation-delay: 0.09s; }
.cl-listing:nth-child(5), .cl-grid > *:nth-child(5) { animation-delay: 0.12s; }
.cl-listing:nth-child(6), .cl-grid > *:nth-child(6) { animation-delay: 0.15s; }
.cl-listing:nth-child(7), .cl-grid > *:nth-child(7) { animation-delay: 0.18s; }
.cl-listing:nth-child(8), .cl-grid > *:nth-child(8) { animation-delay: 0.21s; }
.cl-card::after, .cl-listing::after {
    content: '';
    position: absolute;
    top: 0; bottom: 0; left: 0;
    width: 42%;
    background: linear-gradient(100deg, transparent, rgba(255, 255, 255, 0.05), transparent);
    transform: translateX(-120%);
    pointer-events: none;
    opacity: 0;
}
.cl-card:hover::after, .cl-listing:hover::after {
    opacity: 1;
    animation: cl-sheen 0.9s ease;
}

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



LIGHT_CSS = r"""
/* ---------- Light theme: warm ivory, mint, champagne, lavender ---------- */
:root {
    --emerald: #0E9F6E;
    --emerald-light: #0B7A52;
    --gold: #A9791F;
    --gold-light: #8A6218;
    --amber: #9A5B08;
    --coral: #C0563D;
    --violet: #6D5BD0;
    --teal: #0F9E8E;
    --glass-bg: rgba(255, 255, 255, 0.56);
    --glass-border: rgba(18, 66, 48, 0.13);
    --glass-shadow: rgba(22, 52, 40, 0.16);
    --glass-hover: rgba(255, 255, 255, 0.82);
    --text-primary: #10241C;
    --text-secondary: rgba(16, 36, 28, 0.74);
    --text-muted: rgba(16, 36, 28, 0.50);
    --popover-bg: #FFFDF8;
    --popover-border: rgba(18, 66, 48, 0.12);
    --success: #0E8F63;
    --warning: #9A6B12;
    --danger: #C0392B;
    --info: #1D7FB8;
    color-scheme: light;
}
.stApp {
    background:
        radial-gradient(ellipse 60% 46% at 14% 4%, rgba(14, 159, 110, 0.16), transparent 64%),
        radial-gradient(ellipse 46% 40% at 88% 16%, rgba(94, 168, 214, 0.12), transparent 66%),
        radial-gradient(ellipse 52% 44% at 84% 84%, rgba(214, 168, 79, 0.17), transparent 64%),
        radial-gradient(ellipse 44% 36% at 36% 98%, rgba(167, 139, 250, 0.13), transparent 68%),
        linear-gradient(135deg, #FAF7EE 0%, #EFF7F0 48%, #F7EFE2 100%);
    background-attachment: fixed;
    color: var(--text-primary);
}
.cl-orb { opacity: 0.20; filter: blur(100px); }
.cl-orb-3 { opacity: 0.10; }
.cl-orb-4 { opacity: 0.11; }
[data-testid="stSidebar"] {
    background: rgba(252, 250, 243, 0.76) !important;
    border-right: 1px solid var(--glass-border);
    box-shadow: 18px 0 50px -42px rgba(22, 52, 40, 0.4);
}
.cl-brand-logo, .cl-topbar-logo { filter: brightness(0) invert(0.14) sepia(0.25) saturate(3.2) hue-rotate(112deg); }
.cl-page-title {
    background: linear-gradient(110deg, #10241C 16%, #0B7A52 74%, #A9791F 108%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.cl-hero {
    background:
        radial-gradient(ellipse 70% 90% at 12% 8%, rgba(14, 159, 110, 0.15), transparent 62%),
        radial-gradient(ellipse 60% 80% at 92% 88%, rgba(169, 121, 31, 0.13), transparent 64%),
        linear-gradient(135deg, rgba(255, 255, 255, 0.72), rgba(255, 255, 255, 0.42));
    box-shadow: 0 34px 70px -46px rgba(22, 52, 40, 0.4);
}
.cl-hero h1 {
    background: linear-gradient(112deg, #10241C 4%, #0B7A52 52%, #0F8F80 72%, #A9791F 104%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.cl-hero-art {
    background: linear-gradient(135deg, rgba(14, 159, 110, 0.10), rgba(169, 121, 31, 0.10));
    box-shadow: 0 24px 50px -30px rgba(22, 52, 40, 0.42);
}
.cl-hero::before, .cl-card::before {
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.9), transparent);
}
.cl-chip, .cl-reason { background: rgba(255, 255, 255, 0.52); }
.cl-card:hover { border-color: rgba(14, 159, 110, 0.24); box-shadow: 0 28px 52px -30px var(--glass-shadow); }
.cl-stat { background: var(--glass-bg); }
.cl-stat-value {
    background: linear-gradient(135deg, #10241C 16%, #0B7A52 78%, #A9791F 108%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.cl-stat-icon { background: rgba(14, 159, 110, 0.12); color: var(--emerald-light); }
.cl-stat-icon.gold { background: rgba(169, 121, 31, 0.13); color: var(--gold-light); }
.cl-stat-icon.coral { background: rgba(192, 86, 61, 0.12); color: var(--coral); }
.cl-stat-icon.info { background: rgba(29, 127, 184, 0.12); color: var(--info); }
.cl-listing, .cl-feed, .cl-detail, .cl-table-wrap, [data-testid="stForm"], [data-testid="stExpander"], [data-testid="stAlert"] {
    background: var(--glass-bg) !important;
    color: var(--text-primary);
}
[data-testid="stExpander"] details,
[data-testid="stExpanderDetails"],
[data-testid="stExpander"] summary {
    background: transparent !important;
    color: var(--text-primary) !important;
}
[data-testid="stExpander"] summary:hover { background: var(--glass-hover) !important; }
[data-testid="stExpander"] svg { fill: currentColor !important; color: var(--text-secondary) !important; }
[data-testid="stForm"] [data-testid="stVerticalBlock"] { background: transparent !important; }
.cl-listing:hover { border-color: rgba(14, 159, 110, 0.30); box-shadow: 0 24px 44px -28px rgba(22, 52, 40, 0.35); }
.cl-listing-id { color: rgba(16, 36, 28, 0.34); }
.cl-tag.borrow { background: rgba(29, 127, 184, 0.12); color: #146C9C; }
.cl-tag.swap { background: rgba(14, 159, 110, 0.13); color: #0A6E4A; }
.cl-tag.giveaway { background: rgba(15, 158, 142, 0.13); color: #0B7468; }
.cl-tag.sell { background: rgba(169, 121, 31, 0.14); color: #7C5714; }
.cl-badge.ok { background: rgba(14, 143, 99, 0.12); }
.cl-badge.warn { background: rgba(169, 121, 31, 0.14); }
.cl-badge.info { background: rgba(29, 127, 184, 0.12); }
.cl-badge.danger { background: rgba(192, 57, 43, 0.11); }
.cl-badge.muted { background: rgba(16, 36, 28, 0.06); }
.cl-table td { border-bottom: 1px solid rgba(16, 36, 28, 0.055); }
.cl-meta { background: rgba(255, 255, 255, 0.48); }
.cl-feed-item { border-bottom: 1px solid rgba(16, 36, 28, 0.06); }
.cl-kv { border-bottom: 1px solid rgba(16, 36, 28, 0.07); }
.cl-empty { border-color: rgba(16, 36, 28, 0.18); background: rgba(255, 255, 255, 0.34); }
.cl-bar { background: rgba(16, 36, 28, 0.10); }
[class*="st-key-chartcard_"] {
    background: var(--glass-bg);
    border-color: var(--glass-border);
    box-shadow: 0 24px 50px -38px rgba(22, 52, 40, 0.34);
}
[class*="st-key-chartcard_"]:hover { border-color: rgba(14, 159, 110, 0.26); }
[data-testid="stButton"] button, [data-testid="stDownloadButton"] > button, [data-testid="stFormSubmitButton"] > button {
    background: rgba(255, 255, 255, 0.58);
    color: var(--text-primary);
}
[data-testid="stButton"] button:hover, [data-testid="stDownloadButton"] > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
    background: rgba(255, 255, 255, 0.9);
    border-color: var(--emerald);
}
[data-testid="stButton"] button[kind="primary"], [data-testid="stFormSubmitButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #0E9F6E, #48C98F);
    color: #04110B;
}
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stTextArea"] textarea,
[data-baseweb="select"] > div {
    background: rgba(255, 255, 255, 0.66) !important;
    color: var(--text-primary) !important;
}
[data-testid="stNumberInput"] button { background: rgba(255, 255, 255, 0.6); color: var(--text-secondary); }
[data-testid="stTextInputRootElement"],
[data-testid="stNumberInputContainer"],
[data-testid="stDateInput"] > div,
[data-testid="stSelectbox"] [role="group"] {
    background: rgba(255, 255, 255, 0.66) !important;
    border-color: var(--glass-border) !important;
}
[data-testid="stSelectboxVirtualDropdown"] {
    background: #FFFDF8 !important;
    border-color: var(--glass-border) !important;
    box-shadow: 0 24px 54px -24px rgba(22, 52, 40, 0.28) !important;
}
[data-testid="stTextInputRootElement"]:focus-within,
[data-testid="stNumberInputContainer"]:focus-within,
[data-testid="stDateInput"] > div:focus-within,
[data-testid="stSelectbox"] [role="group"]:focus-within {
    border-color: var(--emerald) !important;
    box-shadow: 0 0 0 1px rgba(14, 159, 110, 0.35), 0 0 18px rgba(14, 159, 110, 0.10) !important;
}
[data-baseweb="popover"] div[role="listbox"], [data-baseweb="menu"] {
    background: #FFFDF8 !important;
    border-color: var(--glass-border);
    box-shadow: 0 18px 40px -20px rgba(22, 52, 40, 0.3);
}
[data-baseweb="popover"] li { color: var(--text-secondary) !important; }
[data-baseweb="popover"] li:hover { background: rgba(14, 159, 110, 0.10) !important; }
.stTabs [data-baseweb="tab-list"] { background: rgba(255, 255, 255, 0.42); }
.stTabs [aria-selected="true"] { background: rgba(255, 255, 255, 0.92); }
.st-key-app_topbar {
    border-color: rgba(255, 255, 255, 0.72);
    background:
        linear-gradient(180deg, rgba(255, 255, 255, 0.38), rgba(255, 255, 255, 0.12)),
        rgba(255, 253, 248, 0.42);
    backdrop-filter: blur(40px) saturate(150%);
    -webkit-backdrop-filter: blur(40px) saturate(150%);
    box-shadow: 0 22px 50px -28px rgba(22, 52, 40, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.75);
}
.st-key-app_topbar [data-testid="stButton"] button {
    background: transparent;
}
.st-key-app_topbar [data-testid="stButton"] button[kind="primary"] {
    background: rgba(14, 159, 110, 0.13);
    border-color: rgba(14, 159, 110, 0.32);
}
[data-testid="stButton"] button:hover, [data-testid="stDownloadButton"] > button:hover, [data-testid="stFormSubmitButton"] > button:hover,
.st-key-app_topbar [data-testid="stButton"] button:hover {
    box-shadow: 0 12px 28px -12px rgba(14, 159, 110, 0.60), 0 0 24px rgba(14, 159, 110, 0.24);
}
.st-key-app_topbar [data-testid="stButton"] button[kind="primary"]:hover,
[data-testid="stButton"] button[kind="primary"]:hover, [data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
    box-shadow: 0 12px 30px -10px rgba(14, 159, 110, 0.64), 0 0 26px rgba(14, 159, 110, 0.26);
}
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(92deg, rgba(14, 159, 110, 0.16), rgba(255, 255, 255, 0.55) 52%, rgba(167, 139, 250, 0.10));
    border-color: rgba(14, 159, 110, 0.30);
    box-shadow: inset 2px 0 0 var(--emerald), 0 4px 16px -14px rgba(14, 159, 110, 0.28);
}
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"]:hover {
    background: linear-gradient(92deg, rgba(14, 159, 110, 0.22), rgba(255, 255, 255, 0.7) 52%, rgba(167, 139, 250, 0.13));
    box-shadow: inset 2px 0 0 var(--emerald), 0 6px 18px -16px rgba(14, 159, 110, 0.30);
}
::-webkit-scrollbar-track { background: rgba(16, 36, 28, 0.04); }
::-webkit-scrollbar-thumb { background: rgba(16, 36, 28, 0.16); }
::-webkit-scrollbar-thumb:hover { background: rgba(14, 159, 110, 0.4); }
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


def inject_css(theme: str = "dark", reduce_motion: bool = False) -> None:
    """Inject the CampusLoop stylesheet for the active theme."""
    extra = ""
    if reduce_motion:
        extra = (
            "<style>.stApp *, .stApp *::before, .stApp *::after"
            " { animation: none !important; transition: none !important; }</style>"
        )
    palette = LIGHT_CSS if theme == "light" else ""
    st.markdown(f"<style>{CSS}{palette}</style>{extra}", unsafe_allow_html=True)
