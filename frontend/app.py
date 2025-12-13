import streamlit as st
import requests
import os

# --- CONFIGURATION ---
# Detect if running on Render or Localhost
BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
CHAT_API_URL = f"{BASE_URL}/api/v1/chat/"
UPLOAD_API_URL = f"{BASE_URL}/api/v1/docs/upload"

PAGE_TITLE = "TechGizmo AI Support"
PAGE_ICON = "🤖"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# --- SIDEBAR: NAVIGATION ---
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Go to:", ["💬 Chatbot", "⚙️ Admin Dashboard"])

# ==========================================
# MODE 1: CHATBOT INTERFACE
# ==========================================
if app_mode == "💬 Chatbot":
    st.title(f"{PAGE_ICON} {PAGE_TITLE}")
    st.markdown("Ask me about our **Refund Policy**, **Shipping**, or **Troubleshooting**!")

    # Session State for Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("How can I help you today?"):
        # Display User Message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Call Backend
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            try:
                response = requests.post(CHAT_API_URL, json={"query": prompt}, timeout=60)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data.get("sources", [])
                    
                    if sources:
                        source_list = ", ".join(sources)
                        final_response = f"{answer}\n\n*Sources: {source_list}*"
                    else:
                        final_response = answer
                        
                    message_placeholder.markdown(final_response)
                    st.session_state.messages.append({"role": "assistant", "content": final_response})
                else:
                    message_placeholder.error(f"❌ Error: {response.text}")
            
            except Exception as e:
                message_placeholder.error(f"❌ Connection Error: {e}")

# ==========================================
# MODE 2: ADMIN DASHBOARD
# ==========================================
elif app_mode == "⚙️ Admin Dashboard":
    st.title("⚙️ Knowledge Base Manager")
    st.markdown("Upload new policy documents or FAQs here to update the AI's brain instantly.")
    st.divider()

    # 1. Admin Authentication
    admin_key = st.text_input("Enter Admin API Key", type="password")
    
    # 2. File Uploader
    uploaded_file = st.file_uploader("Choose a text file", type=["txt", "md", "csv"])

    # 3. Upload Button
    if st.button("🚀 Upload & Ingest Document"):
        if not admin_key:
            st.error("❌ Please enter the Admin API Key.")
        elif not uploaded_file:
            st.error("❌ Please select a file.")
        else:
            with st.spinner("Uploading and Indexing..."):
                try:
                    # Prepare the file and headers
                    files = {"file": (uploaded_file.name, uploaded_file, "text/plain")}
                    headers = {"x-api-key": admin_key}
                    
                    # Send to Backend
                    response = requests.post(UPLOAD_API_URL, headers=headers, files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"✅ Success! File '{data['filename']}' ingested.")
                        st.info(f"💾 Chunks created: {data['chunks_ingested']}")
                    elif response.status_code == 403:
                        st.error("❌ Permission Denied: Invalid Admin Key.")
                    else:
                        st.error(f"❌ Upload Failed: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ Connection Error: {e}")

    st.divider()
    st.caption("Note: Supports .txt and .md files. Updates apply immediately to the Chatbot.")