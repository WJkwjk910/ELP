# Quick Start Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Run the Application

```bash
streamlit run app.py
```

## Step 3: Access the Application

- The app will automatically open in your browser at `http://localhost:8501`
- If it doesn't open automatically, navigate to that URL manually

## Step 4: Create Your Account

1. Click on the "Register" tab
2. Enter your email address
3. Enter a password
4. Click "Register"
5. Switch to the "Login" tab and login with your credentials

## Step 5: Use the Revenue Growth Predictor

1. **Set Initial Parameters** (in the left sidebar):
   - Adjust Initial Revenue, Capital, Expense, and Growth Rate as needed

2. **Adjust Business Variables**:
   - Use the sliders to set weights for:
     - Competition
     - New Entrant
     - Supplier's Bargaining Power
     - Buyer's Bargaining Power
     - Substitute
     - Product-Market Fit
     - Differentiator

3. **Apply Leadership Learning**:
   - Adjust Adaptive Learning and Deep Learning sliders
   - These automatically affect your business variables

4. **View Results**:
   - Growth Rate Chart: See how growth rates change over 5 years
   - Revenue Chart: See projected revenue over 5 years
   - Radar Chart: Visualize all variable weights
   - Cash Flow Table: Detailed financial projections

5. **Sensitivity Analysis**:
   - Use the sensitivity slider to see best case (120%), baseline (100%), and worst case (80%) scenarios

## Step 6: Analyze AI Investments

1. Switch to the "AI Investments Analysis" tab
2. View historical data from 2015-2023
3. Adjust historical values using sliders if needed
4. See predictions for 2024 and 2025
5. Analyze the gap between AI Investments and US New Business Apps

## Admin Features

If you're an admin user:
1. Click the "Admin Console" expander in the sidebar
2. View all registered users
3. Delete users if needed
4. Add new users with email and password
5. Set admin privileges for new users

## Troubleshooting

### Port Already in Use
If port 8501 is already in use:
```bash
streamlit run app.py --server.port 8502
```

### Database Issues
If you encounter database errors, delete `users.db` and restart the app (this will reset all user accounts).

### Missing Dependencies
Make sure all packages are installed:
```bash
pip install --upgrade -r requirements.txt
```

## Next Steps

- Explore different scenarios by adjusting variable weights
- Compare sensitivity analysis results
- Analyze trends in AI Investments vs US New Business Apps
- Export data for further analysis (coming soon)
