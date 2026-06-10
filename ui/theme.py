"""Design tokens, CSS injection, and Plotly styling constants."""

from pathlib import Path
from typing import Literal

import streamlit as st

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_CSS_PATH = _PROJECT_ROOT / "assets" / "styles.css"

COLORS = {
    "primary": "#0972d3",
    "primary_hover": "#0552b5",
    "primary_light": "#e8f4fd",
    "bg": "#f8fafc",
    "surface": "#ffffff",
    "border": "#e2e8f0",
    "text_primary": "#0f172a",
    "text_secondary": "#64748b",
    "success": "#059669",
    "warning": "#d97706",
    "danger": "#dc2626",
    "chart_1": "#0972d3",
    "chart_2": "#1d8fff",
    "chart_3": "#5eb3ff",
    "chart_4": "#94a3b8",
    "chart_5": "#cbd5e1",
    "chart_6": "#64748b",
}

PLOTLY_COLOR_SEQUENCE = [
    COLORS["chart_1"],
    COLORS["chart_2"],
    COLORS["chart_3"],
    COLORS["chart_4"],
    COLORS["chart_5"],
    COLORS["chart_6"],
]

PLOTLY_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {
        "family": "Inter, system-ui, sans-serif",
        "color": COLORS["text_primary"],
        "size": 13,
    },
    "margin": {"l": 48, "r": 24, "t": 40, "b": 48},
    "hoverlabel": {
        "bgcolor": COLORS["surface"],
        "bordercolor": COLORS["border"],
        "font": {"color": COLORS["text_primary"], "size": 12},
    },
    "xaxis": {
        "gridcolor": COLORS["border"],
        "linecolor": COLORS["border"],
        "tickfont": {"color": COLORS["text_secondary"]},
        "title_font": {"color": COLORS["text_secondary"]},
    },
    "yaxis": {
        "gridcolor": COLORS["border"],
        "linecolor": COLORS["border"],
        "tickfont": {"color": COLORS["text_secondary"]},
        "title_font": {"color": COLORS["text_secondary"]},
    },
    "legend": {
        "font": {"color": COLORS["text_secondary"]},
        "bgcolor": "rgba(0,0,0,0)",
    },
}

PLOTLY_LINE_STYLE = {
    "line": {"color": COLORS["primary"], "width": 2.5},
    "marker": {"size": 7, "color": COLORS["primary_hover"]},
}

SidebarState = Literal["auto", "expanded", "collapsed"]


def configure_page(
    title: str,
    *,
    icon: str = "material/cloud",
    layout: Literal["centered", "wide"] = "wide",
    initial_sidebar_state: SidebarState = "expanded",
) -> None:
    """Apply consistent Streamlit page configuration."""
    st.set_page_config(
        page_title=f"{title} | Cloud Expense Intelligence",
        page_icon=f":{icon}:",
        layout=layout,
        initial_sidebar_state=initial_sidebar_state,
    )


def load_theme() -> None:
    """Inject global stylesheet from assets/styles.css."""
    with open(_CSS_PATH, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
