-- 1. Total customers, churned customers, and overall churn rate
SELECT 
    COUNT(customerID) AS TotalCustomers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) / COUNT(customerID) * 100, 2) AS ChurnRatePercentage
FROM customers;

-- 2. Churn rate by contract type
SELECT 
    Contract,
    COUNT(customerID) AS TotalCustomers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) / COUNT(customerID) * 100, 2) AS ChurnRatePercentage
FROM customers
GROUP BY Contract
ORDER BY ChurnRatePercentage DESC;

-- 3. Churn by tenure group
SELECT 
    TenureGroup,
    COUNT(customerID) AS TotalCustomers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) / COUNT(customerID) * 100, 2) AS ChurnRatePercentage
FROM customers
GROUP BY TenureGroup
ORDER BY 
    CAST(SUBSTR(TenureGroup, 1, INSTR(TenureGroup, '-') - 1) AS INTEGER);

-- 4. Churn by payment method
SELECT 
    PaymentMethod,
    COUNT(customerID) AS TotalCustomers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) / COUNT(customerID) * 100, 2) AS ChurnRatePercentage
FROM customers
GROUP BY PaymentMethod
ORDER BY ChurnRatePercentage DESC;

-- 5. Churn by internet service type
SELECT 
    InternetService,
    COUNT(customerID) AS TotalCustomers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) / COUNT(customerID) * 100, 2) AS ChurnRatePercentage
FROM customers
GROUP BY InternetService
ORDER BY ChurnRatePercentage DESC;

-- 6. Average monthly and total charges by churn status
SELECT 
    Churn,
    COUNT(customerID) AS TotalCustomers,
    ROUND(AVG(MonthlyCharges), 2) AS AvgMonthlyCharges,
    ROUND(AVG(TotalCharges), 2) AS AvgTotalCharges
FROM customers
GROUP BY Churn;

-- 7. Customer segmentation by risk-related characteristics (High Risk Segment)
-- Identifying customers with Month-to-month contract and Electronic Check (historically high risk)
WITH SegmentedData AS (
    SELECT 
        customerID,
        Contract,
        PaymentMethod,
        TenureGroup,
        Churn,
        CASE 
            WHEN Contract = 'Month-to-month' AND PaymentMethod = 'Electronic check' THEN 'High Risk (M2M & Elec Check)'
            WHEN Contract = 'Two year' THEN 'Low Risk (2 Year)'
            ELSE 'Medium Risk (Other)'
        END AS RiskSegment
    FROM customers
)
SELECT 
    RiskSegment,
    COUNT(customerID) AS TotalCustomers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) / COUNT(customerID) * 100, 2) AS ChurnRatePercentage
FROM SegmentedData
GROUP BY RiskSegment
ORDER BY ChurnRatePercentage DESC;
