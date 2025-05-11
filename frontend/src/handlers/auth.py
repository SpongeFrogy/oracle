from typing import Tuple, Optional, Dict
import requests
import streamlit as st
from datetime import datetime
from pydantic import BaseModel

class UserData(BaseModel):
    email: str
    username: str
    is_active: bool
    id: int
    tugrik_balance: float
    created_at: datetime
    updated_at: datetime

class AuthHandler:
    """Authentication handler with API integration"""
    
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url
        self._init_session_state()
        
    def _init_session_state(self):
        """Initialize authentication state"""
        if 'auth' not in st.session_state:
            st.session_state.auth = {
                'access_token': None,
                'current_user': None,
                'last_login': None
            }
    
    @property
    def access_token(self) -> Optional[str]:
        return st.session_state.auth['access_token']
    
    @property
    def current_user(self) -> Optional[UserData]:
        self._fetch_current_user()
        return UserData(**st.session_state.auth['current_user']) if st.session_state.auth['current_user'] else None
    
    def _api_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Base API request handler"""
        url = f"{self.api_base_url}{endpoint}"
        headers = kwargs.pop('headers', {})
        
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                **kwargs
            )
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            st.error(f"API Error: {e.response.text}")
            raise
        except requests.exceptions.ConnectionError:
            st.error("Connection to server failed")
            raise
    
    def register(self, email: str, username: str, password: str) -> bool:
        """Register new user through API"""
        try:
            response = self._api_request(
                'POST',
                '/api/auth/register',
                json={
                    "email": email,
                    "username": username,
                    "password": password,
                    "is_active": True
                }
            )
            if response.status_code == 200:
                st.success("Registration successful! Please login")
                return True
            return False
        except:
            return False
    
    def login(self, username: str, password: str) -> bool:
        """Authenticate user through API"""
        try:
            response = requests.post(
                f"{self.api_base_url}/api/auth/login",
                data={
                    "username": username,
                    "password": password,
                }
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state.auth.update({
                    'access_token': data['access_token'],
                    'last_login': datetime.now(),
                })
                self._fetch_current_user()
                return True
            st.error("Invalid credentials")
            return False
        except requests.exceptions.RequestException as e:
            st.error(f"Login failed: {str(e)}")
            return False
    
    def _fetch_current_user(self):
        """Fetch current user data from API"""
        try:
            response = self._api_request('GET', '/api/users/me')
            st.session_state.auth['current_user'] = response.json()
        except:
            st.session_state.auth['current_user'] = None
    
    def update_user(self, email: str, username: str, password: str) -> bool:
        """Update user profile through API"""
        try:
            response = self._api_request(
                'PUT',
                '/api/users/me',
                json={
                    "email": email,
                    "username": username,
                    "password": password
                }
            )
            if response.status_code == 200:
                self._fetch_current_user()
                return True
            return False
        except:
            return False
    
    def logout(self):
        """Clear authentication state"""
        st.session_state.auth = {
            'access_token': None,
            'current_user': None,
            'last_login': None
        }
        st.success("Successfully logged out")
    
    @property
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.access_token is not None and self.current_user is not None
    
    def get_auth_header(self) -> Dict[str, str]:
        """Get authorization header for API requests"""
        return {"Authorization": f"Bearer {self.access_token}"}
    
    def get_user_balance(self) -> float:
        """Get current user's balance"""
        return self.current_user.tugrik_balance if self.is_authenticated else 0.0