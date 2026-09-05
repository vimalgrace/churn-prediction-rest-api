import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app with a name
app = Flask("Telecom Customer Churn Predictor")

# Load the trained churn prediction model
model = joblib.load("churn_prediction_model_v1_0.joblib")

# Define a route for the home page
@app.get('/')
def home():
    return "Welcome to the Telecom Customer Churn Prediction API"

# Define an endpoint to predict churn for a single customer
@app.post('/v1/customer')
def predict_churn():
    # Get JSON data from the request
    customer_data = request.get_json()

    # Extract relevant customer features from the input data
    sample = {
        'SeniorCitizen': customer_data['SeniorCitizen'],
        'Partner': customer_data['Partner'],
        'Dependents': customer_data['Dependents'],
        'tenure': customer_data['tenure'],
        'PhoneService': customer_data['PhoneService'],
        'InternetService': customer_data['InternetService'],
        'Contract': customer_data['Contract'],
        'PaymentMethod': customer_data['PaymentMethod'],
        'MonthlyCharges': customer_data['MonthlyCharges'],
        'TotalCharges': customer_data['TotalCharges']
    }

    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # Make a churn prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # Map prediction result to a human-readable label
    prediction_label = "churn" if prediction == 1 else "not churn"

    # Return the prediction as a JSON response
    return jsonify({'Prediction': prediction_label})

# Define an endpoint to predict churn for a batch of customers
@app.post('/v1/customerbatch')
def predict_churn_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for the batch data and convert raw predictions into a readable format
    predictions = [
        'Churn' if x == 1
        else "Not Churn"
        for x in model.predict(input_data.drop("customerID",axis=1)).tolist()
    ]

    cust_id_list = input_data.customerID.values.tolist()
    output_dict = dict(zip(cust_id_list, predictions))

    return output_dict

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)