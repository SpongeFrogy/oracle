import streamlit as st
from handlers.auth import AuthHandler
from handlers.transactions import TransactionsHandler
from handlers.signals import SignalsHandler

from pages.transactions import transactions_page
from pages.signals import signals_page
from datetime import datetime
from config import settings

def main() -> None:
    """Main application entry point."""
    st.set_page_config(
        page_title="Oracle",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    auth = AuthHandler(settings.API_BASE_URL)
    transactions = TransactionsHandler(settings.API_BASE_URL)
    signals = SignalsHandler(settings.API_BASE_URL)
    
    if auth.is_authenticated:
        st.sidebar.title(f"👋 Welcome {auth.current_user.username}")
        
        with st.sidebar.expander("🔍 Account Details"):
            st.write(f"📧 Email: {auth.current_user.email}")
            st.write(f"🆔 User ID: {auth.current_user.id}")
            st.write(f"💰 Balance: {auth.current_user.tugrik_balance:.2f} TUG")
            st.write(f"📅 Joined: {auth.current_user.created_at.strftime('%d %b %Y')}")
            
        # Navigation radio
        app_page = st.sidebar.radio(
            "Navigation",
            ["📊 Trading", "💸 Transactions", "🫄🏼 Signals" , "⚙ Settings"],
            index=0
        )
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            auth.logout()
            st.rerun()

        if app_page == "📊 Trading":
            st.success("🎉 Successfully logged in!")
            st.write("Trading dashboard will be here")
            # dashboard = Dashboard()  # Раскомментируйте когда будет готов
            # dashboard.render()
            
        elif app_page == "💸 Transactions":
            transactions_page(auth, transactions)
        
        elif app_page == "🫄🏼 Signals":
            signals_page(auth, signals)
            
        elif app_page == "⚙ Settings":
            st.subheader("Account Settings")

    else:
        st.title("Welcome to Oracle Trading Platform")
        
        login_tab, register_tab = st.tabs(["🔑 Login", "📝 Register"])
        
        with login_tab:
            with st.form("Login Form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                
                if st.form_submit_button("Login"):
                    if auth.login(username, password):
                        st.rerun()
        
        with register_tab:
            with st.form("Register Form"):
                email = st.text_input("Email")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                
                if st.form_submit_button("Create Account"):
                    if password != confirm_password:
                        st.error("Passwords do not match!")
                    else:
                        if auth.register(email, username, password):
                            st.success("Account created successfully! Please login")
                            st.rerun()

if __name__ == "__main__":
    main()