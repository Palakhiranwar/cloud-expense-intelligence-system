from datetime import timedelta

import plotly.express as px
import streamlit as st

from database.queries import get_all_expenses
from modules.analytics import create_expense_dataframe
from modules.ml_prediction import predict_ml_expense
from modules.prediction import predict_future_expense
from ui.components import (
    empty_state,
    init_app_shell,
    kpi_card,
    render_section_header
)
from ui.theme import (
    PLOTLY_COLOR_SEQUENCE,
    PLOTLY_LAYOUT,
    PLOTLY_LINE_STYLE
)


user = init_app_shell(
    "Dashboard",
    page_icon="material/analytics",
    header_title="Cost Overview",
    header_subtitle="Spending analytics, trends, and forecasts",
    header_icon="material/analytics",
)


user_id = user["id"]

expenses = get_all_expenses(user_id)

df = create_expense_dataframe(expenses)


if df.empty:

    empty_state(
        title="No expenses recorded yet",
        message="Add your first transaction to unlock spending analytics, charts, and forecasts.",
        action_label="Add Expense",
        action_page="pages/2_Add_Expense.py",
    )


else:

    min_date = df["expense_date"].min().date()
    max_date = df["expense_date"].max().date()


    if "dash_date_start" not in st.session_state:
        st.session_state.dash_date_start = min_date


    if "dash_date_end" not in st.session_state:
        st.session_state.dash_date_end = max_date


    if "dashboard_date_picker" not in st.session_state:
        st.session_state.dashboard_date_picker = (
            min_date,
            max_date
        )


    st.markdown(
        '<div class="filter-bar"><div class="filter-bar-title">Filters & date range</div></div>',
        unsafe_allow_html=True,
    )


    preset_cols = st.columns(4)


    with preset_cols[0]:

        if st.button(
            "All time",
            use_container_width=True,
            key="preset_all"
        ):

            st.session_state.dashboard_date_picker = (
                min_date,
                max_date
            )

            st.rerun()



    with preset_cols[1]:

        if st.button(
            "Last 30 days",
            use_container_width=True,
            key="preset_30d"
        ):

            start = max(
                max_date - timedelta(days=30),
                min_date
            )

            st.session_state.dashboard_date_picker = (
                start,
                max_date
            )

            st.rerun()



    with preset_cols[2]:

        if st.button(
            "Last 90 days",
            use_container_width=True,
            key="preset_90d"
        ):

            start = max(
                max_date - timedelta(days=90),
                min_date
            )

            st.session_state.dashboard_date_picker = (
                start,
                max_date
            )

            st.rerun()



    with preset_cols[3]:

        if st.button(
            "Year to date",
            use_container_width=True,
            key="preset_ytd"
        ):

            start = max_date.replace(
                month=1,
                day=1
            )

            if start < min_date:
                start = min_date


            st.session_state.dashboard_date_picker = (
                start,
                max_date
            )

            st.rerun()



    col_filter1, col_filter2, col_filter3 = st.columns(3)



    with col_filter1:

        selected_category = st.selectbox(
            "Category",
            ["All"] + sorted(df["category"].unique().tolist()),
        )



    with col_filter2:

        selected_payment_mode = st.selectbox(
            "Payment mode",
            ["All"] + sorted(df["payment_mode"].unique().tolist()),
        )



    with col_filter3:

        date_range = st.date_input(
            "Date range",
            key="dashboard_date_picker",
            min_value=min_date,
            max_value=max_date,
        )



    filtered_df = df.copy()



    if selected_category != "All":

        filtered_df = filtered_df[
            filtered_df["category"] == selected_category
        ]



    if selected_payment_mode != "All":

        filtered_df = filtered_df[
            filtered_df["payment_mode"] == selected_payment_mode
        ]



    if len(date_range) == 2:

        start_date, end_date = date_range

        filtered_df = filtered_df[
            (filtered_df["expense_date"].dt.date >= start_date)
            &
            (filtered_df["expense_date"].dt.date <= end_date)
        ]



    if filtered_df.empty:

        st.warning(
            "No expenses match the selected filters. Try adjusting your filters.",
            icon=":material/info:"
        )


    else:


        predict_future_expense(filtered_df)


        ml_prediction = predict_ml_expense(filtered_df)



        recent_prediction = (
            filtered_df
            .groupby(
                filtered_df["expense_date"].dt.to_period("M")
            )["amount"]
            .sum()
            .tail(3)
            .mean()
        )



        if ml_prediction and recent_prediction:

            difference = ml_prediction - recent_prediction

            difference_percent = (
                difference / recent_prediction
            ) * 100


        else:

            difference_percent = None



        total_expense = filtered_df["amount"].sum()

        highest_expense = filtered_df["amount"].max()

        total_transactions = len(filtered_df)



        top_category = (
            filtered_df.groupby("category")["amount"]
            .sum()
            .idxmax()
        )



        render_section_header(
            "Key metrics",
            "Summary for the selected period and filters",
            band=True,
        )



        cols = st.columns(4)


        with cols[0]:
            kpi_card(
                "Total spend",
                f"₹{total_expense:,.2f}"
            )


        with cols[1]:
            kpi_card(
                "Highest expense",
                f"₹{highest_expense:,.2f}"
            )


        with cols[2]:
            kpi_card(
                "Transactions",
                f"{total_transactions}"
            )


        with cols[3]:
            kpi_card(
                "Top category",
                top_category
            )



        render_section_header(
            "Forecast",
            "Projected spending based on recent patterns",
            band=True
        )



        fcols = st.columns(3)


        with fcols[0]:

            kpi_card(
                "Recent avg (3 mo)",
                f"₹{recent_prediction:,.2f}"
            )


        with fcols[1]:

            kpi_card(
                "ML prediction",
                f"₹{ml_prediction:,.2f}"
                if ml_prediction
                else "Not enough data"
            )


        with fcols[2]:

            kpi_card(
                "Prediction change",
                f"{difference_percent:.1f}%"
                if difference_percent
                else "N/A",
                delta=f"{difference_percent:+.1f}% vs avg"
                if difference_percent
                else None
            )



        render_section_header(
            "Visualizations",
            "Category breakdown and spending trend",
            band=True
        )


        category_data = (
            filtered_df
            .groupby("category")["amount"]
            .sum()
            .reset_index()
        )


        pie_fig = px.pie(
            category_data,
            names="category",
            values="amount",
            hole=0.45,
            color_discrete_sequence=PLOTLY_COLOR_SEQUENCE,
        )


        pie_fig.update_layout(
            **PLOTLY_LAYOUT,
            height=380
        )



        monthly_expense = (
            filtered_df
            .groupby(
                filtered_df["expense_date"].dt.to_period("M")
            )["amount"]
            .sum()
            .reset_index()
        )


        monthly_expense["expense_date"] = (
            monthly_expense["expense_date"]
            .dt.to_timestamp()
        )



        line_fig = px.line(
            monthly_expense,
            x="expense_date",
            y="amount",
            markers=True,
        )


        line_fig.update_traces(
            **PLOTLY_LINE_STYLE
        )


        line_fig.update_layout(
            **PLOTLY_LAYOUT,
            height=380
        )



        c1,c2 = st.columns(2)


        with c1:

            st.plotly_chart(
                pie_fig,
                use_container_width=True
            )


        with c2:

            st.plotly_chart(
                line_fig,
                use_container_width=True
            )



        render_section_header(
            "Transactions",
            "Detailed expense records"
        )


        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )



        csv = filtered_df.to_csv(
            index=False
        ).encode("utf-8")



        st.download_button(
            "Download CSV",
            csv,
            "expenses.csv",
            "text/csv"
        )