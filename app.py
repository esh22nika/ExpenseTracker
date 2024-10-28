import streamlit as st
from streamlit_option_menu import option_menu
from database import Database
from user import User
from expense import Expense
import pandas as pd
import plotly.graph_objects as go
st.markdown("""
    <style>
    /* Sidebar style */
    .css-1d391kg {  /* Update the class as per Streamlit version for the sidebar */
        background-color: #1F2633 !important;
        color: #FFFFFF !important;
    }
    .css-1e5imcs {  /* Container for the sidebar */
        background-color: #1F2633 !important;
        color: #FFFFFF !important;
    }
    .sidebar-title {
        font-size: 18px;
        color: #FFFFFF;
        padding: 0px;
        margin: 10px;
    }
    .icon {
        font-size: 18px;
        color: #FFFFFF;
        padding-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


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

def app():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        with st.sidebar:
            selected = option_menu(
                "Navigation",
                ["Add Expense", "View Dashboard", "Update Expense", "Delete Expense","Set Expense Goals","Expense Statistics", "Logout"],
                icons=["plus-circle", "bar-chart-line", "pencil-square", "trash", "target", "stats-bars","box-arrow-right"],
                menu_icon="cast",
                default_index=0,
                styles={
                    "container": {"background-color": "#1F2633"},
                    "icon": {"color": "#FFFFFF"},
                    "nav-link": {
                        "font-size": "15px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#262B3D",
                    },
                    "nav-link-selected": {"background-color": "#262B3D"},
                },
            )

        if selected == "Add Expense":
            add_expense()
        elif selected == "View Dashboard":
            dashboard()
        elif selected == "Update Expense":
            update_expense()
        elif selected == "Delete Expense":
            delete_expense()
        elif selected == "Set Expense Goals":
            set_goals()
        elif selected == "Expense Statistics":
            stats_dashboard()
        elif selected == "Logout":
            st.session_state['logged_in'] = False
            st.success("Logged out successfully!")

    else:
        st.sidebar.title("Expense Tracker")
        page = st.sidebar.selectbox("Select Option", ["Login", "Register"])
        if page == "Login":
            login()
        else:
            register()

def add_expense():
    st.title("Add New Expense")
    categories = ["Food", "Transport", "Bills", "Entertainment", "Health", "Education", "Shopping", "Others"]
    expense_name = st.selectbox("Expense Category", options=categories)
    amount = st.number_input("Amount", min_value=0.0)
    expense_date = st.date_input("Expense Date")
    
    if st.button("Add Expense"):
        db.insert_expense(st.session_state['user_id'], expense_name, amount, str(expense_date))
        st.success("Expense added successfully!")

def dashboard():
    st.title("Expenses Dashboard")
    
    expenses = db.get_expenses(st.session_state['user_id'])
    
    if expenses:
        df = pd.DataFrame(expenses, columns=["ID", "User ID", "Expense", "Amount", "Date"])
        
        st.dataframe(df)
        
        st.bar_chart(df[['Amount']])

        category_data = df.groupby("Expense")["Amount"].sum()
        
        pie_fig = go.Figure(data=[go.Pie(
            labels=category_data.index,
            values=category_data.values,
            hole=0.3,  
            marker=dict(colors=['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#66FF66', '#FF6666'])
        )])
        
        pie_fig.update_layout(
            title="Expense Distribution by Category",
            showlegend=True
        )
        
        st.plotly_chart(pie_fig)

    else:
        st.warning("No expenses found for the user.")
        
def update_expense():
    st.title("Update Expense")
    expenses = db.get_expenses(st.session_state['user_id'])
    if expenses:
        expense_options = [f"{expense[2]} - rs{expense[3]} (ID: {expense[0]})" for expense in expenses]
        selected_expense = st.selectbox("Select Expense to Update", options=expense_options)
        
        selected_expense_id = int(selected_expense.split("(ID: ")[-1][:-1])

        expense_data = next(expense for expense in expenses if expense[0] == selected_expense_id)

        try:
            new_expense_name = st.selectbox("New Expense Category", options=["Food", "Transport", "Bills", "Entertainment", "Health", "Education", "Shopping", "Others"], 
                                             index=["Food", "Transport", "Bills", "Entertainment", "Health", "Education", "Shopping", "Others"].index(expense_data[2]))
        except ValueError:
            st.error("Invalid expense category selected. Please try again.")
            return

        new_amount = st.number_input("New Amount", min_value=0.0, value=expense_data[3])
        new_expense_date = st.date_input("New Expense Date", value=pd.to_datetime(expense_data[4]))

        if st.button("Update Expense"):
            db.update_expense(selected_expense_id, new_expense_name, new_amount, str(new_expense_date))
            st.success("Expense updated successfully!")
    else:
        st.error("No expenses found for the user.")



def delete_expense():
    st.title("Delete Expense")
    expenses = db.get_expenses(st.session_state['user_id'])
    if expenses:
        expense_options = [f"{expense[2]} - {expense[3]} (ID: {expense[0]})" for expense in expenses]
        selected_expense = st.selectbox("Select Expense to Delete", options=expense_options)
        
        selected_expense_id = int(selected_expense.split("(ID: ")[-1][:-1])

        if st.button("Delete Expense"):
            db.delete_expense(selected_expense_id)
            st.success("Expense deleted successfully!")
def set_goals():
    st.title("Set Expense Goals")
    
    weekly_goal = st.number_input("Weekly Expense Goal", min_value=0.0)
    monthly_goal = st.number_input("Monthly Expense Goal", min_value=0.0)

    if st.button("Save Goals"):
        db.set_goals(st.session_state['user_id'], weekly_goal, monthly_goal)
        st.success("Goals saved successfully!")

    current_goals = db.get_goals(st.session_state['user_id'])  
    if current_goals:
        st.write(f"Current Weekly Goal: rs {current_goals[0]}")
        st.write(f"Current Monthly Goal: rs {current_goals[1]}")

def stats_dashboard():
    st.title("Expense Goals & Statistics")
    
    weekly_goal, monthly_goal = db.get_goals(st.session_state['user_id'])
    weekly_expenses = db.get_weekly_expenses(st.session_state['user_id'])
    monthly_expenses = db.get_monthly_expenses(st.session_state['user_id'])

    if weekly_expenses > weekly_goal:
        st.warning(f"⚠️ You have exceeded your weekly goal by {weekly_expenses - weekly_goal:.2f}!")
    else:
        st.info(f"✅ You have {weekly_goal - weekly_expenses:.2f} left to spend this week!")

    if monthly_expenses > monthly_goal:
        st.warning(f"⚠️ You have exceeded your monthly goal by {monthly_expenses - monthly_goal:.2f}!")
    else:
        st.info(f"✅ You have {monthly_goal - monthly_expenses:.2f} left to spend this month!")

    weekly_fig = go.Figure()
    weekly_fig.add_trace(go.Bar(
        x=["Weekly Goal", "Weekly Expenses"],
        y=[weekly_goal, weekly_expenses],
        marker_color=["#4CAF50", "#FF5733"]
    ))
    weekly_fig.update_layout(
        title="Weekly Expenses vs Goal",
        xaxis_title="Category",
        yaxis_title="Amount",
    )
    st.plotly_chart(weekly_fig)

    monthly_fig = go.Figure()
    monthly_fig.add_trace(go.Bar(
        x=["Monthly Goal", "Monthly Expenses"],
        y=[monthly_goal, monthly_expenses],
        marker_color=["#4CAF50", "#FF5733"]
    ))
    monthly_fig.update_layout(
        title="Monthly Expenses vs Goal",
        xaxis_title="Category",
        yaxis_title="Amount",
    )
    st.plotly_chart(monthly_fig)

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

if __name__ == "__main__":
    app()