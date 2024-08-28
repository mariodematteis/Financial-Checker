from datetime import date

import streamlit as st

from financialchecker.database.mongodb.database import MongoDBCrud
from financialchecker.transactions.expense import Expense
from financialchecker.transactions.income import Income


def main():
    st.set_page_config(page_title="FinancialChecker")

    mongodb_instance: MongoDBCrud = MongoDBCrud()
    list_categories: list[str] = mongodb_instance.get_categories()
    list_payment_methods: list[str] = mongodb_instance.get_payment_methods()
    st.title("Add Transaction")
    list_firms: list[str] = mongodb_instance.get_firms()
    list_locations: list[str] = mongodb_instance.get_locations()

    with st.form("transaction_form"):
        transaction_date = st.date_input("Date", value=date.today())
        transaction_type = st.radio("Transaction Type", ["Expense", "Income"])
        transaction_category = st.selectbox("Category", list_categories)
        transaction_amount = st.number_input("Amount", min_value=0.01, format="%.2f")
        transaction_method = st.radio("Payment Method", list_payment_methods)
        transaction_firm = st.selectbox("Firm", options=list_firms)
        transaction_location = st.selectbox("Location", options=list_locations)
        transaction_advance_payment = st.checkbox("Advance Payment? \
            (If so, add details in the description)")

        transaction_description = st.text_area("Description",
                                               placeholder="Enter transaction details here...") # noqa E507

        submitted = st.form_submit_button("Add Transaction", use_container_width=True) # noqa E507

        match transaction_type:
            case "Expense":
                transaction: Expense = Expense(
                    transaction_category=transaction_category,
                    transaction_amount=transaction_amount,
                    transaction_method=transaction_method,
                    transaction_date=transaction_date,
                    transaction_advance_payment=transaction_advance_payment,
                    transaction_description=transaction_description,
                    transaction_firm=transaction_firm,
                    transaction_location=transaction_location,
                )
            case "Income":
                transaction: Income = Income(
                    transaction_category=transaction_category,
                    transaction_amount=transaction_amount,
                    transaction_method=transaction_method,
                    transaction_date=transaction_date,
                    transaction_description=transaction_description,
                )
            case _:
                st.error("Unable to recognize the following transaction type", icon="🚨")

        if submitted:
            mongodb_instance.add_transaction(transaction=transaction)
            st.success('Transaction correctly submitted!', icon="✅")


if __name__ == "__main__":
    main()
