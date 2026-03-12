import streamlit as st
import pandas as pd
from database import (
    initialize_database, create_user, verify_user, username_exists,
    get_all_wishlist_items, get_wishlist_item_by_id, create_wishlist_item,
    delete_wishlist_item, update_wishlist_item_name, add_transaction,
    get_transactions_by_item_id, get_all_transactions, get_total_savings,
    calculate_progress_percentage, get_progress_color
)
from export_csv import export_all_transactions_to_csv, export_item_transactions_to_csv
from constants import COLORS, FONTS


# ============================================
# CUSTOM RERUN FUNCTION
# ============================================

def rerun():
    st.markdown("<script>window.location.reload()</script>", unsafe_allow_html=True)


# ============================================
# CLOSE ALL POPUPS
# ============================================

def close_all_popups():
    # Close add wishlist
    st.session_state.show_add_popup = False
    
    # Get all wishlist items to close their popups
    try:
        user = st.session_state.user
        items = get_all_wishlist_items(user['id'])
        for item in items:
            st.session_state[f"show_add_money_{item['id']}"] = False
            st.session_state[f"show_rename_{item['id']}"] = False
            st.session_state[f"show_delete_{item['id']}"] = False
            st.session_state[f"show_history_{item['id']}"] = False
    except:
        pass


# ============================================
# DATABASE INITIALIZATION
# ============================================

try:
    initialize_database()
except Exception as e:
    st.error(f"Database error: {str(e)}")


# ============================================
# SESSION STATE SETUP
# ============================================

if 'user' not in st.session_state:
    st.session_state.user = None

if 'page' not in st.session_state:
    st.session_state.page = 'login'

if 'show_all_transactions' not in st.session_state:
    st.session_state.show_all_transactions = False

if 'show_add_popup' not in st.session_state:
    st.session_state.show_add_popup = False


