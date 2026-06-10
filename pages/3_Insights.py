import streamlit as st

from database.queries import get_all_expenses
from modules.analytics import create_expense_dataframe
from modules.insights import generate_insights
from modules.anomaly_detection import detect_anomalies
from modules.ai_advisor import generate_ai_response
from ui.components import (
    empty_state,
    init_app_shell,
    render_ai_response,
    render_insight_card,
    render_section_header,
)

SUGGESTED_PROMPTS = [
    "How can I save money?",
    "What is my highest spending category?",
    "Show my monthly spending trends",
]


def _anomaly_display_df(anomalies, full_df):
    """Add a display-only severity column for the anomalies table."""
    if anomalies.empty:
        return anomalies

    display = anomalies.copy()
    severities = []

    for _, row in anomalies.iterrows():
        category_df = full_df[full_df["category"] == row["category"]]
        average = category_df["amount"].mean()
        std_dev = category_df["amount"].std()

        if std_dev and std_dev > 0 and row["amount"] > average + (2 * std_dev):
            severities.append("High")
        else:
            severities.append("Elevated")

    display.insert(0, "severity", severities)
    return display


init_app_shell(
    "Insights",
    page_icon="material/psychology",
    header_title="Financial Insights",
    header_subtitle="Rule-based analysis, anomaly detection, and AI assistant",
    header_icon="material/psychology",
)

user_id = st.session_state.user["id"]

expenses = get_all_expenses(user_id)
df = create_expense_dataframe(expenses)

if df.empty:
    empty_state(
        title="No expense data yet",
        message="Add transactions to unlock spending insights, anomaly detection, and AI recommendations.",
        action_label="Add Expense",
        action_page="pages/2_Add_Expense.py",
    )
else:
    tab_insights, tab_anomalies, tab_ai = st.tabs(
        [
            "Insights",
            "Anomalies",
            "AI Assistant",
        ]
    )

    with tab_insights:
        render_section_header(
            "Spending insights",
            "Automated observations based on your expense history",
            band=True,
        )

        insights = generate_insights(df)

        if insights:
            for insight in insights:
                render_insight_card(insight)
        else:
            st.markdown(
                '<div class="insights-empty">No major spending patterns detected yet. '
                "Keep adding expenses to generate more insights.</div>",
                unsafe_allow_html=True,
            )

    with tab_anomalies:
        render_section_header(
            "Expense anomalies",
            "Transactions that exceed normal category spending patterns",
        )

        anomalies = detect_anomalies(df)

        if not anomalies.empty:
            st.markdown(
                '<div class="anomaly-alert-banner">'
                "Some expenses appear unusually high compared to normal category spending."
                "</div>",
                unsafe_allow_html=True,
            )

            display_anomalies = _anomaly_display_df(anomalies, df)

            st.dataframe(
                display_anomalies[
                    [
                        "severity",
                        "expense_date",
                        "category",
                        "amount",
                        "payment_mode",
                        "description",
                    ]
                ],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "severity": st.column_config.TextColumn(
                        "Severity",
                        help="Display-only flag based on deviation from category average",
                    ),
                    "expense_date": st.column_config.DatetimeColumn(
                        "Date",
                        format="DD MMM YYYY",
                    ),
                    "category": st.column_config.TextColumn("Category"),
                    "amount": st.column_config.NumberColumn(
                        "Amount",
                        format="₹ %.2f",
                    ),
                    "payment_mode": st.column_config.TextColumn("Payment"),
                    "description": st.column_config.TextColumn("Description"),
                },
            )
        else:
            st.markdown(
                '<div class="anomalies-empty">No unusual spending detected. '
                "Your expenses are within expected category ranges.</div>",
                unsafe_allow_html=True,
            )

    with tab_ai:
        render_section_header(
            "Financial assistant",
            "Ask questions about your spending patterns and get tailored guidance",
        )

        if "ai_question" not in st.session_state:
            st.session_state.ai_question = ""

        if "ai_response" not in st.session_state:
            st.session_state.ai_response = None

        st.markdown('<p class="ai-prompt-label">Suggested questions</p>', unsafe_allow_html=True)

        st.markdown('<div class="prompt-chip-row">', unsafe_allow_html=True)
        prompt_cols = st.columns(len(SUGGESTED_PROMPTS))

        for index, prompt in enumerate(SUGGESTED_PROMPTS):
            with prompt_cols[index]:
                if st.button(prompt, key=f"ai_prompt_{index}", use_container_width=True):
                    st.session_state.ai_question = prompt

        st.markdown("</div>", unsafe_allow_html=True)

        question = st.text_input(
            "Your question",
            key="ai_question",
            placeholder="e.g. How can I reduce my food spending?",
        )

        ask_col1, ask_col2 = st.columns([1, 4])

        with ask_col1:
            ask_clicked = st.button("Ask AI", type="primary", use_container_width=True)

        if ask_clicked:
            if question.strip():
                with st.spinner("Analyzing your expenses…"):
                    st.session_state.ai_response = generate_ai_response(df, question)
            else:
                st.warning(
                    "Please enter a question first.",
                    icon=":material/info:",
                )

        if st.session_state.ai_response:
            render_ai_response(st.session_state.ai_response)
