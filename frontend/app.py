import streamlit as st
import requests

# --- CONFIGURATION ---
BACKEND_URL = "http://127.0.0.1:8000/api/v1/chat/"
PAGE_TITLE = "TechGizmo AI Support"
PAGE_ICON = "🤖"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# --- HEADER ---
st.title(f"{PAGE_ICON} {PAGE_TITLE}")
st.markdown("Ask me about our **Refund Policy**, **Shipping**, or **Troubleshooting**!")

# --- SESSION STATE (Memory) ---
# This keeps the chat history alive while you use the app
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- USER INPUT ---
if prompt := st.chat_input("How can I help you today?"):
    # 1. Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Add to History
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Call Backend API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Send request to your FastAPI backend
                response = requests.post(
                    BACKEND_URL, 
                    json={"query": prompt},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data.get("sources", [])
                    
                    # Format Sources nicely
                    if sources:
                        source_list = ", ".join(sources)
                        final_response = f"{answer}\n\n*Source: {source_list}*"
                    else:
                        final_response = answer
                        
                    st.markdown(final_response)
                    
                    # Add to History
                    st.session_state.messages.append({"role": "assistant", "content": final_response})
                
                elif response.status_code == 429:
                    st.error("⚠️ Rate limit exceeded. Please wait a moment.")
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the Backend. Is it running?")