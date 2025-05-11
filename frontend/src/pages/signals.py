import streamlit as st

from handlers.signals import SignalsHandler
from handlers.auth import AuthHandler

def signals_page(auth_handler: AuthHandler, signals_handler: SignalsHandler):
    st.header("📡 Signal Generation")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        ml_enabled = st.toggle("Use ML Model (10 TUG)", value=True)
        symbol = st.selectbox('What Symbol to Signal Generate', options=['BTC', 'ETH'])
        if st.button("Generate Signal"):
            with st.spinner("Generating signal..."):
                signal = signals_handler.request_signal(
                    symbol=symbol,
                    signal_type='ML' if ml_enabled else 'TECHNICAL',
                    token=auth_handler.access_token
                )
                display_signal(signal)

    with col2:
        st.metric("Current Balance", f"{auth_handler.current_user.tugrik_balance:.2f} TUG")

def display_signal(data):
    st.success("Signal generated successfully!")
    with st.expander("Signal Details", expanded=True):
        st.write(f"**Suggestion:** {data['response']['suggestion']}")
        st.write(f"**Type:** {data['signal_type']}")
        st.write(f"**Status:** {data['status']}")