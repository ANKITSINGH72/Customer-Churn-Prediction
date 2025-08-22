import streamlit as st
import numpy as np

# Define feature categories
categories = {
    "Gender": ["gender_Female", "gender_Male"],
    "Partner": ["Partner_No", "Partner_Yes"],
    "Dependents": ["Dependents_No", "Dependents_Yes"],
    "Phone Service": ["PhoneService_No", "PhoneService_Yes"],
    "Multiple Lines": ["MultipleLines_No", "MultipleLines_No phone service", "MultipleLines_Yes"],
    "Internet Service": ["InternetService_DSL", "InternetService_Fiber optic", "InternetService_No"],
    "Online Security": ["OnlineSecurity_No", "OnlineSecurity_No internet service", "OnlineSecurity_Yes"],
    "Online Backup": ["OnlineBackup_No", "OnlineBackup_No internet service", "OnlineBackup_Yes"],
    "Device Protection": ["DeviceProtection_No", "DeviceProtection_No internet service", "DeviceProtection_Yes"],
    "Tech Support": ["TechSupport_No", "TechSupport_No internet service", "TechSupport_Yes"],
    "Streaming TV": ["StreamingTV_No", "StreamingTV_No internet service", "StreamingTV_Yes"],
    "Streaming Movies": ["StreamingMovies_No", "StreamingMovies_No internet service", "StreamingMovies_Yes"],
    "Contract": ["Contract_Month-to-month", "Contract_One year", "Contract_Two year"],
    "Paperless Billing": ["PaperlessBilling_No", "PaperlessBilling_Yes"],
    "Payment Method": [
        "PaymentMethod_Bank transfer (automatic)",
        "PaymentMethod_Credit card (automatic)",
        "PaymentMethod_Electronic check",
        "PaymentMethod_Mailed check"
    ],
    "Tenure Group": [
        "tenure_group_1 - 12", "tenure_group_13 - 24", "tenure_group_25 - 36",
        "tenure_group_37 - 48", "tenure_group_49 - 60", "tenure_group_61 - 72"
    ]
}

# Additional numerical columns
numerical_columns = ["SeniorCitizen", "MonthlyCharges", "TotalCharges"]

# UI for user selections
st.title("Customer Feature Selection")

# Dictionary to hold user selections
user_selection = {}

for category, options in categories.items():
    selected_option = st.selectbox(f"Select {category}:", options)
    user_selection[category] = selected_option

# Numeric inputs
numeric_values = {}
for col in numerical_columns:
    numeric_values[col] = st.number_input(f"Enter {col}:", min_value=0.0)

# Generate feature array
feature_array = []

# Append numeric values in order
for col in numerical_columns:
    feature_array.append(numeric_values[col])

# Append categorical values in order
for category, options in categories.items():
    selected = user_selection[category]
    for option in options:
        feature_array.append(1 if option == selected else 0)

# Display the final feature array
st.write("Final Feature Array:")
st.write(np.array(feature_array))
