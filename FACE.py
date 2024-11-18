#face.py
#default=python brain_communication.py
#specific=python brain_communication.py --port 6000 --peer_port 6001 --password my_secret_password
from pipin import install_requirements
install_requirements()

import streamlit as st
import requests
from flask import Flask, request, jsonify
import threading
import argparse

# Global variable to store conversation history
conversation_history = []

# Default ports and passwords
DEFAULT_PORT = 5000
DEFAULT_PEER_PORT = 5001
DEFAULT_PASSWORD = "secure_token"

# Streamlit UI setup
def streamlit_ui(peer_port, password):
    global conversation_history
    st.title("Brain Communication System")

    # Placeholders for conversation and input
    conversation = st.empty()
    user_input = st.text_input("Send a message to the other brain:")

    # Update conversation in real-time
    def update_conversation(new_message):
        conversation_history.append(new_message)
        conversation.text_area("Conversation", value="\n".join(conversation_history), height=400)

    # When user sends a message
    if user_input:
        new_message = f"Brain 1: {user_input}"
        update_conversation(new_message)
        status = send_message(user_input, peer_port, password)
        st.write(f"Message status: {status}")

# Flask app for receiving webhooks
app = Flask(__name__)

@app.route('/receive_message', methods=['POST'])
def receive_message():
    global conversation_history
    data = request.json
    token = data.get("token")
    message = data.get("message")

    # Verify the token (password) before accepting the message
    if token == app.config['password']:
        new_message = f"Brain 2: {message}"
        conversation_history.append(new_message)
        return jsonify({"status": "Message received and displayed!"})
    else:
        return jsonify({"status": "Unauthorized access!"}), 401

# Function to send a message to the other brain's webhook
def send_message(message, peer_port, password):
    payload = {
        "token": password,
        "message": message
    }
    try:
        # Send to the peer's port
        response = requests.post(f'http://localhost:{peer_port}/receive_message', json=payload)
        if response.status_code == 200:
            return response.json().get("status")
        else:
            return "Error sending message!"
    except requests.exceptions.RequestException as e:
        return f"Failed to send message: {e}"

# Webhook listener thread for Flask
def run_flask(port, password):
    app.config['password'] = password
    app.run(port=port)

# Start Flask in a separate thread so it doesn't block Streamlit
def start_flask_thread(port, password):
    flask_thread = threading.Thread(target=run_flask, args=(port, password))
    flask_thread.daemon = True
    flask_thread.start()

# Argument parser setup
def parse_arguments():
    parser = argparse.ArgumentParser(description="Brain Communication System")
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help='Port to run the Flask server (default: 5000)')
    parser.add_argument('--peer_port', type=int, default=DEFAULT_PEER_PORT, help='Port of the peer brain to communicate with (default: 5001)')
    parser.add_argument('--password', type=str, default=DEFAULT_PASSWORD, help='Password for secure communication (default: "secure_token")')
    return parser.parse_args()

# Entry point for the script
if __name__ == "__main__":
    args = parse_arguments()

    # Start the Flask server for webhooks
    start_flask_thread(args.port, args.password)

    # Launch the Streamlit UI and allow communication
    streamlit_ui(args.peer_port, args.password)
