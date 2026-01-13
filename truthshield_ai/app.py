import streamlit as st
import time
from firebase_config import initialize_firebase
from message_verifier import MessageVerifier
from classifier import TopicClassifier

# Page Config
st.set_page_config(
    page_title="TruthShield AI",
    page_icon="🛡️",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
    .safe {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .unsafe {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .unverified {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeeba;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Components
auth = initialize_firebase()
verifier = MessageVerifier()
topic_classifier = TopicClassifier()

# Session State for User
if "user" not in st.session_state:
    st.session_state.user = None

def main():
    st.title("🛡️ TruthShield AI")
    st.markdown("### Verify WhatsApp Forwarded Messages using RAG")

    if not auth:
        st.warning("⚠️ Firebase configuration missing! Please add your keys to `.streamlit/secrets.toml`.")
        st.info("Check `firebase_config.py` for the required structure.")
        return

    # Authentication Section
    if not st.session_state.user:
        auth_choice = st.selectbox("Select Option", ["Login", "Sign Up"])
        
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        
        if auth_choice == "Sign Up":
            if st.button("Create Account"):
                try:
                    user = auth.create_user_with_email_and_password(email, password)
                    st.success("✅ Account created successfully! Please log in.")
                except Exception as e:
                    st.error(f"Signup Failed: {e}")
                    
        else: # Login
            if st.button("Login"):
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    st.session_state.user = user
                    st.success("Welcome back!")
                    st.rerun() # Refresh to show app
                except Exception as e:
                    st.error("Login Failed. Please check your credentials.")
    
    else:
        # Main App Interface (Protected)
        st.sidebar.title(f"👤 User: {st.session_state.user.get('email', 'Guest')}")
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.rerun()
            
        st.sidebar.markdown("---")
        st.sidebar.info("Supported Topics:\n- 🏥 Health\n- 🚜 Farming\n- 🌍 Environment")

        st.subheader("📝 Analyze Message")
        user_input = st.text_area("Paste the forwarded message here:", height=150)
        
        if st.button("Verify Message"):
            if user_input.strip():
                with st.spinner("Analyzing message content..."):
                    # 1. Classify Topic
                    topic = topic_classifier.predict(user_input)
                    st.caption(f"detected Data Context: {topic.capitalize()}")
                    
                    # 2. Verify with RAG
                    result = verifier.verify_message(user_input)
                    status = result["status"]
                    explanation = result["explanation"]
                    
                    # 3. Display Result
                    st.markdown("---")
                    st.subheader("Analysis Result")
                    
                    if status == "Safe":
                        st.markdown(f"""
                        <div class="safe">
                            <h3>🟢 SAFE</h3>
                            <p>{explanation}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    elif status == "Unsafe":
                        st.markdown(f"""
                        <div class="unsafe">
                            <h3>🔴 UNSAFE</h3>
                            <p>{explanation}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="unverified">
                            <h3>🟡 UNVERIFIED</h3>
                            <p>{explanation}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("Please enter a message to verify.")

if __name__ == "__main__":
    main()
