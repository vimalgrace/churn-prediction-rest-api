import streamlit as st
import pandas as pd
import requests

BACKEND_URL = "http://backend:7860"

st.title("Telecom Customer Churn Prediction App")
st.write(
    "Enter the customer's details below to predict whether the customer is likely to churn."
)

SeniorCitizen = st.selectbox(
    "Is the customer a senior citizen?",
    [0, 1]
)

Partner = st.selectbox(
    "Does the customer have a partner?",
    ["Yes", "No"]
)

Dependents = st.selectbox(
    "Does the customer have dependents?",
    ["Yes", "No"]
)

PhoneService = st.selectbox(
    "Does the customer have phone service?",
    ["Yes", "No"]
)


InternetService = st.selectbox(
    "Type of Internet Service",
    ["DSL", "Fiber optic", "No"]
)

Contract = st.selectbox(
    "Type of Contract",
    ["Month-to-month", "One year", "Two year"]
)


PaymentMethod = st.selectbox(
    "Payment Method",
    ["Electronic check", "Mailed check", "Bank transfer", "Credit card"]
)


tenure = st.number_input(
    "Monthly Charges",
    min_value = 0.0,
    value = 50.0
)


MonthlyCharges = st.number_input(
    "Monthly Charges",
    min_value = 0.0,
    value = 50.0

)


TotalCharges = st.number_input(
    "Total Charges".
    min_value = 0.0,
    value = 600.0
)


customer_data = {
    "SeniorCitizen": SeniorCitizen,
    "tenure": tenure,
    "MonthlyCharges": MonthlyCharges,
    "TotalCharges": TotalCharges,
    "Partner": Partner,
    "Dependents": Dependents,
    "PhoneService": PhoneService,
    "InternetService": InternetService,
    "Contract": Contract,
    "PaymentMethod": PaymentMethod
}


if st.button("Predict", type = "primary"):

  response = request.post(
      f"{BACKEND_URL}/v1/customer"
  )

  if response.status_code == 200:
    result = response.json()

    if result["Prediction"] == "Churn":
      st.error("⚠️ The customer is likely to churn.")
    else:
      st.success("✅ The customer is unlikely to churn.")
  else:
    st.error("Unable to connect to the prediction API.")


st.subheader("Batch Prediction")

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type = ["csv"]
)


if uploaded_file is not None:
  if st.button("Predict for Batch", type = "primary"):

    reponse = request.post(
        f"{BACKEND_URL}/v1/customerbatch",
        files = {"file":uploaded_file}
    )

    if response.status_code == 200:
      results = response.json()

      st.success("Predictions completed successfully!")

      try:

        if isinstance(results, list):
          df = pd.DataFrame(results)

        elif isinstance(results, dict):
          if all(not isinstance(v, (list, dict)) for v in results.values()):
            df = pd.DataFrame([results])
          else:
            df = pd.DataFrame(results)

        else:
          df = pd.DataFrame({"Result": [results]})


        st.dataframe(df, use_container_width = True)


      except Exception as e:
        st.error(f"Unable to display results as a table: {e}")
        st.json(results)


    else:
      st.error("Unable to connect to the prediction API")

