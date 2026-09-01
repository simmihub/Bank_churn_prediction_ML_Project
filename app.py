import streamlit as st
import pandas as pd
import joblib

# Load trained model/pipeline
model = joblib.load("churn_model.pkl")

# Page configuration
st.set_page_config(
    page_title="Bank Churn Prediction",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 Bank Customer Churn Prediction")
st.write("Predict customer churn and get a retention recommendation.")

st.divider()

# Customer details
st.subheader("Customer Information")

col1, col2 = st.columns(2)

with col1:
    credit_score = st.number_input(
        "Credit Score",
        min_value=300,
        max_value=900,
        value=650
    )

    geography = st.selectbox(
        "Geography",
        ["France", "Germany", "Spain"]
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=35
    )

    tenure = st.number_input(
        "Tenure",
        min_value=0,
        max_value=10,
        value=5
    )

with col2:
    balance = st.number_input(
        "Balance",
        min_value=0.0,
        value=50000.0
    )

    num_products = st.number_input(
        "Number of Products",
        min_value=1,
        max_value=4,
        value=1
    )

    has_card = st.selectbox(
        "Has Credit Card",
        [0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

    active_member = st.selectbox(
        "Is Active Member",
        [0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

    salary = st.number_input(
        "Estimated Salary",
        min_value=0.0,
        value=50000.0
    )

# Prediction
if st.button("Predict Churn", type="primary"):

    input_data = pd.DataFrame({
        "CreditScore": [credit_score],
        "Geography": [geography],
        "Gender": [gender],
        "Age": [age],
        "Tenure": [tenure],
        "Balance": [balance],
        "NumOfProducts": [num_products],
        "HasCrCard": [has_card],
        "IsActiveMember": [active_member],
        "EstimatedSalary": [salary]
    })

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    st.divider()

    st.subheader("Prediction Result")

    st.metric(
        "Churn Probability",
        f"{probability * 100:.2f}%"
    )

    # Risk level
    if probability >= 0.70:
        risk = "High Risk"
        recommendation = (
            "Customer has a high risk of churn. "
            "Consider a personalized retention offer, "
            "customer engagement call, or loyalty benefit."
        )

    elif probability >= 0.40:
        risk = "Medium Risk"
        recommendation = (
            "Customer has a moderate risk of churn. "
            "Consider targeted engagement and personalized offers."
        )

    else:
        risk = "Low Risk"
        recommendation = (
            "Customer has a low risk of churn. "
            "Continue regular engagement and customer service."
        )

    if prediction == 1:
        st.error("⚠️ Customer is likely to churn")
    else:
        st.success("✅ Customer is likely to stay")

    st.write(f"### Risk Level: {risk}")

    st.info(
        f"**Retention Recommendation:** {recommendation}"
    )