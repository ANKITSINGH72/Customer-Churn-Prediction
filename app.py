import streamlit as st
import numpy as np
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Random Forest Classifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from imblearn.combine import SMOTEENN

# Load the trained model
model = pickle.load(open("final_model.sav", "rb"))
df=pd.read_csv('raw_data.csv')

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

# Function to predict churn
def predict_churn(feature_array):
    """Makes a churn prediction based on the user inputs."""
    feature_array = np.array(feature_array).reshape(1, -1)
    prediction = model.predict(feature_array)[0]
    probability = model.predict_proba(feature_array)[:, 1][0]
    return prediction, probability

# Sidebar for navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.selectbox("Go to:", ["Churn Prediction", "Churn Analysis"])

# Churn Prediction Page
if selected_page == "Churn Prediction":
    st.markdown("<h1 style='color: #FF5733; text-align: center;'>Customer Churn Prediction</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #4682B4; text-align: center;'>Enter Customer Details Below:</h3>", unsafe_allow_html=True)

    feature_array = []

    # Numeric inputs
    st.markdown("<h3 style='color: #32CD32;'>📊 Numeric Features</h3>", unsafe_allow_html=True)
    numeric_values = {}
    for col in numerical_columns:
        numeric_values[col] = st.number_input(f"{col}:", min_value=0.0)
        feature_array.append(numeric_values[col])

    # Categorical inputs
    st.markdown("<h3 style='color: #DAA520;'>📂 Categorical Features</h3>", unsafe_allow_html=True)
    user_selection = {}
    for category, options in categories.items():
        st.markdown(f"<h4 style='color: #1E90FF;'>{category}</h4>", unsafe_allow_html=True)
        selected_option = st.selectbox(f"{category}:", options)
        user_selection[category] = selected_option

    # Encode categorical features
    for category, options in categories.items():
        selected = user_selection[category]
        for option in options:
            feature_array.append(1 if option == selected else 0)

    # Prediction button
    if st.button("🔮 Predict Churn"):
        result, prob = predict_churn(feature_array)

        # Display result
        if result == 1:
            st.error(f"🚨 This customer is likely to churn! Confidence: {prob*100:.2f}%")
        else:
            st.success(f"✅ This customer is likely to continue! Confidence: {prob*100:.2f}%")

# Churn Analysis Page
elif selected_page == "Churn Analysis":
    st.markdown("<h1 style='color: #FF4500; text-align: center;'>Churn Analysis Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #4682B4; text-align: center;'>Select a Figure Below to View</h3>", unsafe_allow_html=True)

    # Create a list of image filenames
    image_list = [
        "images/count-dependents.png",
        "images/count-seniorcitizen.png",
        "images/count-fiberoptic.png",
        "images/count-gender.png",
        "images/count-multiplelines.png",
        "images/count-onlinesecurity.png",
        "images/count-onlineservice.png",
        "images/count-partner.png",
        "images/count-techsupport.png",
       
    ]

    # Create dropdown options matching the image list
    figure_options = {
        "count-dependents": image_list[0],
        "count-SeniorCitizen": image_list[1],
        "count-fiberoptic": image_list[2],
        "count-gender": image_list[3],
        "count-multiplelines": image_list[4],
        "count-onlinesecurity": image_list[5],
        "count-onlineservice": image_list[6],
        "count-partner": image_list[7],
        "count-techsupport": image_list[8],
        
    }

    # Center the dropdown
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_figure = st.selectbox("Select a figure to display:", list(figure_options.keys()))

    # Display image
    image_path = figure_options[selected_figure]
    st.image(image_path, caption=selected_figure, use_container_width=True)



