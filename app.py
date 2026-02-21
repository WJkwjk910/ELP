import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import sqlite3
import hashlib
import os

# Page configuration
st.set_page_config(
    page_title="Entrepreneurial Learning Predictor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database setup for user management
DB_PATH = "users.db"

def init_db():
    """Initialize SQLite database for user management"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify password against hash"""
    return hash_password(password) == password_hash

def create_user(email, password, is_admin=False):
    """Create a new user"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO users (email, password_hash, is_admin)
            VALUES (?, ?, ?)
        ''', (email, hash_password(password), 1 if is_admin else 0))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(email, password):
    """Authenticate user"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT password_hash, is_admin FROM users WHERE email = ?', (email,))
    result = c.fetchone()
    conn.close()
    
    if result and verify_password(password, result[0]):
        return True, bool(result[1])
    return False, False

def get_all_users():
    """Get all users (admin only)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, email, is_admin, created_at FROM users')
    users = c.fetchall()
    conn.close()
    return users

def delete_user(user_id):
    """Delete a user (admin only)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Authentication page
if not st.session_state.authenticated:
    st.title("🔐 Login / Register")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if email and password:
                    success, is_admin = authenticate_user(email, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.is_admin = is_admin
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
                else:
                    st.error("Please enter both email and password")
    
    with tab2:
        with st.form("register_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Register")
            
            if submit:
                if email and password:
                    if create_user(email, password):
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error("Email already exists")
                else:
                    st.error("Please enter both email and password")
    
    st.stop()

# Main application
st.title("📈 Entrepreneurial Learning Predictor")
st.sidebar.write(f"Logged in as: {st.session_state.user_email}")
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.session_state.user_email = None
    st.session_state.is_admin = False
    st.rerun()

# Admin console
if st.session_state.is_admin:
    with st.sidebar.expander("🔧 Admin Console"):
        st.subheader("User Management")
        users = get_all_users()
        
        if users:
            for user_id, email, is_admin, created_at in users:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{email} {'(Admin)' if is_admin else ''}")
                with col2:
                    if st.button("Delete", key=f"delete_{user_id}"):
                        delete_user(user_id)
                        st.rerun()
        
        st.subheader("Add New User")
        with st.form("add_user_form"):
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            new_is_admin = st.checkbox("Admin")
            add_user = st.form_submit_button("Add User")
            
            if add_user:
                if new_email and new_password:
                    if create_user(new_email, new_password, new_is_admin):
                        st.success("User added successfully!")
                        st.rerun()
                    else:
                        st.error("Email already exists")
                else:
                    st.error("Please enter both email and password")

# Main tabs
tab1, tab2 = st.tabs(["Revenue Growth Predictor", "AI Investments Analysis"])

with tab1:
    st.header("Revenue Growth Rate Predictor")
    
    # Sidebar inputs
    st.sidebar.header("Initial Parameters")
    initial_revenue = st.sidebar.number_input(
        "Initial Revenue ($)",
        min_value=0.0,
        value=1000000.0,
        step=10000.0,
        format="%.2f"
    )
    
    initial_capital = st.sidebar.number_input(
        "Initial Capital ($)",
        min_value=0.0,
        value=500000.0,
        step=10000.0,
        format="%.2f"
    )
    
    initial_expense = st.sidebar.number_input(
        "Initial Expense ($)",
        min_value=0.0,
        value=1000000.0,
        step=10000.0,
        format="%.2f"
    )
    
    initial_growth_rate = st.sidebar.slider(
        "Initial Growth Rate (%)",
        min_value=0.0,
        max_value=99.0,
        value=20.0,
        step=0.1
    )
    
    st.sidebar.header("Variable Weights")
    
    # Independent variables with initial values
    competition = st.sidebar.slider(
        "Competition",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.01
    )
    
    new_entrant = st.sidebar.slider(
        "New Entrant",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.01
    )
    
    supplier_power = st.sidebar.slider(
        "Supplier's Bargaining Power",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.01
    )
    
    buyer_power = st.sidebar.slider(
        "Buyer's Bargaining Power",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.01
    )
    
    substitute = st.sidebar.slider(
        "Substitute",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.01
    )
    
    product_market_fit = st.sidebar.slider(
        "Product-Market Fit",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.01
    )
    
    differentiator = st.sidebar.slider(
        "Differentiator",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.01
    )
    
    st.sidebar.header("Leadership Learning")
    adaptive_learning = st.sidebar.slider(
        "Adaptive Learning",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.01
    )
    
    deep_learning = st.sidebar.slider(
        "Deep Learning",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.01
    )
    
    st.sidebar.header("Process Management")
    process_management = st.sidebar.slider(
        "Process Management",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.01
    )
    
    # Store initial values before applying leadership learning effects
    initial_competition = competition
    initial_supplier_power = supplier_power
    initial_buyer_power = buyer_power
    initial_differentiator = differentiator
    initial_substitute = substitute
    
    # Apply leadership learning effects to differentiator and substitute
    # Adaptive learning: +0.1 differentiator per 0.1 adaptive learning
    adjusted_differentiator = differentiator + adaptive_learning
    
    # Deep learning: +0.2 differentiator and -0.1 substitute per 0.1 deep learning
    adjusted_differentiator += deep_learning * 2
    adjusted_substitute = max(0.0, substitute - deep_learning)
    
    # Process management: +0.1 buyer power per 0.1 process
    adjusted_buyer_power = buyer_power + process_management
    
    # Ensure values stay within bounds
    adjusted_differentiator = min(1.0, adjusted_differentiator)
    adjusted_substitute = max(0.0, adjusted_substitute)
    adjusted_buyer_power = min(1.0, adjusted_buyer_power)
    
    # Calculate growth rates over 5 years
    years = list(range(1, 6))
    growth_rates = []
    revenues = []
    current_growth_rate = initial_growth_rate
    current_revenue = initial_revenue
    
    # Track variables over time (start with initial values)
    current_competition = initial_competition
    current_supplier_power = initial_supplier_power
    current_buyer_power = adjusted_buyer_power  # Start with adjusted value
    current_differentiator = adjusted_differentiator  # Start with adjusted value
    current_substitute = adjusted_substitute  # Start with adjusted value
    
    for year in years:
        # Calculate growth rate impact based on current variable values
        growth_change = 0
        
        # Direct impacts on growth rate
        growth_change -= current_competition * 10  # -1% per 0.1
        growth_change -= current_buyer_power * 10  # -1% per 0.1
        growth_change -= new_entrant * 10  # -1% per 0.1
        growth_change += current_supplier_power * 10  # +1% per 0.1
        growth_change -= current_substitute * 100  # -10% per 0.1
        growth_change += product_market_fit * 5  # +0.5% per 0.1
        growth_change += current_differentiator * 5  # +0.5% per 0.1
        
        # Update variables for next year based on relationships
        if year < 5:  # Don't update after year 5
            # Competition increases by at least 0.05 annually
            current_competition += 0.05
            
            # Competition increases by 0.05 if new entrant increases by 0.1
            # (Assuming new entrant can change, but for now it's user-controlled)
            # Competition decreases by 0.05 if supplier power increases by 0.1
            supplier_change = current_supplier_power - initial_supplier_power
            current_competition -= supplier_change * 0.5
            
            # Competition increases by 0.05 if buyer power increases by 0.1
            buyer_change = current_buyer_power - initial_buyer_power
            current_competition += buyer_change * 0.5
            
            # Competition decreases by 0.05 if differentiator increases by 0.1
            differentiator_change = current_differentiator - initial_differentiator
            current_competition -= differentiator_change * 0.5
            
            # Supplier power increases by 0.05 if differentiator increases by 0.1
            current_supplier_power += differentiator_change * 0.5
            
            # Buyer power increases by 0.05 if differentiator decreases by 0.1
            # (This would be negative change, so it decreases buyer power)
            if differentiator_change < 0:
                current_buyer_power += abs(differentiator_change) * 0.5
        
        # Ensure values stay within bounds
        current_competition = max(0.0, min(1.0, current_competition))
        current_supplier_power = max(0.0, min(1.0, current_supplier_power))
        current_buyer_power = max(0.0, min(1.0, current_buyer_power))
        current_differentiator = max(0.0, min(1.0, current_differentiator))
        current_substitute = max(0.0, min(1.0, current_substitute))
        
        # Apply growth change
        current_growth_rate = initial_growth_rate + growth_change
        current_growth_rate = max(0.0, current_growth_rate)  # Ensure non-negative
        
        growth_rates.append(current_growth_rate)
        current_revenue = current_revenue * (1 + current_growth_rate / 100)
        revenues.append(current_revenue)
    
    # Display charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Growth Rate Over Time")
        fig_growth = go.Figure()
        fig_growth.add_trace(go.Scatter(
            x=years,
            y=growth_rates,
            mode='lines+markers',
            name='Growth Rate (%)',
            line=dict(color='blue', width=2)
        ))
        fig_growth.update_layout(
            xaxis_title="Year",
            yaxis_title="Growth Rate (%)",
            title="Growth Rate Over 5 Years",
            hovermode='x unified'
        )
        st.plotly_chart(fig_growth, use_container_width=True)
    
    with col2:
        st.subheader("Revenue Over Time")
        fig_revenue = go.Figure()
        fig_revenue.add_trace(go.Scatter(
            x=years,
            y=revenues,
            mode='lines+markers',
            name='Revenue ($)',
            line=dict(color='green', width=2)
        ))
        fig_revenue.update_layout(
            xaxis_title="Year",
            yaxis_title="Revenue ($)",
            title="Revenue Over 5 Years",
            hovermode='x unified'
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    # Radar chart (using adjusted initial values)
    st.subheader("Variable Analysis (Radar Chart)")
    categories = ['Competition', 'New Entrant', 'Supplier Power', 'Buyer Power', 
                  'Substitute', 'Product-Market Fit', 'Differentiator']
    # Use initial values with leadership learning adjustments for radar chart
    values = [initial_competition, new_entrant, initial_supplier_power, adjusted_buyer_power, 
              adjusted_substitute, product_market_fit, adjusted_differentiator]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Current Values'
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title="Variable Weights Radar Chart"
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Sensitivity Analysis
    st.subheader("Sensitivity Analysis")
    sensitivity_variance = st.slider(
        "Sensitivity Variance (%)",
        min_value=80.0,
        max_value=120.0,
        value=100.0,
        step=1.0
    )
    
    # Calculate baseline, best case, and worst case scenarios
    baseline_growth_rates = growth_rates.copy()
    best_case_growth_rates = [g * (sensitivity_variance / 100) for g in growth_rates]
    worst_case_growth_rates = [g * (100 / sensitivity_variance) for g in growth_rates]
    
    fig_sensitivity = go.Figure()
    fig_sensitivity.add_trace(go.Scatter(
        x=years,
        y=baseline_growth_rates,
        mode='lines+markers',
        name='Baseline',
        line=dict(color='blue')
    ))
    fig_sensitivity.add_trace(go.Scatter(
        x=years,
        y=best_case_growth_rates,
        mode='lines+markers',
        name=f'Best Case ({sensitivity_variance}%)',
        line=dict(color='green')
    ))
    fig_sensitivity.add_trace(go.Scatter(
        x=years,
        y=worst_case_growth_rates,
        mode='lines+markers',
        name=f'Worst Case ({100/sensitivity_variance*100:.1f}%)',
        line=dict(color='red')
    ))
    fig_sensitivity.update_layout(
        xaxis_title="Year",
        yaxis_title="Growth Rate (%)",
        title="Sensitivity Analysis",
        hovermode='x unified'
    )
    st.plotly_chart(fig_sensitivity, use_container_width=True)
    
    # Cash Flow Table
    st.subheader("5-Year Cash Flow Projection")
    
    # Calculate expenses (compounding similar to revenue)
    expenses = []
    current_expense = initial_expense
    for g in growth_rates:
        current_expense = current_expense * (1 + g/100)
        expenses.append(current_expense)
    
    # Calculate cash flow
    cash_flow_data = {
        'Year': years,
        'Capital': [initial_capital] + [0] * 4,
        'Revenue': revenues,
        'Expense': expenses,
        'Net Profit': [],
        'Cumulative Cash': []
    }
    
    cumulative_cash = initial_capital
    for i in range(5):
        net_profit = cash_flow_data['Revenue'][i] - cash_flow_data['Expense'][i]
        cash_flow_data['Net Profit'].append(net_profit)
        cumulative_cash += net_profit
        cash_flow_data['Cumulative Cash'].append(cumulative_cash)
    
    df_cashflow = pd.DataFrame(cash_flow_data)
    df_cashflow['Capital'] = df_cashflow['Capital'].apply(lambda x: f"${x:,.2f}")
    df_cashflow['Revenue'] = df_cashflow['Revenue'].apply(lambda x: f"${x:,.2f}")
    df_cashflow['Expense'] = df_cashflow['Expense'].apply(lambda x: f"${x:,.2f}")
    df_cashflow['Net Profit'] = df_cashflow['Net Profit'].apply(lambda x: f"${x:,.2f}")
    df_cashflow['Cumulative Cash'] = df_cashflow['Cumulative Cash'].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(df_cashflow, use_container_width=True)
    
    # Revenue Projection Table with Sensitivity
    st.subheader("Revenue Projection with Sensitivity Analysis")
    
    baseline_revenues = revenues.copy()
    best_case_revenues = [r * (sensitivity_variance / 100) for r in revenues]
    worst_case_revenues = [r * (100 / sensitivity_variance) for r in revenues]
    
    df_projection = pd.DataFrame({
        'Year': years,
        'Baseline Revenue': [f"${r:,.2f}" for r in baseline_revenues],
        'Best Case Revenue': [f"${r:,.2f}" for r in best_case_revenues],
        'Worst Case Revenue': [f"${r:,.2f}" for r in worst_case_revenues]
    })
    
    st.dataframe(df_projection, use_container_width=True)

with tab2:
    st.header("AI Investments vs US New Business Apps Analysis")
    
    # Historical data
    years_historical = list(range(2015, 2024))
    ai_investments_historical = [24, 33, 53, 79, 95, 146, 276, 189, 252]
    us_business_apps_historical = [2.8, 2.9, 3.2, 3.5, 3.5, 4.3, 5.4, 5.0, 5.4]
    
    # Calculate growth rates
    ai_growth_rates = []
    apps_growth_rates = []
    
    for i in range(len(ai_investments_historical)):
        if i == 0:
            ai_growth_rates.append(0)
            apps_growth_rates.append(0)
        else:
            ai_growth = ((ai_investments_historical[i] - ai_investments_historical[i-1]) / 
                        ai_investments_historical[i-1]) * 100
            apps_growth = ((us_business_apps_historical[i] - us_business_apps_historical[i-1]) / 
                          us_business_apps_historical[i-1]) * 100
            ai_growth_rates.append(ai_growth)
            apps_growth_rates.append(apps_growth)
    
    # Sliders for adjustment
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("AI Investments Adjustment")
        ai_adjustments = []
        for i, year in enumerate(years_historical):
            adj = st.slider(
                f"AI Investments {year} ($ Billions)",
                min_value=0.0,
                max_value=500.0,
                value=float(ai_investments_historical[i]),
                step=1.0,
                key=f"ai_{year}"
            )
            ai_adjustments.append(adj)
    
    with col2:
        st.subheader("US New Business Apps Adjustment")
        apps_adjustments = []
        for i, year in enumerate(years_historical):
            adj = st.slider(
                f"US Business Apps {year} (Millions)",
                min_value=0.0,
                max_value=20.0,
                value=float(us_business_apps_historical[i]),
                step=0.1,
                key=f"apps_{year}"
            )
            apps_adjustments.append(adj)
    
    # Recalculate growth rates with adjustments
    ai_growth_rates_adj = []
    apps_growth_rates_adj = []
    
    for i in range(len(ai_adjustments)):
        if i == 0:
            ai_growth_rates_adj.append(0)
            apps_growth_rates_adj.append(0)
        else:
            ai_growth = ((ai_adjustments[i] - ai_adjustments[i-1]) / 
                        ai_adjustments[i-1]) * 100 if ai_adjustments[i-1] > 0 else 0
            apps_growth = ((apps_adjustments[i] - apps_adjustments[i-1]) / 
                          apps_adjustments[i-1]) * 100 if apps_adjustments[i-1] > 0 else 0
            ai_growth_rates_adj.append(ai_growth)
            apps_growth_rates_adj.append(apps_growth)
    
    # Predict 2024 and 2025
    # Simple linear trend prediction
    ai_avg_growth = np.mean(ai_growth_rates_adj[-3:]) if len(ai_growth_rates_adj) >= 3 else 0
    apps_avg_growth = np.mean(apps_growth_rates_adj[-3:]) if len(apps_growth_rates_adj) >= 3 else 0
    
    ai_2024 = ai_adjustments[-1] * (1 + ai_avg_growth / 100)
    ai_2025 = ai_2024 * (1 + ai_avg_growth / 100)
    
    apps_2024 = apps_adjustments[-1] * (1 + apps_avg_growth / 100)
    apps_2025 = apps_2024 * (1 + apps_avg_growth / 100)
    
    # Calculate growth rates for 2024 and 2025
    ai_growth_2024 = ((ai_2024 - ai_adjustments[-1]) / ai_adjustments[-1]) * 100 if ai_adjustments[-1] > 0 else 0
    ai_growth_2025 = ((ai_2025 - ai_2024) / ai_2024) * 100 if ai_2024 > 0 else 0
    
    apps_growth_2024 = ((apps_2024 - apps_adjustments[-1]) / apps_adjustments[-1]) * 100 if apps_adjustments[-1] > 0 else 0
    apps_growth_2025 = ((apps_2025 - apps_2024) / apps_2024) * 100 if apps_2024 > 0 else 0
    
    # Combine historical and predicted data
    all_years = years_historical + [2024, 2025]
    all_ai_growth = ai_growth_rates_adj + [ai_growth_2024, ai_growth_2025]
    all_apps_growth = apps_growth_rates_adj + [apps_growth_2024, apps_growth_2025]
    
    # Growth Rate Chart
    st.subheader("Growth Rates Over Time")
    fig_growth_comparison = go.Figure()
    fig_growth_comparison.add_trace(go.Scatter(
        x=all_years,
        y=all_ai_growth,
        mode='lines+markers',
        name='AI Investments Growth Rate (%)',
        line=dict(color='blue', width=2)
    ))
    fig_growth_comparison.add_trace(go.Scatter(
        x=all_years,
        y=all_apps_growth,
        mode='lines+markers',
        name='US Business Apps Growth Rate (%)',
        line=dict(color='green', width=2)
    ))
    fig_growth_comparison.update_layout(
        xaxis_title="Year",
        yaxis_title="Growth Rate (%)",
        title="Growth Rates: AI Investments vs US New Business Apps",
        hovermode='x unified'
    )
    st.plotly_chart(fig_growth_comparison, use_container_width=True)
    
    # Gap Analysis
    st.subheader("Gap Analysis")
    gap_values = [ai - apps for ai, apps in zip(all_ai_growth, all_apps_growth)]
    
    fig_gap = go.Figure()
    fig_gap.add_trace(go.Bar(
        x=all_years,
        y=gap_values,
        name='Gap (AI Growth - Apps Growth)',
        marker_color='purple'
    ))
    fig_gap.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Zero Gap")
    fig_gap.update_layout(
        xaxis_title="Year",
        yaxis_title="Growth Rate Gap (%)",
        title="Gap Analysis: Difference in Growth Rates",
        hovermode='x unified'
    )
    st.plotly_chart(fig_gap, use_container_width=True)
    
    # Summary table
    st.subheader("Summary Table")
    df_summary = pd.DataFrame({
        'Year': all_years,
        'AI Investments ($B)': ai_adjustments + [ai_2024, ai_2025],
        'AI Growth Rate (%)': all_ai_growth,
        'US Business Apps (M)': apps_adjustments + [apps_2024, apps_2025],
        'Apps Growth Rate (%)': all_apps_growth,
        'Gap (%)': gap_values
    })
    
    df_summary['AI Investments ($B)'] = df_summary['AI Investments ($B)'].apply(lambda x: f"${x:.1f}")
    df_summary['US Business Apps (M)'] = df_summary['US Business Apps (M)'].apply(lambda x: f"{x:.1f}")
    df_summary['AI Growth Rate (%)'] = df_summary['AI Growth Rate (%)'].apply(lambda x: f"{x:.2f}%")
    df_summary['Apps Growth Rate (%)'] = df_summary['Apps Growth Rate (%)'].apply(lambda x: f"{x:.2f}%")
    df_summary['Gap (%)'] = df_summary['Gap (%)'].apply(lambda x: f"{x:.2f}%")
    
    st.dataframe(df_summary, use_container_width=True)
