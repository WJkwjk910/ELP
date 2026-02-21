# Entrepreneurial Learning Predictor

A comprehensive Streamlit web application for predicting company revenue growth rates and analyzing AI investment trends.

## Features

### 1. Revenue Growth Rate Predictor
- **5-Year Revenue Growth Simulation**: Predict revenue growth rates based on multiple business factors
- **Interactive Variable Sliders**: Adjust weights (0.0 to 1.0) for:
  - Competition
  - New Entrants
  - Supplier's Bargaining Power
  - Buyer's Bargaining Power
  - Substitutes
  - Product-Market Fit
  - Differentiator
- **Leadership Learning Sliders**:
  - Adaptive Learning (affects differentiator)
  - Deep Learning (affects differentiator and substitutes)
- **Process Management Slider** (affects buyer's bargaining power)
- **Visualizations**:
  - Linear chart: Growth Rate (%) vs Year (1-5)
  - Linear chart: Revenue ($) vs Year (1-5)
  - Radar chart: Variable weights analysis
- **Sensitivity Analysis**: Analyze best case (120%), baseline (100%), and worst case (80%) scenarios
- **5-Year Cash Flow Table**: Track Capital, Revenue, Expense, Net Profit, and Cumulative Cash

### 2. AI Investments vs US New Business Apps Analysis
- **Historical Data Analysis**: View growth rates from 2015-2023
- **Future Predictions**: Predict growth rates for 2024 and 2025
- **Interactive Sliders**: Adjust historical data points for both AI Investments and US New Business Apps
- **Gap Analysis**: Visualize the difference in growth rates between AI Investments and US New Business Apps
- **Growth Rate Charts**: Compare trends over time

### 3. Multi-Tenant Architecture
- **User Authentication**: Create accounts using email addresses
- **User Management**: Admin console to add/delete users
- **Independent Sessions**: Each user can use the service independently

## Installation

1. **Clone or navigate to the project directory**:
```bash
cd /Users/juny910/Desktop/Entrepreneurial-Learning-Predictor
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Running the Application

1. **Start the Streamlit app**:
```bash
streamlit run app.py
```

2. **Access the application**:
   - The app will open in your default web browser
   - If not, navigate to `http://localhost:8501`

3. **First-time Setup**:
   - Register a new account with your email address
   - Login with your credentials
   - The first user can be made an admin by modifying the database or code

## Usage Instructions

### Revenue Growth Predictor

1. **Set Initial Parameters** (in sidebar):
   - Initial Revenue ($): Default $1,000,000
   - Initial Capital ($): Default $500,000
   - Initial Expense ($): Default $1,000,000
   - Initial Growth Rate (%): Default 20%, adjustable 0-99%

2. **Adjust Variable Weights**:
   - Use sliders to set weights (0.0 to 1.0) for each business factor
   - Initial values are set according to specifications

3. **Apply Leadership Learning**:
   - Adjust Adaptive Learning and Deep Learning sliders
   - These automatically affect differentiator and substitute values

4. **View Results**:
   - Growth rate chart shows predicted growth rates over 5 years
   - Revenue chart shows projected revenue over 5 years
   - Radar chart visualizes all variable weights
   - Cash flow table shows detailed financial projections

5. **Sensitivity Analysis**:
   - Use the sensitivity variance slider (80-120%)
   - View best case, baseline, and worst case scenarios

### AI Investments Analysis

1. **View Historical Data**:
   - Default values from 2015-2023 are pre-loaded
   - AI Investments: $24B to $252B
   - US New Business Apps: 2.8M to 5.4M

2. **Adjust Historical Values**:
   - Use sliders to modify any historical data point
   - Growth rates will automatically recalculate

3. **View Predictions**:
   - See predicted values for 2024 and 2025
   - Based on average growth rate from recent years

4. **Gap Analysis**:
   - Visualize the difference in growth rates
   - Identify trends and patterns

### Admin Console

1. **Access Admin Features**:
   - Login as an admin user
   - Click the "Admin Console" expander in the sidebar

2. **User Management**:
   - View all registered users
   - Delete users by clicking the "Delete" button
   - Add new users with email and password
   - Set admin privileges for new users

## Calculation Logic

### Growth Rate Impacts:
- Competition: -1% per 0.1 increase
- Buyer's Bargaining Power: -1% per 0.1 increase
- New Entrant: -1% per 0.1 increase
- Supplier's Bargaining Power: +1% per 0.1 increase
- Substitute: -10% per 0.1 increase
- Product-Market Fit: +0.5% per 0.1 increase
- Differentiator: +0.5% per 0.1 increase

### Variable Relationships:
- Competition increases by at least 0.05 annually
- Competition increases by 0.05 if new entrant increases by 0.1
- Competition decreases by 0.05 if supplier power increases by 0.1
- Competition increases by 0.05 if buyer power increases by 0.1
- Competition decreases by 0.05 if differentiator increases by 0.1
- Supplier power increases by 0.05 if differentiator increases by 0.1
- Buyer power increases by 0.05 if differentiator decreases by 0.1

### Leadership Learning:
- Adaptive Learning: +0.1 differentiator per 0.1 adaptive learning
- Deep Learning: +0.2 differentiator and -0.1 substitute per 0.1 deep learning
- Process Management: +0.1 buyer power per 0.1 process

## File Structure

```
Entrepreneurial-Learning-Predictor/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── users.db              # SQLite database (created automatically)
```

## Dependencies

- streamlit==1.28.0
- pandas==2.1.1
- numpy==1.24.3
- plotly==5.17.0
- sqlalchemy==2.0.23
- bcrypt==4.0.1
- python-dotenv==1.0.0
- streamlit-authenticator==0.2.3

## Notes

- The application uses SQLite for user management (local database)
- All user data is stored locally in `users.db`
- For production deployment on Azure, consider using Azure SQL Database or Cosmos DB
- Passwords are hashed using SHA256 (consider upgrading to bcrypt for production)

## Future Enhancements

- Azure cloud deployment configuration
- Enhanced security with bcrypt password hashing
- Data persistence for user-specific scenarios
- Export functionality for reports and charts
- Advanced analytics and machine learning predictions

## Support

For issues or questions, please refer to the code comments or contact the development team.
