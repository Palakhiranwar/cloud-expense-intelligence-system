import streamlit as st

from ui.components import init_app_shell, render_html

user = init_app_shell(
    "Overview",
    page_icon="material/home",
    show_header=False,
)

name = user["name"]

render_html(
    f"""
    <div class="home-hero">
        <div class="home-hero-badge">Welcome back</div>
        <h1>{name}</h1>
        <p>
            Your cloud expense intelligence workspace is ready.
            Review costs, add transactions, and explore AI-driven insights.
        </p>
    </div>
    """
)

st.markdown('<div class="quick-links-label">Quick actions</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    render_html(
        """
        <div class="home-card">
            <div class="home-card-icon">+</div>
            <h3>Add expense</h3>
            <p>Record a new transaction and keep your ledger up to date.</p>
        </div>
        """
    )
    st.page_link(
        "pages/2_Add_Expense.py",
        label="Go to Add Expense",
        icon=":material/add:",
        use_container_width=True,
    )

with col2:
    render_html(
        """
        <div class="home-card">
            <div class="home-card-icon">&#9670;</div>
            <h3>Cost dashboard</h3>
            <p>View KPIs, trends, forecasts, and filtered transaction data.</p>
        </div>
        """
    )
    st.page_link(
        "pages/1_Dashboard.py",
        label="Open Dashboard",
        icon=":material/analytics:",
        use_container_width=True,
    )

with col3:
    render_html(
        """
        <div class="home-card">
            <div class="home-card-icon">&#9672;</div>
            <h3>AI insights</h3>
            <p>Discover patterns, anomalies, and ask the financial assistant.</p>
        </div>
        """
    )
    st.page_link(
        "pages/3_Insights.py",
        label="Explore Insights",
        icon=":material/psychology:",
        use_container_width=True,
    )

st.markdown('<div class="overview-grid">', unsafe_allow_html=True)

feat_col, quote_col = st.columns([1.4, 1])

with feat_col:
    render_html(
        """
        <div class="feature-banner">
            <h2>Platform capabilities</h2>
            <ul>
                <li>AI-powered spending analysis</li>
                <li>ML-based expense forecasting</li>
                <li>Automatic unusual spending detection</li>
                <li>Secure cloud-based expense tracking</li>
            </ul>
        </div>
        """
    )

with quote_col:
    render_html(
        """
        <div class="quote-card">
            <h3>"Small spending decisions create big financial changes."</h3>
            <p>Consistent tracking is the foundation of smarter cost control.</p>
        </div>
        """
    )

st.markdown("</div>", unsafe_allow_html=True)
