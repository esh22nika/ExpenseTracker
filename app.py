import streamlit as st
from database import Database
from user import User
from expense import Expense
import pandas as pd

db = Database('expenses.db')

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = db.validate_user(username, password)
        if user:
            st.session_state['logged_in'] = True
            st.session_state['user_id'] = user[0]
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials")

def register():
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        try:
            db.insert_user(username, password)
            st.success("User registered successfully!")
        except:
            st.error("User already exists")

def dashboard():
    st.title("Expenses Dashboard")
    
    if st.button("Logout"):
        st.session_state['logged_in'] = False
    
    expenses = db.get_expenses(st.session_state['user_id'])
    if expenses:
        df = pd.DataFrame(expenses, columns=["ID", "User ID", "Expense", "Amount", "Date"])
        st.dataframe(df)
        st.bar_chart(df[['Amount']])

    st.subheader("Add New Expense")
    expense_name = st.text_input("Expense Name")
    amount = st.number_input("Amount", min_value=0.0)
    expense_date = st.date_input("Expense Date")
    
    if st.button("Add Expense"):
        db.insert_expense(st.session_state['user_id'], expense_name, amount, str(expense_date))
        st.success("Expense added successfully!")

def app():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if st.session_state['logged_in']:
        dashboard()
    else:
        st.sidebar.title("Expense Tracker")
        page = st.sidebar.selectbox("Select Option", ["Login", "Register"])
        if page == "Login":
            login()
        else:
            register()

if __name__ == "__main__":
    app()
