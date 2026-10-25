import streamlit as st
import bcrypt
from database import conn

cursor = conn.cursor()

# ============================
# Password Functions
# ============================

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


# ============================
# Register User
# ============================

def register_user(name, email, username, password):

    hashed = hash_password(password)

    try:
        cursor.execute("""
        INSERT INTO users(full_name,email,username,password)
        VALUES(?,?,?,?)
        """, (name, email, username, hashed))

        conn.commit()
        return True

    except Exception:
        return False


# ============================
# Login User
# ============================

def login_user(username, password):

    cursor.execute("""
    SELECT * FROM users
    WHERE username=?
    """, (username,))

    user = cursor.fetchone()

    if user is None:
        return None

    if verify_password(password, user[4]):
        return user

    return None


# ============================
# Register Page
# ============================

def register_page():

    st.title("📝 Register")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Create Account"):

        if not all([name, email, username, password, confirm]):
            st.error("Please fill all fields.")
            return

        if password != confirm:
            st.error("Passwords do not match.")
            return

        success = register_user(
            name,
            email,
            username,
            password
        )

        if success:
            st.success("Registration Successful! Please login.")
        else:
            st.error("Username or Email already exists.")


# ============================
# Login Page
# ============================

def login_page():

    st.title("🔐 Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = login_user(
            username,
            password
        )

        if user:

            st.session_state.logged_in = True
            st.session_state.username = user[3]
            st.session_state.name = user[1]

            st.success("Login Successful!")

            st.rerun()

        else:

            st.error("Invalid Username or Password")


# ============================
# Logout
# ============================

def logout():

    st.session_state.clear()
    st.rerun()