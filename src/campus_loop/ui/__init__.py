"""CampusLoop presentation layer.

Dark and light glass UI (deep forest or ivory ambient background, animated
orbs, glass surfaces, emerald/gold palette, Outfit + Space Mono typography).
"""

from .theme import CSS, inject_css, img_data_uri
from .components import (
    compact,
    activity_feed,
    compact,
    badge,
    data_table,
    detail_card,
    empty_state,
    esc,
    fmt_inr,
    hero,
    initials,
    listing_cards,
    page_header,
    stat_cards,
    stat_grid_frame,
    user_rows,
    mode_tag,
)
from .charts import donut_chart, bar_chart, line_chart, histogram_chart

__all__ = [
    "CSS",
    "inject_css",
    "img_data_uri",
    "compact",
    "activity_feed",
    "badge",
    "data_table",
    "detail_card",
    "empty_state",
    "hero",
    "initials",
    "listing_cards",
    "page_header",
    "stat_cards",
    "stat_grid_frame",
    "user_rows",
    "mode_tag",
    "donut_chart",
    "bar_chart",
    "line_chart",
    "histogram_chart",
]
