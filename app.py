# app.py

import pandas as pd
from flask import Flask, request, render_template
import pickle

app = Flask("__name__")

# 1. Load the model and the trained columns
model = pickle.load(open("model.sav", "rb"))
trained_columns = pickle.load(open("model_columns.pkl", "rb"))

@app.route("/")
def load_page():
    """
    Renders the initial home page (GET).
    """
    return render_template("home.html", query="")

@app.route("/", methods=["POST"])
def predict():
    """
    Handles the POST request from the form submission.
    """
    try:
        # --------------------------------------------------------------------
        # 2. Retrieve user inputs (19 fields) from the form
        #    EXACTLY match the 'name' attributes in your home.html
        # --------------------------------------------------------------------
        inputQuery1  = request.form.get("query1",  "").strip()  # SeniorCitizen
        inputQuery2  = request.form.get("query2",  "").strip()  # MonthlyCharges
        inputQuery3  = request.form.get("query3",  "").strip()  # TotalCharges
        inputQuery4  = request.form.get("query4",  "").strip()  # gender
        inputQuery5  = request.form.get("query5",  "").strip()  # Partner
        inputQuery6  = request.form.get("query6",  "").strip()  # Dependents
        inputQuery7  = request.form.get("query7",  "").strip()  # PhoneService
        inputQuery8  = request.form.get("query8",  "").strip()  # MultipleLines
        inputQuery9  = request.form.get("query9",  "").strip()  # InternetService
        inputQuery10 = request.form.get("query10", "").strip()  # OnlineSecurity
        inputQuery11 = request.form.get("query11", "").strip()  # OnlineBackup
        inputQuery12 = request.form.get("query12", "").strip()  # DeviceProtection
        inputQuery13 = request.form.get("query13", "").strip()  # TechSupport
        inputQuery14 = request.form.get("query14", "").strip()  # StreamingTV
        inputQuery15 = request.form.get("query15", "").strip()  # StreamingMovies
        inputQuery16 = request.form.get("query16", "").strip()  # Contract
        inputQuery17 = request.form.get("query17", "").strip()  # PaperlessBilling
        inputQuery18 = request.form.get("query18", "").strip()  # PaymentMethod
        inputQuery19 = request.form.get("query19", "").strip()  # tenure

        # --------------------------------------------------------------------
        # 3. Convert numeric fields (handle ValueError if user typed bad input)
        # --------------------------------------------------------------------
        # SeniorCitizen is often 0 or 1; adjust if yours is "Yes/No"
        senior_citizen = int(inputQuery1) if inputQuery1 else 0

        # MonthlyCharges and TotalCharges are floats
        monthly_charges = float(inputQuery2) if inputQuery2 else 0.0
        total_charges   = float(inputQuery3) if inputQuery3 else 0.0

        # Tenure is integer
        tenure = int(inputQuery19) if inputQuery19 else 0

    except ValueError:
        # If conversion fails, show error while preserving all user inputs
        return render_template(
            "home.html",
            output1="Invalid numeric input. Please check your entries.",
            output2="",
            query1=inputQuery1,
            query2=inputQuery2,
            query3=inputQuery3,
            query4=inputQuery4,
            query5=inputQuery5,
            query6=inputQuery6,
            query7=inputQuery7,
            query8=inputQuery8,
            query9=inputQuery9,
            query10=inputQuery10,
            query11=inputQuery11,
            query12=inputQuery12,
            query13=inputQuery13,
            query14=inputQuery14,
            query15=inputQuery15,
            query16=inputQuery16,
            query17=inputQuery17,
            query18=inputQuery18,
            query19=inputQuery19
        )

    # ------------------------------------------------------------------------
    # 4. Build a single-row DataFrame using your original, pre-dummy columns
    #    (i.e., the columns that existed before pd.get_dummies).
    # ------------------------------------------------------------------------
    new_data = pd.DataFrame([[
        senior_citizen,
        monthly_charges,
        total_charges,
        inputQuery4,   # gender
        inputQuery5,   # Partner
        inputQuery6,   # Dependents
        inputQuery7,   # PhoneService
        inputQuery8,   # MultipleLines
        inputQuery9,   # InternetService
        inputQuery10,  # OnlineSecurity
        inputQuery11,  # OnlineBackup
        inputQuery12,  # DeviceProtection
        inputQuery13,  # TechSupport
        inputQuery14,  # StreamingTV
        inputQuery15,  # StreamingMovies
        inputQuery16,  # Contract
        inputQuery17,  # PaperlessBilling
        inputQuery18,  # PaymentMethod
        tenure
    ]], columns=[
        "SeniorCitizen",
        "MonthlyCharges",
        "TotalCharges",
        "gender",
        "Partner",
        "Dependents",
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaperlessBilling",
        "PaymentMethod",
        "tenure"
    ])

    # ------------------------------------------------------------------------
    # 5. Convert the single row to dummy columns
    # ------------------------------------------------------------------------
    new_data_dummies = pd.get_dummies(new_data)

    # ------------------------------------------------------------------------
    # 6. Align with the trained_columns:
    #    A) Add missing columns as 0
    #    B) Drop extra columns
    #    C) Reorder to match training
    # ------------------------------------------------------------------------
    for col in trained_columns:
        if col not in new_data_dummies.columns:
            new_data_dummies[col] = 0

    extra_cols = set(new_data_dummies.columns) - set(trained_columns)
    if extra_cols:
        new_data_dummies.drop(columns=extra_cols, inplace=True)

    new_data_dummies = new_data_dummies[trained_columns]

    # ------------------------------------------------------------------------
    # 7. Model prediction
    # ------------------------------------------------------------------------
    single_pred = model.predict(new_data_dummies)[0]
    probability = model.predict_proba(new_data_dummies)[:, 1][0]

    # ------------------------------------------------------------------------
    # 8. Interpret the result
    # ------------------------------------------------------------------------
    if single_pred == 1:
        o1 = "This customer is likely to be churned!"
    else:
        o1 = "This customer is likely to continue!"

    o2 = f"Confidence: {probability * 100:.2f}%"

    # ------------------------------------------------------------------------
    # 9. Return the template with predictions & user inputs
    # ------------------------------------------------------------------------
    return render_template(
        "home.html",
        output1=o1,
        output2=o2,
        query1=inputQuery1,
        query2=inputQuery2,
        query3=inputQuery3,
        query4=inputQuery4,
        query5=inputQuery5,
        query6=inputQuery6,
        query7=inputQuery7,
        query8=inputQuery8,
        query9=inputQuery9,
        query10=inputQuery10,
        query11=inputQuery11,
        query12=inputQuery12,
        query13=inputQuery13,
        query14=inputQuery14,
        query15=inputQuery15,
        query16=inputQuery16,
        query17=inputQuery17,
        query18=inputQuery18,
        query19=inputQuery19
    )

if __name__ == "__main__":
    # For local development
    app.run(debug=True)
