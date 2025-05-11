import streamlit as st

from handlers.auth import AuthHandler
from handlers.transactions import TransactionsHandler, TransactionCreate, TransactionType


def transactions_page(auth_handler: AuthHandler, transactions_handler: TransactionsHandler):
    st.header("💰 Transaction Management")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Balance", f"{auth_handler.current_user.tugrik_balance:.2f} TUG")

    with st.expander("Create New Transaction", expanded=True):
        with st.form("transaction_form"):
            trans_type = st.selectbox(
                "Type",
                [TransactionType.DEPOSIT.value, TransactionType.WITHDRAWAL.value],
                format_func=lambda x: x.replace("_", " ").title()
            )
            amount = st.number_input("Amount", min_value=0.01, step=0.01)
            description = st.text_area("Description")
            
            if st.form_submit_button("Submit Transaction"):
                print(trans_type.upper().replace(' ', '_'))
                transaction = TransactionCreate(
                    amount=amount,
                    type=trans_type.upper().replace(' ', '_'),
                    description=description
                )
                result = transactions_handler.create_transaction(transaction, auth_handler.access_token)
                if result:
                    st.success("Transaction completed successfully!")
                    auth_handler._fetch_current_user()
                    st.rerun()
    
    st.subheader("Transaction History")
    page_size = 10
    page_number = st.number_input("Page", min_value=1, value=1) - 1
    transactions = transactions_handler.get_transactions(
        auth_handler.access_token, 
        skip=page_number * page_size,
        limit=page_size
    )

    if transactions:
        for transaction in transactions:
            with st.container(border=True):
                cols = st.columns([1,2,1,2])
                status_color = "🟢" if transaction.status == "completed" else "🟡"
                cols[0].write(f"{status_color} **{transaction.status.title()}**")
                cols[1].write(f"**{transaction.type.replace('_', ' ').title()}**")
                cols[2].write(f"**{transaction.amount:.2f} TUG**")
                cols[3].write(transaction.created_at.strftime("%Y-%m-%d %H:%M"))
                
                if transaction.description:
                    st.caption(transaction.description)
                
                with st.expander("View Details"):
                    detailed_trans = transactions_handler.get_transaction(
                        transaction.id, 
                        auth_handler.access_token
                    )
                    if detailed_trans:
                        st.json(detailed_trans.dict())
    else:
        st.info("No transactions found")