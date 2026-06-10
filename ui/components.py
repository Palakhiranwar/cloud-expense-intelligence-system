"""Reusable UI layout components."""

import html
from textwrap import dedent

import streamlit as st

from ui.theme import load_theme, configure_page


def render_html(markup: str) -> None:
    """Render HTML without markdown code-block escaping from indentation."""
    st.markdown(dedent(markup).strip(), unsafe_allow_html=True)

NAV_ITEMS = [
    ("Dashboard", "pages/1_Dashboard.py", ":material/analytics:"),
    ("Add Expense", "pages/2_Add_Expense.py", ":material/add:"),
    ("Insights", "pages/3_Insights.py", ":material/psychology:"),
    ("Overview", "pages/0_Overview.py", ":material/home:"),
]

_SESSION_KEYS_ON_LOGOUT = (
    "user",
    "logged_in",
    "user_id",
    "pending_expense",
    "pending_expense_limit",
    "ai_response",
    "ai_question",
)


def logout() -> None:
    """Clear session state and return to the login page."""
    for key in _SESSION_KEYS_ON_LOGOUT:
        if key in st.session_state:
            del st.session_state[key]

    st.session_state.user = None
    st.session_state.logged_in = False
    st.switch_page("app.py")


def require_auth() -> dict:
    """Redirect unauthenticated users to login. Returns the current user."""
    if "user" not in st.session_state or st.session_state.user is None:
        st.switch_page("app.py")
    return st.session_state.user


def render_sidebar() -> None:
    """Render branded sidebar with navigation and logout."""
    with st.sidebar:
        render_html(
            """
            <div class="sidebar-brand">
                <div class="sidebar-logo">CE</div>
                <div>
                    <div class="sidebar-brand-title">Cloud Expense</div>
                    <div class="sidebar-brand-subtitle">Intelligence</div>
                </div>
            </div>
            """
        )

        st.markdown('<p class="sidebar-section-label">Navigation</p>', unsafe_allow_html=True)

        for label, path, icon in NAV_ITEMS:
            st.page_link(path, label=label, icon=icon)

        st.divider()

        user = st.session_state.get("user")
        if user:
            render_html(
                f"""
                <div class="sidebar-user">
                    <div class="sidebar-user-name">{user["name"]}</div>
                    <div class="sidebar-user-email">{user.get("email", "")}</div>
                </div>
                """
            )

        if st.button("Logout", use_container_width=True, icon=":material/logout:", key="sidebar_logout"):
            logout()


def render_page_header(
    title: str,
    subtitle: str | None = None,
    icon: str | None = None,
) -> None:
    """Render a consistent page title block."""
    st.markdown('<div class="page-header-block">', unsafe_allow_html=True)

    if icon:
        st.markdown(f"### :{icon}: {title}")
    else:
        st.markdown(f"### {title}")

    if subtitle:
        st.markdown(
            f'<p class="page-header-subtitle">{html.escape(subtitle)}</p>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="page-header-divider"></div></div>', unsafe_allow_html=True)


def init_app_shell(
    page_title: str,
    *,
    page_icon: str = "material/cloud",
    header_title: str | None = None,
    header_subtitle: str | None = None,
    header_icon: str | None = None,
    show_header: bool = True,
) -> dict:
    """
    Bootstrap an authenticated page: config, auth guard, theme, sidebar.
    Returns the current user dict.
    """
    configure_page(
        page_title,
        icon=page_icon,
        initial_sidebar_state="expanded",
    )
    user = require_auth()
    load_theme()
    render_sidebar()

    if show_header and header_title:
        render_page_header(header_title, header_subtitle, header_icon)

    return user


