"""Plotly chart helpers styled to the CampusLoop glass theme.

All charts are expected to receive already-aggregated data (value_counts /
groupby / histogram bins) so large raw datasets are never shipped to the
browser.
"""

from __future__ import annotations

from typing import Sequence

import plotly.graph_objects as go
import streamlit as st

CHART_COLORS = [
    "#8CFF66",
    "#38D996",
    "#D6A84F",
    "#E07A5F",
    "#5EC8FF",
    "#B8FF9A",
    "#E8C9A0",
    "#7FE9BC",
    "#FFB4A0",
    "#2DD4BF",
]

LIGHT_CHART_COLORS = [
    "#0E8F63",
    "#16A34A",
    "#B7791F",
    "#C0563D",
    "#1D7FB8",
    "#3B7F4E",
    "#A67C2E",
    "#2F8F6B",
    "#C97B5E",
    "#0F9E8E",
]


def _light() -> bool:
    try:
        return st.session_state.get("theme", "dark") == "light"
    except Exception:
        return False


def _palette() -> list[str]:
    return LIGHT_CHART_COLORS if _light() else CHART_COLORS


def _tokens() -> dict:
    if _light():
        return {
            "text": "#10241C",
            "muted": "rgba(16,36,28,0.56)",
            "grid": "rgba(16,50,38,0.10)",
            "line": "rgba(16,50,38,0.16)",
            "hover_bg": "#FFFDF8",
            "accent": "#0E9F6E",
            "accent_soft": "rgba(14,159,110,0.08)",
            "marker_fill": "#FFFDF8",
            "bar_fill": "rgba(14,159,110,0.55)",
            "bar_line": "rgba(11,122,82,0.75)",
        }
    return {
        "text": "#F4F7F5",
        "muted": "#9AA7A0",
        "grid": "rgba(255,255,255,0.06)",
        "line": "rgba(255,255,255,0.08)",
        "hover_bg": "#0B1714",
        "accent": "#8CFF66",
        "accent_soft": "rgba(140,255,102,0.07)",
        "marker_fill": "#0B1714",
        "bar_fill": "rgba(56,217,150,0.55)",
        "bar_line": "rgba(140,255,102,0.7)",
    }


def _style(fig: go.Figure, height: int = 320, axes: bool = True) -> go.Figure:
    t = _tokens()
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=28, b=24),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Outfit, system-ui, sans-serif", color=t["text"], size=12),
        title=dict(font=dict(color=t["text"], size=14)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=t["muted"], size=11)),
        hoverlabel=dict(
            bgcolor=t["hover_bg"],
            bordercolor=t["accent"],
            font=dict(color=t["text"], family="Outfit, sans-serif", size=12),
        ),
        bargap=0.35,
        uirevision="campusloop",
    )
    if axes:
        axis = dict(
            gridcolor=t["grid"],
            zeroline=False,
            linecolor=t["line"],
            tickfont=dict(color=t["muted"], size=11),
            title_font=dict(color=t["muted"], size=11),
            automargin=True,
        )
        fig.update_xaxes(**axis)
        fig.update_yaxes(**axis)
    else:
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
    return fig


def donut_chart(labels: Sequence, values: Sequence, center_value: str = "", center_label: str = "", height: int = 300) -> go.Figure:
    fig = go.Figure(
        data=[
            go.Pie(
                labels=list(labels),
                values=list(values),
                hole=0.64,
                sort=False,
                marker=dict(
                    colors=_palette(),
                    line=dict(color="rgba(255,255,255,0.85)" if _light() else "rgba(5,10,10,0.65)", width=2),
                ),
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>%{value:,} &middot; %{percent}<extra></extra>",
            )
        ]
    )
    if center_value:
        t = _tokens()
        fig.add_annotation(
            text=f"<span style='font-family:Space Mono,monospace;font-size:20px;color:{t['text']}'>{center_value}</span>"
            f"<br><span style='font-size:10px;color:{t['muted']};letter-spacing:.12em'>{center_label}</span>",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
    _style(fig, height=height, axes=False)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.12, x=0.5, xanchor="center"))
    return fig


def bar_chart(
    x: Sequence,
    y: Sequence,
    height: int = 320,
    horizontal: bool = False,
    text: Sequence | None = None,
) -> go.Figure:
    palette = _palette()
    colors = [palette[i % len(palette)] for i in range(len(list(x)))]
    if horizontal:
        trace = go.Bar(
            x=list(y),
            y=list(x),
            orientation="h",
            marker=dict(color=colors, cornerradius=6),
            text=list(text) if text is not None else None,
            textposition="outside",
            textfont=dict(color=_tokens()["muted"], size=10),
            hovertemplate="<b>%{y}</b><br>%{x:,}<extra></extra>",
        )
    else:
        trace = go.Bar(
            x=list(x),
            y=list(y),
            marker=dict(color=colors, cornerradius=6),
            text=list(text) if text is not None else None,
            textposition="outside",
            textfont=dict(color=_tokens()["muted"], size=10),
            hovertemplate="<b>%{x}</b><br>%{y:,}<extra></extra>",
        )
    fig = go.Figure(data=[trace])
    _style(fig, height=height)
    fig.update_layout(showlegend=False)
    if horizontal:
        fig.update_layout(margin=dict(l=132, r=20))
        fig.update_yaxes(tickfont=dict(size=10))
    return fig


def line_chart(x: Sequence, y: Sequence, height: int = 320, name: str = "Value") -> go.Figure:
    fig = go.Figure(
        data=[
            go.Scatter(
                x=list(x),
                y=list(y),
                mode="lines+markers",
                line=dict(color=_tokens()["accent"], width=2.4, shape="spline", smoothing=0.6),
                marker=dict(
                    size=5,
                    color=_tokens()["marker_fill"],
                    line=dict(color=_tokens()["accent"], width=1.6),
                ),
                fill="tozeroy",
                fillcolor=_tokens()["accent_soft"],
                hovertemplate="<b>%{x}</b><br>%{y:,}<extra></extra>",
                name=name,
            )
        ]
    )
    _style(fig, height=height)
    fig.update_layout(showlegend=False)
    return fig


def histogram_chart(centers: Sequence, counts: Sequence, height: int = 320) -> go.Figure:
    fig = go.Figure(
        data=[
            go.Bar(
                x=list(centers),
                y=list(counts),
                marker=dict(
                    color=_tokens()["bar_fill"],
                    line=dict(color=_tokens()["bar_line"], width=1),
                    cornerradius=4,
                ),
                hovertemplate="<b>%{x}</b><br>%{y:,} listings<extra></extra>",
            )
        ]
    )
    _style(fig, height=height)
    fig.update_layout(showlegend=False, bargap=0.08)
    return fig
