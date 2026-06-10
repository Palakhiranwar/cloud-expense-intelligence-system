"""Shared UI theme and components for Cloud Expense Intelligence."""

from ui.theme import (
    COLORS,
    PLOTLY_COLOR_SEQUENCE,
    PLOTLY_LAYOUT,
    PLOTLY_LINE_STYLE,
    configure_page,
    load_theme,
)
from ui.components import (
    empty_state,
    init_app_shell,
    kpi_card,
    logout,
    render_ai_response,
    render_anomaly_review_panel,
    render_breadcrumb,
    render_insight_card,
    render_page_header,
    render_section_header,
    render_sidebar,
    require_auth,
    section_card,
)

__all__ = [
    "COLORS",
    "PLOTLY_COLOR_SEQUENCE",
    "PLOTLY_LAYOUT",
    "PLOTLY_LINE_STYLE",
    "configure_page",
    "load_theme",
    "empty_state",
    "init_app_shell",
    "kpi_card",
    "logout",
    "render_ai_response",
    "render_anomaly_review_panel",
    "render_breadcrumb",
    "render_insight_card",
    "render_page_header",
    "render_section_header",
    "render_sidebar",
    "require_auth",
    "section_card",
]