def render_section_header(
    title: str,
    subtitle: str | None = None,
    *,
    band: bool = False,
) -> None:
    """Section heading with optional subtitle and optional tinted band."""
    band_class = " section-header-band" if band else ""
    subtitle_html = f'<p class="section-subtitle">{subtitle}</p>' if subtitle else ""
    render_html(
        f"""
        <div class="section-header{band_class}">
            <h3>{html.escape(title)}</h3>
            {subtitle_html}
        </div>
        """
    )


def kpi_card(
    label: str,
    value: str,
    delta: str | None = None,
) -> None:
    """Render a styled KPI metric card."""
    delta_html = f'<div class="kpi-delta">{delta}</div>' if delta else ""

    render_html(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
        """
    )


def empty_state(title: str, message: str, action_label: str, action_page: str) -> None:
    """Empty data placeholder with navigation CTA."""
    render_html(
        f"""
        <div class="empty-state">
            <div class="empty-state-title">{title}</div>
            <div class="empty-state-message">{message}</div>
        </div>
        """
    )

    if st.button(action_label, type="primary", use_container_width=False):
        st.switch_page(action_page)


def render_breadcrumb(*parts: str) -> None:
    """Render a breadcrumb trail (last item is current page)."""
    crumbs = []
    for index, part in enumerate(parts):
        if index == len(parts) - 1:
            crumbs.append(f'<span class="breadcrumb-current">{part}</span>')
        else:
            crumbs.append(f'<span class="breadcrumb-item">{part}</span>')

    trail = '<span class="breadcrumb-sep">/</span>'.join(crumbs)
    st.markdown(f'<div class="breadcrumb">{trail}</div>', unsafe_allow_html=True)


def render_anomaly_review_panel(
    pending: dict,
    limit: float | None = None,
) -> None:
    """Styled panel for reviewing an unusual expense before saving."""
    limit_html = (
        f'<div class="review-limit">Typical category limit: ₹{limit:,.2f}</div>'
        if limit is not None
        else ""
    )

    render_html(
        f"""
        <div class="review-panel">
            <div class="review-panel-header">
                <span class="review-panel-badge">Review required</span>
            </div>
            <div class="review-panel-title">Unusual expense detected</div>
            <p class="review-panel-message">
                This transaction exceeds the normal spending pattern for
                <strong>{pending["category"]}</strong>. Confirm before saving.
            </p>
            <div class="review-details">
                <div class="review-detail-row">
                    <span class="review-detail-label">Date</span>
                    <span class="review-detail-value">{pending["date"]}</span>
                </div>
                <div class="review-detail-row">
                    <span class="review-detail-label">Category</span>
                    <span class="review-detail-value">{pending["category"]}</span>
                </div>
                <div class="review-detail-row">
                    <span class="review-detail-label">Amount</span>
                    <span class="review-detail-value">₹{pending["amount"]:,.2f}</span>
                </div>
                <div class="review-detail-row">
                    <span class="review-detail-label">Payment</span>
                    <span class="review-detail-value">{pending["payment"]}</span>
                </div>
                <div class="review-detail-row">
                    <span class="review-detail-label">Description</span>
                    <span class="review-detail-value">{pending["description"] or "—"}</span>
                </div>
            </div>
            {limit_html}
        </div>
        """
    )


def render_insight_card(text: str) -> None:
    """Compact card for a single rule-based insight."""
    safe_text = html.escape(text)
    render_html(
        f"""
        <div class="insight-card">
            <div class="insight-card-icon">&#9679;</div>
            <div class="insight-card-body">{safe_text}</div>
        </div>
        """
    )


def render_ai_response(text: str) -> None:
    """Chat-style container for AI advisor output."""
    safe_text = html.escape(text).replace("\n", "<br>")
    render_html(
        f"""
        <div class="ai-chat-response">
            <div class="ai-chat-header">
                <span class="ai-chat-label">Financial Assistant</span>
            </div>
            <div class="ai-chat-body">{safe_text}</div>
        </div>
        """
    )


def section_card(title: str | None = None) -> None:
    """Section title placeholder."""
    if title:
        render_section_header(title)
