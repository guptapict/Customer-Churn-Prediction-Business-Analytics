# Power BI DAX Measures

Once you have imported `cleaned_churn_data.csv` and `customer_risk_scores.csv` into Power BI Desktop, you need to create these DAX measures. These measures are dynamic and will recalculate based on the slicers and filters you click on the dashboard.

## 1. Core Base Measures
Create these on the `cleaned_churn_data` table.

**Total Customers**
```dax
Total Customers = COUNTROWS(cleaned_churn_data)
```

**Total Churned Customers**
```dax
Total Churned = 
CALCULATE(
    COUNTROWS(cleaned_churn_data),
    cleaned_churn_data[Churn] = "Yes"
)
```

**Churn Rate %**
```dax
Churn Rate = 
DIVIDE(
    [Total Churned],
    [Total Customers],
    0
)
```
*Note: Format this measure as a Percentage (%) in the Ribbon.*

## 2. Revenue & Financial Measures
Create these on the `cleaned_churn_data` table.

**Average Monthly Charges**
```dax
Avg Monthly Charges = AVERAGE(cleaned_churn_data[MonthlyCharges])
```
*Note: Format this as Currency ($).*

**Total Monthly Revenue Lost (MRR Lost to Churn)**
```dax
Monthly Revenue Lost = 
CALCULATE(
    SUM(cleaned_churn_data[MonthlyCharges]),
    cleaned_churn_data[Churn] = "Yes"
)
```
*Note: Format this as Currency ($).*

## 3. Predictive / Risk Measures
Create these on the `customer_risk_scores` table.

**Total High-Risk Customers**
```dax
High Risk Customers = 
CALCULATE(
    COUNTROWS(customer_risk_scores),
    customer_risk_scores[RiskCategory] = "High Risk"
)
```

**Predicted vs Actual Churn Discrepancy**
(Useful for validation views)
```dax
Is False Negative = 
IF(
    customer_risk_scores[ActualChurn] = "Yes" && customer_risk_scores[PredictedChurnClass] = "No", 
    1, 
    0
)
```
