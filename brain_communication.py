# brain_communication.py
import os
import threading
from flask import Flask, request, jsonify
import streamlit as st

# Flask Server Setup
app = Flask(__name__)

# Secure communication settings
DEFAULT_PASSWORD = "securepassword"
DEFAULT_PORT = 5000
password = os.getenv("BRAIN_COMM_PASSWORD", DEFAULT_PASSWORD)
messages = []

@app.route('/send_message', methods=['POST'])
def send_message():
    """Endpoint to handle incoming messages."""
    data = request.json
    if not data or "message" not in data or "token" not in data:
        return jsonify({"error": "Invalid request format"}), 400

    if data["token"] != password:
        return jsonify({"error": "Unauthorized"}), 403

    # Add message to the conversation
    messages.append({"sender": "Remote Brain", "message": data["message"]})
    return jsonify({"success": True}), 200

def run_flask():
    """Run the Flask app on a separate thread."""
    app.run(host='0.0.0.0', port=DEFAULT_PORT, debug=False, use_reloader=False)

# Streamlit UI
def streamlit_ui():
    """Streamlit UI for interaction with the Flask server."""
    st.title("AI Brain Communication")

    # Configurations
    st.sidebar.header("Configuration")
    port = st.sidebar.number_input("Port", min_value=1, max_value=65535, value=DEFAULT_PORT)
    local_password = st.sidebar.text_input("Password", value=DEFAULT_PASSWORD, type="password")

    # Display current conversation
    st.header("Conversation")
    for msg in messages:
        st.markdown(f"**{msg['sender']}**: {msg['message']}")

    # Message sending
    st.header("Send a Message")
    target_url = st.text_input("Target Brain URL", f"http://localhost:{port}/send_message")
    user_message = st.text_area("Your Message")
    if st.button("Send"):
        if user_message.strip():
            # Send message to the target brain
            import requests
            payload = {"message": user_message, "token": local_password}
            try:
                response = requests.post(target_url, json=payload)
                if response.status_code == 200:
                    messages.append({"sender": "You", "message": user_message})
                    st.success("Message sent successfully!")
                else:
                    st.error(f"Failed to send message: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the target brain: {e}")
        else:
            st.error("Message cannot be empty!")

if __name__ == '__main__':
    # Run Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start Streamlit UI
    streamlit_ui()
