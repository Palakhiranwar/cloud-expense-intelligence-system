import streamlit as st

from database.queries import add_expense
from modules.expense_review import is_unusual_expense
from ui.components import (
    init_app_shell,
    render_anomaly_review_panel,
    render_breadcrumb,
    render_section_header,
)

user = init_app_shell(
    "Add Expense",
    page_icon="material/add",
    header_title="New expense",
    header_subtitle="Record a transaction and update your spending history",
    header_icon="material/add",
)

render_breadcrumb("Transactions", "New expense")

user_id = user["id"]

render_section_header(
    "Transaction details",
    "Complete the form below to record a new expense",
    band=True,
)

with st.form("expense_form"):
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<p class="form-section-label">Basic info</p>', unsafe_allow_html=True)
        expense_date = st.date_input("Expense date")
        category = st.selectbox(
            "Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Education",
                "Health",
                "Entertainment",
                "Other",
            ],
        )
        amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)

    with col_right:
        st.markdown('<p class="form-section-label">Payment & notes</p>', unsafe_allow_html=True)
        payment_mode = st.selectbox(
            "Payment mode",
            [
                "Cash",
                "UPI",
                "Debit Card",
                "Credit Card",
                "Net Banking",
            ],
        )
        description = st.text_area(
            "Description",
            placeholder="Optional notes about this expense…",
            height=148,
        )

    submit = st.form_submit_button("Save expense", use_container_width=True)

    if submit:
        unusual, limit = is_unusual_expense(category, amount)

        if unusual:
            st.session_state.pending_expense = {
                "date": expense_date.strftime("%Y-%m-%d"),
                "category": category,
                "amount": amount,
                "payment": payment_mode,
                "description": description,
            }
            st.session_state.pending_expense_limit = limit

            st.warning(
                f"This expense exceeds the typical limit of ₹{limit:,.2f} for {category}. "
                "Review the details below before confirming.",
                icon=":material/warning:",
            )

        else:
            add_expense(
                user_id,
                expense_date.strftime("%Y-%m-%d"),
                category,
                amount,
                payment_mode,
                description,
            )

            st.success("Expense added successfully", icon=":material/check_circle:")

if "pending_expense" in st.session_state:
    p = st.session_state.pending_expense
    limit = st.session_state.get("pending_expense_limit")

    render_anomaly_review_panel(p, limit=limit)

    action_col1, action_col2 = st.columns(2)

    with action_col1:
        if st.button("Confirm & save", type="primary", use_container_width=True):
            add_expense(
                user_id,
                p["date"],
                p["category"],
                p["amount"],
                p["payment"],
                p["description"],
            )

            del st.session_state.pending_expense
            if "pending_expense_limit" in st.session_state:
                del st.session_state.pending_expense_limit

            st.success("Expense saved", icon=":material/check_circle:")
            st.rerun()

    with action_col2:
        if st.button("Discard", use_container_width=True):
            del st.session_state.pending_expense
            if "pending_expense_limit" in st.session_state:
                del st.session_state.pending_expense_limit
            st.rerun()
