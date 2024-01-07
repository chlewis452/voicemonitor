import streamlit as st
import os
import hashlib

# File to store user credentials
USER_CREDENTIALS_FILE = "user_credentials.txt"

# Function to create a new user and password combination
def create_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with open(USER_CREDENTIALS_FILE, "a") as file:
        file.write(f"{username}:{hashed_password}\n")

# Function to authenticate users
def authenticate(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with open(USER_CREDENTIALS_FILE, "r") as file:
        lines = file.readlines()
        for line in lines:
            stored_username, stored_hashed_password = line.strip().split(":")
            if username == stored_username and hashed_password == stored_hashed_password:
                return True
    return False

# Streamlit app
def main():
    st.title("Secure Audio App")

    # Check if the user_credentials file exists, create it if not
    if not os.path.exists(USER_CREDENTIALS_FILE):
        with open(USER_CREDENTIALS_FILE, "w"):
            pass

    # Home page with login and user creation
    if 'login' not in st.session_state:
        st.session_state.login = False

    if not st.session_state.login:
        st.header("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate(username, password):
                st.success("Login successful!")
                st.session_state.login = True
            else:
                st.error("Invalid credentials. Try again.")

        st.header("Create New User")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")

        if st.button("Create User"):
            create_user(new_username, new_password)
            st.success("User created successfully!")

    # Authenticated page with audio upload widget
    else:
        st.header("Audio Upload")

        uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav"])

        if uploaded_file is not None:
            st.audio(uploaded_file, format='audio/wav')

if __name__ == "__main__":
    main()