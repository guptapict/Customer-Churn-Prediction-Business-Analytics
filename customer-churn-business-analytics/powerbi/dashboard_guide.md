# Power BI Dashboard Implementation Guide

Follow these steps to build the interactive Power BI dashboard for your Customer Churn & Business Analytics project.

## Step 1: Data Import & Modeling
1. Open **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV**.
3. Import `data/processed/cleaned_churn_data.csv`.
4. Click **Get Data** > **Text/CSV** again and import `data/predictions/customer_risk_scores.csv`.
5. Go to the **Model View** (the relationship icon on the left panel).
6. Power BI should automatically detect a 1-to-1 relationship between the two tables based on `customerID`. If it doesn't, drag `customerID` from one table to the other to link them.
7. Open the `powerbi/dax_measures.md` file and create all the calculated measures listed there.

---

## Step 2: Build Page 1 - Executive Overview
**Goal:** A high-level view of current churn performance for senior management.

1. **Title:** Add a text box at the top: "Executive Churn Overview".
2. **KPI Cards (Top Row):**
   - Add a Card visual. Drop in the `[Total Customers]` DAX measure.
   - Add a Card visual. Drop in the `[Total Churned]` DAX measure.
   - Add a Card visual. Drop in the `[Churn Rate]` DAX measure.
   - Add a Card visual. Drop in the `[Avg Monthly Charges]` DAX measure.
3. **Donut Chart (Churn by Contract):**
   - Values: `[Total Customers]`
   - Legend: `Contract` (from cleaned data)
   - *Insight: Quickly shows how many customers are trapped in high-risk month-to-month plans.*
4. **Line Chart (Monthly Charges by Tenure):**
   - X-Axis: `tenure`
   - Y-Axis: `[Avg Monthly Charges]`
   - Legend: `Churn`
   - *Insight: Shows if churners consistently pay more over their lifecycle.*

---

## Step 3: Build Page 2 - Customer Churn Analysis
**Goal:** Deep dive into historical drivers of churn for product/marketing teams.

1. **Slicers (Filters) on the left panel:**
   - Add a Slicer for `gender`.
   - Add a Slicer for `SeniorCitizen`.
   - Add a Slicer for `Partner`.
2. **Clustered Bar Chart (Churn by Tenure Group):**
   - X-Axis: `TenureGroup`
   - Y-Axis: `[Total Customers]`
   - Legend: `Churn`
   - *Note: Sort the X-axis chronologically (0-12, 13-24, etc.).*
3. **Clustered Column Chart (Churn by Payment Method):**
   - X-Axis: `PaymentMethod`
   - Y-Axis: `[Churn Rate]` measure
   - *Insight: Highlights the risk of Electronic Checks.*
4. **Matrix (Service Breakdown):**
   - Rows: `InternetService`, `OnlineSecurity`, `TechSupport`
   - Values: `[Total Customers]`, `[Churn Rate]`
   - *Insight: Lets analysts drill down to see if lack of Tech Support drives churn.*

---

## Step 4: Build Page 3 - Churn Risk & Retention (Machine Learning Output)
**Goal:** Actionable list for the Retention Team to reach out to high-risk customers.

1. **Disclaimer Text Box:** Add text at the top: *"Warning: This page contains predictive model outputs. Risk Categories are probabilities, not certainties."*
2. **KPI Card:**
   - Drop in the `[High Risk Customers]` DAX measure. 
   - Label it "Customers Requiring Immediate Action".
3. **Donut Chart (Risk Distribution):**
   - Legend: `RiskCategory` (from risk_scores table)
   - Values: `customerID` (Count)
4. **Histogram/Column Chart (Churn Probability Distribution):**
   - X-Axis: `ChurnProbability` (bin it by 0.1 intervals if necessary)
   - Y-Axis: Count of `customerID`
5. **Actionable Table / Data Grid:**
   - Add a Table visual.
   - Columns to include: `customerID`, `RiskCategory`, `ChurnProbability`, `Contract`, `MonthlyCharges`, `TenureGroup`.
   - *Filter this visual* using the filter pane to only show `RiskCategory` = "High Risk".
   - *Action:* The retention team can export this specific table to Excel to start their calling campaign.

## Step 5: Formatting & Polish
1. **Theme:** Go to *View > Themes* and pick a professional theme (e.g., Executive or City Park).
2. **Colors:** Ensure "Churn = Yes" is consistently colored (e.g., Red/Orange) across all charts, and "Churn = No" is a calming color (e.g., Blue/Grey).
3. **Navigation:** Add button visuals to navigate between the 3 pages for an app-like experience.
