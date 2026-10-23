"""Plotly chart helpers styled to the CampusLoop glass theme.

All charts are expected to receive already-aggregated data (value_counts /
groupby / histogram bins) so large raw datasets are never shipped to the
browser.
"""

from __future__ import annotations

from typing import Sequence

import plotly.graph_objects as go

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


def _style(fig: go.Figure, height: int = 320, axes: bool = True) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=14, r=14, t=18, b=14),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Outfit, system-ui, sans-serif", color="#F4F7F5", size=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#9AA7A0", size=11)),
        hoverlabel=dict(
            bgcolor="#0B1714",
            bordercolor="rgba(140,255,102,0.35)",
            font=dict(color="#F4F7F5", family="Outfit, sans-serif", size=12),
        ),
        bargap=0.35,
    )
    if axes:
        axis = dict(
            gridcolor="rgba(255,255,255,0.06)",
            zeroline=False,
            linecolor="rgba(255,255,255,0.08)",
            tickfont=dict(color="#9AA7A0", size=11),
            title_font=dict(color="#9AA7A0", size=11),
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
                marker=dict(colors=CHART_COLORS, line=dict(color="rgba(5,10,10,0.65)", width=2)),
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>%{value:,} &middot; %{percent}<extra></extra>",
            )
        ]
    )
    if center_value:
        fig.add_annotation(
            text=f"<span style='font-family:Space Mono,monospace;font-size:20px;color:#F4F7F5'>{center_value}</span>"
            f"<br><span style='font-size:10px;color:#9AA7A0;letter-spacing:.12em'>{center_label}</span>",
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
    colors = [CHART_COLORS[i % len(CHART_COLORS)] for i in range(len(list(x)))]
    if horizontal:
        trace = go.Bar(
            x=list(y),
            y=list(x),
            orientation="h",
            marker=dict(color=colors, cornerradius=6),
            text=list(text) if text is not None else None,
            textposition="outside",
            textfont=dict(color="#9AA7A0", size=10),
            hovertemplate="<b>%{y}</b><br>%{x:,}<extra></extra>",
        )
    else:
        trace = go.Bar(
            x=list(x),
            y=list(y),
            marker=dict(color=colors, cornerradius=6),
            text=list(text) if text is not None else None,
            textposition="outside",
            textfont=dict(color="#9AA7A0", size=10),
            hovertemplate="<b>%{x}</b><br>%{y:,}<extra></extra>",
        )
    fig = go.Figure(data=[trace])
    _style(fig, height=height)
    fig.update_layout(showlegend=False)
    return fig


def line_chart(x: Sequence, y: Sequence, height: int = 320, name: str = "Value") -> go.Figure:
    fig = go.Figure(
        data=[
            go.Scatter(
                x=list(x),
                y=list(y),
                mode="lines+markers",
                line=dict(color="#8CFF66", width=2.4, shape="spline", smoothing=0.6),
                marker=dict(size=5, color="#0B1714", line=dict(color="#8CFF66", width=1.6)),
                fill="tozeroy",
                fillcolor="rgba(140,255,102,0.07)",
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
                    color="rgba(56,217,150,0.55)",
                    line=dict(color="rgba(140,255,102,0.7)", width=1),
                    cornerradius=4,
                ),
                hovertemplate="<b>%{x}</b><br>%{y:,} listings<extra></extra>",
            )
        ]
    )
    _style(fig, height=height)
    fig.update_layout(showlegend=False, bargap=0.08)
    return fig