# ============================================
# CUSTOM CSS
# ============================================

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {COLORS['bg_main']};
    }}
    .title-text {{
        font-family: 'Courier New', monospace;
        font-size: 28px;
        font-weight: bold;
        color: {COLORS['primary']};
        text-align: center;
    }}
    .heading-text {{
        font-family: 'Courier New', monospace;
        font-size: 16px;
        font-weight: bold;
        color: {COLORS['primary']};
    }}
    .normal-text {{
        font-family: 'Courier New', monospace;
        font-size: 12px;
        color: {COLORS['text_primary']};
    }}
    .card {{
        background-color: {COLORS['bg_card']};
        padding: 15px;
        border-radius: 5px;
        border: 1px solid {COLORS['border']};
        margin-bottom: 10px;
    }}
    .total-card {{
        background-color: {COLORS['primary']};
        padding: 15px;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 15px;
    }}
    .stButton>button {{
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)


# ============================================
# LOGOUT FUNCTION
# ============================================

def logout():
    try:
        st.session_state.user = None
        st.session_state.page = 'login'
        st.session_state.show_all_transactions = False
        close_all_popups()
        rerun()
    except Exception as e:
        st.error(f"Error logging out: {str(e)}")


# ============================================
# LOGIN PAGE
# ============================================

def show_login():
    try:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<p class='title-text'>W - L I S T</p>", unsafe_allow_html=True)
            st.markdown("<p class='heading-text' style='text-align:center'>LOGIN TO ACCOUNT</p>", 
unsafe_allow_html=True)
            
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("LOGIN", use_container_width=True):
                try:
                    if username and password:
                        user = verify_user(username, password)
                        if user:
                            st.session_state.user = user
                            st.session_state.page = 'app'
                            rerun()
                        else:
                            st.error("Invalid username or password!")
                    else:
                        st.error("Please enter username and password!")
                except Exception as e:
                    st.error(f"Login error: {str(e)}")
            
            st.markdown("<p class='normal-text'>Don't have account?</p>", unsafe_allow_html=True)
            if st.button("REGISTER HERE", use_container_width=True):
                st.session_state.page = 'register'
                rerun()
    except Exception as e:
        st.error(f"Error: {str(e)}")


# ============================================
# REGISTER PAGE
# ============================================

def show_register():
    try:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<p class='title-text'>W - L I S T</p>", unsafe_allow_html=True)
            st.markdown("<p class='heading-text' style='text-align:center'>CREATE ACCOUNT</p>", 
unsafe_allow_html=True)
            
            username = st.text_input("Username", key="reg_user")
            password = st.text_input("Password", type="password", key="reg_pass")
            confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.button("REGISTER", use_container_width=True):
                try:
                    if username and password and confirm:
                        if password != confirm:
                            st.error("Passwords do not match!")
                        elif len(password) < 4:
                            st.error("Password must be at least 4 characters!")
                        elif username_exists(username):
                            st.error("Username already exists!")
                        else:
                            user_id = create_user(username, password)
                            if user_id:
                                st.session_state.user = {'id': user_id, 'username': username}
                                st.session_state.page = 'app'
                                rerun()
                            else:
                                st.error("Failed to create account!")
                    else:
                        st.error("Please fill all fields!")
                except Exception as e:
                    st.error(f"Registration error: {str(e)}")
            
            st.markdown("<p class='normal-text'>Already have account?</p>", unsafe_allow_html=True)
            if st.button("LOGIN HERE", use_container_width=True):
                st.session_state.page = 'login'
                rerun()
    except Exception as e:
        st.error(f"Error: {str(e)}")


# ============================================
# MAIN APP PAGE
# ============================================

def show_app():
    try:
        user = st.session_state.user
        user_id = user['id']
        
        # Header
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"<p style='font-family:Courier New;font-size:14px;color:#FFFFFF'>👤 Welcome, {user['username']}!</p>", unsafe_allow_html=True)
        with col2:
            if st.button("LOGOUT"):
                logout()
        
        st.markdown("<p class='title-text'>W - L I S T</p>", unsafe_allow_html=True)
        
        # Total Savings
        try:
            total = get_total_savings(user_id)
        except:
            total = 0.0
        
        st.markdown(f"""
            <div class='total-card'>
                <p style='font-family:Courier New;font-size:16px;font-weight:bold;color:#FFFFFF;margin:0'>
                    TOTAL SAVINGS: Rs {total:,.2f}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            try:
                transactions = get_all_transactions(user_id)
                csv_data = export_all_transactions_to_csv(transactions)
                if csv_data:
                    st.download_button(
                        label="DOWNLOAD CSV",
                        data=csv_data,
                        file_name="wlist_transactions.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Error loading CSV: {str(e)}")
        
        with col2:
            btn_text = "HIDE ALL TRANSACTIONS ▲" if st.session_state.show_all_transactions else "VIEW ALL TRANSACTIONS ▼"
            if st.button(btn_text, use_container_width=True):
                st.session_state.show_all_transactions = not st.session_state.show_all_transactions
                rerun()
        
        # Show/Hide All Transactions
        if st.session_state.show_all_transactions:
            try:
                show_all_transactions_popup(user_id)
            except Exception as e:
                st.error(f"Error loading transactions: {str(e)}")
        
        st.markdown("<p class='heading-text'>> M-LISTS</p>", unsafe_allow_html=True)
        st.markdown("=" * 50)
        
        # Show wishlists
        try:
            items = get_all_wishlist_items(user_id)
        except:
            items = []
        
        if not items:
            st.markdown("<p class='normal-text' style='text-align:center'>No wishlists yet. Click [ + ADD NEW WISHLIST ] to start!</p>", unsafe_allow_html=True)
        else:
            for item in items:
                try:
                    show_wishlist_card(item, user_id)
                except Exception as e:
                    st.error(f"Error loading item: {str(e)}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Add new wishlist button
        if st.button("+ ADD NEW WISHLIST", use_container_width=True):
            close_all_popups()
            st.session_state.show_add_popup = True
            rerun()
        
        if st.session_state.get('show_add_popup', False):
            try:
                show_add_popup(user_id)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    except Exception as e:
        st.error(f"Error: {str(e)}")


# ============================================
# WISHLIST CARD
# ============================================

def show_wishlist_card(item, user_id):
    try:
        toggle_key = f"show_actions_{item['id']}"
        if toggle_key not in st.session_state:
            st.session_state[toggle_key] = False
        
        percentage = calculate_progress_percentage(item['total_saved'], item['target_price'])
        progress_color = get_progress_color(percentage)
        remaining = item['target_price'] - item['total_saved']
        
        icon_map = {
            "P": "[PHONE]", "L": "[LAPTOP]", "C": "[CAR]", "H": "[HOME]",
            "T": "[TRAVEL]", "G": "[GAME]", "Cam": "[CAMERA]", "W": "[WATCH]",
            "B": "[BIKE]", "Bi": "[BAG]", "Gi": "[GIFT]", "S": "[SPORTS]"
        }
        icon_text = icon_map.get(item['icon'], "[*]")
        
        percent_text = f"{percentage:.1f}%"
        if percentage >= 100:
            percent_text = "100% COMPLETED"
        
        # Display card
        st.markdown(f"""
            <div class='card'>
                <p style="font-family:Courier New;font-size:16px;color:{COLORS['primary']};margin:0">
                    {icon_text} <span style="color:{COLORS['text_primary']}">{item['item_name']}</span>
                </p>
                <div style="background-color:#220000;height:14px;border-radius:3px;margin:5px 0">
                    <div 
style="background-color:{progress_color};height:14px;width:{percentage}%;border-radius:3px"></div>
                </div>
                <p style="font-family:Courier New;font-size:12px;color:{COLORS['text_secondary']};margin:0">
                    Target: {item['currency']} {item['target_price']:,.0f} | 
                    <span style="color:{COLORS['success']}">Saved: {item['currency']} 
{item['total_saved']:,.0f}</span> | 
                    <span style="color:{COLORS['danger']}">Left: {item['currency']} {remaining:,.0f}</span>
                    <span style="float:right;color:{progress_color}">{percent_text}</span>
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Actions toggle button
        col0, col1, col2, col3, col4 = st.columns([3, 1, 1, 1, 1])
        with col0:
            btn_text = "HIDE ACTIONS ▲" if st.session_state[toggle_key] else "ACTIONS ▼"
            if st.button(btn_text, key=f"toggle_{item['id']}"):
                st.session_state[toggle_key] = not st.session_state[toggle_key]
                rerun()
        
        # Show action buttons if toggled
        if st.session_state[toggle_key]:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("ADD MONEY", key=f"add_{item['id']}"):
                    close_all_popups()
                    st.session_state[f"show_add_money_{item['id']}"] = True
            with col2:
                if st.button("RENAME", key=f"rename_{item['id']}"):
                    close_all_popups()
                    st.session_state[f"show_rename_{item['id']}"] = True
            with col3:
                if st.button("DELETE", key=f"delete_{item['id']}"):
                    close_all_popups()
                    st.session_state[f"show_delete_{item['id']}"] = True
            with col4:
                if st.button("HISTORY", key=f"history_{item['id']}"):
                    close_all_popups()
                    st.session_state[f"show_history_{item['id']}"] = True
            
            # Show popups
            if st.session_state.get(f"show_add_money_{item['id']}", False):
                try:
                    show_add_money_popup(item, user_id)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            if st.session_state.get(f"show_rename_{item['id']}", False):
                try:
                    show_rename_popup(item, user_id)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            if st.session_state.get(f"show_delete_{item['id']}", False):
                try:
                    show_delete_popup(item, user_id)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            if st.session_state.get(f"show_history_{item['id']}", False):
                try:
                    show_history_popup(item, user_id)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        st.markdown("<hr style='border-color:#330000'>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error displaying card: {str(e)}")


# ============================================
# ADD WISHLIST POPUP (No Form - No Auto Submit)
# ============================================

def show_add_popup(user_id):
    try:
        st.markdown("<p class='heading-text'>ADD NEW WISHLIST</p>", unsafe_allow_html=True)
        
        icons = ["P", "L", "C", "H", "T", "G", "Cam", "W", "B", "Bi", "Gi", "S"]
        icon_labels = {"P": "Phone", "L": "Laptop", "C": "Car", "H": "Home", "T": "Travel", "G": "Game", "Cam": 
"Camera", "W": "Watch", "B": "Bike", "Bi": "Bag", "Gi": "Gift", "S": "Sports"}
        
        selected_icon = st.selectbox("Select Icon", icons, format_func=lambda x: f"{icon_labels[x]} [{x}]")
        item_name = st.text_input("Item Name", key="new_item_name")
        target_price = st.number_input("Target Price", min_value=0.0, step=100.0, key="new_item_price")
        
        currencies = [("Rs", "INR"), ("$", "USD"), ("Euro", "EUR"), ("Pound", "GBP")]
        currency = st.selectbox("Currency", [c[0] for c in currencies], format_func=lambda x: x, 
key="new_item_currency")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("CANCEL", use_container_width=True):
                st.session_state.show_add_popup = False
                rerun()
        with col2:
            if st.button("CREATE", use_container_width=True):
                try:
                    if item_name and target_price > 0:
                        create_wishlist_item(user_id, selected_icon, item_name, currency, target_price)
                        st.session_state.show_add_popup = False
                        rerun()
                    else:
                        st.error("Please fill all fields!")
                except Exception as e:
                    st.error(f"Error creating item: {str(e)}")
    except Exception as e:
        st.error(f"Error: {str(e)}")


# ============================================
# ADD MONEY POPUP (No Form - No Auto Submit)
# ============================================

def show_add_money_popup(item, user_id):
    try:
        remaining = item['target_price'] - item['total_saved']
        curr = item['currency']
        
        st.markdown(f"<p class='heading-text'>ADD MONEY - {item['item_name']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='normal-text'>Target: {curr} {item['target_price']:,.0f} | Already Saved: {curr} {item['total_saved']:,.0f} | Remaining: {curr} {remaining:,.0f}</p>", unsafe_allow_html=True)
        
        amount = st.number_input(f"Amount to Add ({curr})", min_value=0.0, step=100.0, key=f"amount_{item['id']}")
        note = st.text_input("Note (Optional)", key=f"note_{item['id']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("CANCEL", key=f"cancel_add_{item['id']}", use_container_width=True):
                st.session_state[f"show_add_money_{item['id']}"] = False
                rerun()
        with col2:
            if st.button("ADD MONEY", key=f"addmoney_{item['id']}", use_container_width=True):
                try:
                    if amount > 0 and amount <= remaining:
                        add_transaction(user_id, item['id'], amount, note, curr)
                        st.session_state[f"show_add_money_{item['id']}"] = False
                        rerun()
                    else:
                        st.error(f"Amount must be between 0 and {remaining:,.0f}!")
                except Exception as e:
                    st.error(f"Error adding money: {str(e)}")
    except Exception as e:
        st.error(f"Error: {str(e)}")


# ============================================
# RENAME POPUP (No Form - No Auto Submit)
# ============================================

def show_rename_popup(item, user_id):
    try:
        st.markdown(f"<p class='heading-text'>RENAME: {item['item_name']}</p>", unsafe_allow_html=True)
        new_name = st.text_input("New Name", value=item['item_name'], key=f"new_name_{item['id']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("CANCEL", key=f"cancel_rename_{item['id']}", use_container_width=True):
                st.session_state[f"show_rename_{item['id']}"] = False
                rerun()
        with col2:
            if st.button("SAVE", key=f"save_rename_{item['id']}", use_container_width=True):
                try:
                    if new_name:
                        update_wishlist_item_name(user_id, item['id'], new_name)
                        st.session_state[f"show_rename_{item['id']}"] = False
                        rerun()
                    else:
                        st.error("Please enter a name!")
                except Exception as e:
                    st.error(f"Error renaming: {str(e)}")
    except Exception as e:
        st.error(f"Error: {str(e)}")


# ============================================
# DELETE POPUP
# ============================================

def show_delete_popup(item, user_id):
    try:
        st.error(f"WARNING! Delete: {item['item_name']}? All transaction history will be deleted!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("CANCEL", key=f"del_cancel_{item['id']}", use_container_width=True):
                st.session_state[f"show_delete_{item['id']}"] = False
                rerun()
        with col2:
            if st.button("DELETE", key=f"del_confirm_{item['id']}", use_container_width=True):
                try:
                    delete_wishlist_item(user_id, item['id'])
                    st.session_state[f"show_delete_{item['id']}"] = False
                    rerun()
                except Exception as e:
                    st.error(f"Error deleting: {str(e)}")
    except Exception as e:
        st.error(f"Error: {str(e)}")


# ============================================
# HISTORY POPUP
# ============================================

def show_history_popup(item, user_id):
    try:
        transactions = get_transactions_by_item_id(user_id, item['id'])
        curr = item['currency']
        
        total = sum(t['amount'] for t in transactions)
        st.markdown(f"<p class='heading-text'>HISTORY: {item['item_name']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='normal-text'>Transactions: {len(transactions)} | Total: {curr} {total:,.0f}</p>", 
unsafe_allow_html=True)
        
        if transactions:
            data = []
            for t in transactions:
                data.append({
                    'Date': t['transaction_date'],
                    'Time': t['transaction_time'],
                    'Amount': f"{curr} {t['amount']:,.0f}",
                    'Note': t['note'] or '-'
                })
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            
            try:
                csv_data = export_item_transactions_to_csv(item['item_name'], transactions)
                if csv_data:
                    st.download_button(
                        label="DOWNLOAD CSV",
                        data=csv_data,
                        file_name=f"wlist_{item['item_name']}.csv",
                        mime="text/csv"
                    )
            except:
                pass
        
        if st.button("CLOSE", key=f"close_{item['id']}"):
            st.session_state[f"show_history_{item['id']}"] = False
            rerun()
    except Exception as e:
        st.error(f"Error loading history: {str(e)}")


# ============================================
# ALL TRANSACTIONS POPUP
# ============================================

def show_all_transactions_popup(user_id):
    try:
        transactions = get_all_transactions(user_id)
        
        st.markdown("<p class='heading-text'>ALL TRANSACTIONS - GLOBAL VIEW</p>", unsafe_allow_html=True)
        total = sum(t['amount'] for t in transactions)
        st.markdown(f"<p class='normal-text'>Total: {len(transactions)} Transactions | Amount: Rs {total:,.0f}</p>", 
unsafe_allow_html=True)
        
        if transactions:
            data = []
            for t in transactions:
                data.append({
                    'Date': t['transaction_date'],
                    'Time': t['transaction_time'],
                    'Item': t['item_name'],
                    'Amount': f"{t['currency']} {t['amount']:,.0f}",
                    'Note': t['note'] or '-'
                })
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {str(e)}")


# ============================================
# MAIN EXECUTION
# ============================================

try:
    if st.session_state.page == 'login':
        show_login()
    elif st.session_state.page == 'register':
        show_register()
    elif st.session_state.page == 'app':
        show_app()
except Exception as e:
    st.error(f"Application error: {str(e)}")
