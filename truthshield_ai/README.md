# 🛡️ TruthShield AI

**TruthShield AI** is an intelligent web application designed to verify WhatsApp forwarded messages using Retrieval-Augmented Generation (RAG). It helps beginner users identify misinformation related to Health, Farming, and the Environment.

## 🎯 Purpose
The app checks if a message is:
- 🟢 **Safe** (Supported by verified data)
- 🔴 **Unsafe** (Contradicts verified data)
- 🟡 **Unverified** (No reliable evidence found)

## 🧠 How It Works (RAG Explanation)
TruthShield AI uses a technique called **Retrieval-Augmented Generation (RAG)** to provide accurate answers without guessing.
1. **Retrieve**: When you enter a message, the app searches its trusted database (`data/`) for relevant information pieces using vector similarity (FAISS).
2. **Augment**: It combines your message with these retrieved facts.
3. **Generate**: It sends this combined context to an AI model (Flan-T5) which decides if your message is true based *only* on the provided facts.

## 🌍 SDG Alignment
This project supports the United Nations Sustainable Development Goals:
- **SDG 3: Good Health & Well-being** (Combating health misinformation)
- **SDG 2: Zero Hunger** (Promoting sustainable farming practices)
- **SDG 12: Responsible Consumption** (Encouraging environmental awareness)

## 🚀 How to Run Locally

### Prerequisites
- Python 3.8+
- A Firebase project (for authentication)

### Steps
1. **Clone or Download** this repository.
2. Navigate to the project folder:
   ```bash
   cd truthshield_ai
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Secrets**:
   Create a file `.streamlit/secrets.toml` with your Firebase credentials:
   ```toml
   [firebase]
   apiKey = "your-api-key"
   authDomain = "your-project.firebaseapp.com"
   databaseURL = "https://your-project.firebaseio.com"
   projectId = "your-project-id"
   storageBucket = "your-project.appspot.com"
   messagingSenderId = "your-sender-id"
   appId = "your-app-id"
   ```
5. **Run the App**:
   ```bash
   streamlit run app.py
   ```

## ☁️ How to Deploy on Streamlit Cloud
1. Push your code to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and deploy your repository.
3. In the "Advanced Settings", copy the contents of your `secrets.toml` into the **Secrets** section.
4. Click **Deploy**!

## 🤝 Responsible AI Statement
TruthShield AI is designed to minimize hallucinations by strictly grounding its answers in provided trusted data. It is explicitly programmed to return "Unverified" when it cannot find sufficient evidence, rather than fabricating an answer. This "Refusal to Guess" is a core tenet of our Responsible AI approach.

---
*Created for IBM AI for Sustainability Internship Submission*
