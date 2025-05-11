import streamlit as st
import requests

class SignalsHandler:
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url
    
    def request_signal(self, symbol: str, signal_type: str, token: str) -> dict:
        try:
            response = requests.post(
                f"{self.api_base_url}/api/signals/for_money_yes",
                json={
                    'symbol': symbol,
                    'signal_type': signal_type
                },
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            st.error(f"Generation signal failed: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
        return None
