import streamlit as st
import pyrebase

# Configuration instructions for the user
# Create a .streamlit/secrets.toml file with the following structure:
# [firebase]
# apiKey = "..."
# authDomain = "..."
# databaseURL = "..."
# projectId = "..."
# storageBucket = "..."
# messagingSenderId = "..."
# appId = "..."

def initialize_firebase():
    config = {
        "apiKey": "AIzaSyBB0Gu7rrzIn8Aj1kcnaMykQoly9jqfKXg",
        "authDomain": "trustield-ai.firebaseapp.com",
        "projectId": "trustield-ai",
        "storageBucket": "trustield-ai.firebasestorage.app",
        "messagingSenderId": "694387029780",
        "appId": "1:694387029780:web:131f2bc3dec01fc7f23401",
        "measurementId": "G-CZFNDVK8MZ",
        "databaseURL": ""
    }
    
    try:
        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        return auth
    except Exception as e:
        st.error(f"Error initializing Firebase: {str(e)}")
        return None
