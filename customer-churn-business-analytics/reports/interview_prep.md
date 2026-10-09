# Resume & Interview Preparation

## 1. Resume Bullet Points (ATS-Friendly)
* Designed and executed an end-to-end Customer Churn Prediction system in Python, applying Scikit-Learn (Random Forest, Logistic Regression) to classify at-risk customers, achieving an 84% ROC-AUC and successfully identifying 80% of true churners.
* Engineered automated data processing pipelines using Pandas and SQL to handle missing values, correct data types, and generate dynamic segmentations (e.g., tenure grouping) across 7,000+ records.
* Developed an interactive Power BI dashboard utilizing DAX measures to visualize churn trends by contract type and payment methods, delivering actionable, prioritized retention lists for stakeholders.

## 2. The 60-Second Elevator Pitch
"For my capstone project, I built an end-to-end Machine Learning pipeline to predict customer churn for a telecom company. I started by using SQL and Pandas to clean the historical data and uncover insights—for instance, I found that month-to-month contracts and manual payment methods drove the highest churn. Since finding a churning customer was the priority, I optimized my models for Recall and ROC-AUC rather than just accuracy. My best model, a Random Forest, successfully caught 80% of true churners. Finally, I output those predictive risk scores into a Power BI dashboard so the retention team could actually use the data to target high-revenue, high-risk customers."

## 3. The 3-Minute Project Walkthrough
**The Problem:** "I wanted to move beyond just running a model in a notebook, so I framed this around a real business problem: Retaining customers is cheaper than acquiring new ones. The goal was to find out *who* is leaving and *why*."
**The Data & SQL:** "I used the IBM Telco dataset. After cleaning missing values in Python, I loaded it into SQLite. I wrote queries using CTEs and CASE statements to segment the users. The SQL analysis revealed that early-tenure customers on month-to-month plans paying by electronic check were incredibly high risk."
**The ML Model:** "When predicting churn, the classes are usually imbalanced—here, only 26% of people churned. I knew accuracy would be a misleading metric. I trained Logistic Regression, Random Forest, and XGBoost, utilizing class weights to handle the imbalance. I selected Random Forest because it had the highest ROC-AUC (0.84) and a strong Recall (80%), meaning it successfully flagged the vast majority of actual churners."
**The Business Value:** "But a model alone isn't a product. I took the probability scores from the Random Forest, categorized customers into High, Medium, and Low risk, and exported that data. I then built a Power BI dashboard. The final page of that dashboard filters specifically for 'High Risk' customers, allowing a business retention team to export a targeted call list prioritized by monthly revenue."

## 4. Likely Interview Questions & Answers

**Q: Why didn't you use Accuracy to evaluate your model?**
**A:** "Because the dataset was imbalanced (73% No Churn, 26% Churn). A naive model that just predicts 'No Churn' every time would be 73% accurate but completely useless for the business. I focused on ROC-AUC for overall class separation and Recall because missing a churning customer (False Negative) is more expensive than mistakenly offering a retention discount to a loyal customer (False Positive)."

**Q: How did you handle the class imbalance?**
**A:** "I used the `class_weight='balanced'` parameter in Scikit-Learn for Random Forest and Logistic Regression, and `scale_pos_weight` for XGBoost. This penalizes the model more for misclassifying the minority class. I also used a stratified train/test split to ensure both sets maintained the 73/26 ratio."

**Q: Did you check for data leakage?**
**A:** "Yes. I split my data into train and test sets *before* applying any transformations. I used a Scikit-Learn `ColumnTransformer` and `Pipeline` to fit the `StandardScaler` and `OneHotEncoder` strictly on the training data, and then applied them to the test data. This ensures the model has no knowledge of the test set distribution."

**Q: You mentioned month-to-month contracts cause churn. Should the business force everyone into 1-year contracts?**
**A:** "Not necessarily. The model proves correlation, not causation. Customers might choose month-to-month *because* they intend to leave soon, or they might be unhappy with the service. Forcing a contract might just reduce initial sales. Instead, I recommended incentivizing the transition with a discount or free add-on."

**Q: How would you improve this model if you had more time?**
**A:** "I would implement a financial cost-benefit matrix. Right now, I optimize for Recall, accepting False Positives. But if the retention strategy is very expensive (e.g., a $100 credit), False Positives become costly. I would want to adjust the prediction threshold to maximize expected profit, not just catch the maximum number of churners."

**Q: Tell me about a data cleaning challenge you faced.**
**A:** "The `TotalCharges` column loaded as an object instead of a float. Upon investigation, I found blank strings (`' '`) for customers who had a tenure of 0 months. Instead of dropping them, I realized they were simply new customers who hadn't been billed yet, so I coerced the blanks to NaN and filled them with 0."
