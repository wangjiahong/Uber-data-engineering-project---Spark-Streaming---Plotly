import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Simulate some data
np.random.seed(0)
n_samples = 1000
data = {
    'gender': np.random.choice(['Male', 'Female'], n_samples),
    'SeniorCitizen': np.random.choice([0, 1], n_samples),
    'Partner': np.random.choice(['Yes', 'No'], n_samples),
    'Dependents': np.random.choice(['Yes', 'No'], n_samples),
    'tenure': np.random.randint(1, 72, n_samples),
    'PhoneService': np.random.choice(['Yes', 'No'], n_samples),
    'MultipleLines': np.random.choice(['No', 'Yes', 'No phone service'], n_samples),
    'InternetService': np.random.choice(['DSL', 'Fiber optic', 'No'], n_samples),
    'OnlineSecurity': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
    'OnlineBackup': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
    'DeviceProtection': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
    'TechSupport': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
    'StreamingTV': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
    'StreamingMovies': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
    'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples),
    'PaperlessBilling': np.random.choice(['Yes', 'No'], n_samples),
    'PaymentMethod': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], n_samples),
    'MonthlyCharges': np.random.uniform(18.25, 118.75, n_samples),
    'TotalCharges': np.random.uniform(18.8, 8684.8, n_samples),
    'Churn': np.random.choice(['Yes', 'No'], n_samples)
}
df = pd.DataFrame(data)

# Step 1: Data Preparation
# Encode categorical variables
for column in df.columns:
    if df[column].dtype == 'object':
        encoder = LabelEncoder()
        df[column] = encoder.fit_transform(df[column])

X = df.drop('Churn', axis=1)
y = df['Churn']

# Step 2: Splitting data into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Model Training
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# Step 4: Model Evaluation
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:,1]
print("Accuracy:", accuracy_score(y_test, y_pred))
print("ROC AUC Score:", roc_auc_score(y_test, y_proba))
print(classification_report(y_test, y_pred))

# Step 5: Visualization - ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_proba)
plt.plot(fpr, tpr, label='XGBoost')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d')
plt.title('Confusion Matrix')
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()

# Step 6: Feature Importance
xgb.plot_importance(model)
plt.title('Feature Importance')
plt.show()
