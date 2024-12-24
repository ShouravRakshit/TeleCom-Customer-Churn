# Telecom Customer Churn Prediction

Welcome to the **Telecom Customer Churn Prediction** project! This repository demonstrates an end-to-end machine learning solution that predicts whether a customer is likely to churn (i.e., discontinue service). The final model achieves **94% accuracy** and is deployed as a Flask web application.

## Table of Contents
- [Overview](#overview)
- [Data Description](#data-description)
- [Setup](#setup)
- [Contact](#contact)


---

## Overview
This project aims to predict customer churn for a fictional telecommunications company. By identifying churn-prone customers, telecom providers can take proactive measures (e.g., targeted marketing campaigns, better support) to improve retention.

**Key Objectives**:
1. Clean and explore the telecom dataset.
2. Engineer features (tenure binning, dummy encoding, etc.) to improve model performance.
3. Handle class imbalance using SMOTE or related techniques.
4. Build multiple machine learning models (Decision Tree, Random Forest, etc.) and select the best performer.
5. Deploy the final model via a Flask web app where users can input customer info and obtain a churn prediction.

**Final Accuracy**: ~94%

---

## Data Description
- **Source**: The dataset (`data.csv` or `tel_churn.csv`) contains ~7,000+ rows of customer information.
- **Columns** (examples):
  - `customerID`, `gender`, `SeniorCitizen`, `Partner`, `Dependents`
  - `tenure`, `PhoneService`, `MultipleLines`, `InternetService`, ...
  - `Contract`, `PaperlessBilling`, `PaymentMethod`
  - `MonthlyCharges`, `TotalCharges`
  - `Churn` (Yes/No) – the target variable

For privacy reasons, this dataset is a mock or sample dataset.

---

## Setup
- Clone the repo
```bash
git clone https://github.com/ShouravRakshit/TeleCom-Customer-Churn.git

```
- Install the required packages
```bash
pip install -r requirements.txt

```
- Run the app
```bash
python app.py

```
# **Contact**
- Shourav Rakshit Ivan, Email: shouravrakshit.ivan@ucalgary.ca  (UCID: 30131085)

University of Calgary


