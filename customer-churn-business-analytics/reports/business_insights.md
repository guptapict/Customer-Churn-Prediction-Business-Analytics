# Strategic Business Recommendations

Based on the end-to-end analysis of the IBM Telco dataset and the predictions of the Random Forest model, here is the executive business report.

## 1. Key Findings & High-Risk Segments
Historical data clearly shows that churn is not random. It is heavily concentrated in specific customer segments:
* **The "First 90 Days" Gap:** Customers in their first year (especially months 0-5) have a churn rate near 47%. The onboarding process is currently a critical failure point.
* **The Flexibility Tax:** Customers on Month-to-Month contracts churn at 42.7%, compared to less than 3% for those on 2-year contracts. 
* **The Friction of Payment:** Customers paying via "Electronic Check" (a manual process) have a vastly disproportionate churn rate compared to those on automatic billing.
* **Price Sensitivity:** Higher monthly charges loosely correlate with higher churn. Customers feel the pain of the price if the perceived value is low.

## 2. Suggested Retention Strategies
**Strategy A: The Autopay Incentive**
* **Action:** Offer a small, permanent discount (e.g., $2-5/month) or a one-time bill credit for customers who switch from Electronic Check to Automatic Credit Card/Bank Transfer billing.
* **Why:** Removing the monthly decision to pay reduces the cognitive friction that leads to cancellations.

**Strategy B: The "Bridge to Annual" Program**
* **Action:** Target Month-to-Month customers approaching their 6th month. Offer them a free premium add-on (like Tech Support or Online Security) if they commit to a 1-year contract.
* **Why:** Moving them off month-to-month drastically drops their historical churn probability.

**Strategy C: White-Glove Onboarding**
* **Action:** Implement a 30-day and 60-day check-in call for all new customers. Ensure their services are working perfectly and they understand their bill.

## 3. How to Prioritize Customers (Using ML Output)
The Machine Learning model exported a file (`customer_risk_scores.csv`) categorizing every active customer as High, Medium, or Low risk.
* **Prioritization:** The retention team should filter the Power BI dashboard for **"High Risk"** customers. Sort this list by **MonthlyCharges** (descending). 
* **Why:** This ensures the team spends their limited time calling the customers who are most likely to leave AND who generate the most revenue.

## 4. Measuring Success (A/B Testing)
Do not deploy retention strategies to everyone at once. 
* Take the top 1,000 High-Risk customers.
* Randomly assign 500 to the "Treatment Group" (they get the retention call/discount).
* Assign the other 500 to the "Control Group" (business as usual).
* After 30 days, compare the actual churn rates between the two groups to prove the financial ROI of the retention team.

## 5. Risks & Limitations
* **Causation vs. Correlation:** The ML model knows that month-to-month contracts are *associated* with churn. Forcing an unhappy customer into a 1-year contract might just make them angry and cause negative brand perception. We must solve the underlying dissatisfaction.
* **Cost of False Positives:** The model has a precision of ~51%. This means half the people the model flags as "High Risk" were not actually going to churn. Therefore, retention interventions must be relatively cheap (like a phone call or a $10 credit). We cannot afford to give away $100 discounts to people who were never going to leave anyway.
