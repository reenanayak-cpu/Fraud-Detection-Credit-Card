import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

# ── Load saved model & encoders ──────────────────
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("le_payment.pkl", "rb") as f:
        le_payment = pickle.load(f)
    with open("le_merchant.pkl", "rb") as f:
        le_merchant = pickle.load(f)
    return model, le_payment, le_merchant

rfc, le_payment, le_merchant = load_model()

# ── Load data (for EDA only) ──────────────────────
@st.cache_data
def load_data():
    data = pd.read_csv("fraud_detection_credit_card.csv")
    data = data.drop(columns=["Unnamed: 0"])
    return data

data = load_data()

# ── Sidebar ───────────────────────────────────────
st.sidebar.title("🔍 Fraud Detection App")
page = st.sidebar.radio("Navigate", ["Overview", "EDA", "Model Results", "Predict"])

# ── Page 1: Overview ──────────────────────────────
if page == "Overview":
    st.title("Credit Card Fraud Detection")
    st.dataframe(data.head())
    st.write(data.describe())

# ── Page 2: EDA ───────────────────────────────────
elif page == "EDA":
    st.title("Exploratory Data Analysis")

    fig, ax = plt.subplots()
    data['is_fraud'].value_counts().plot(kind='bar', ax=ax, color=['green','red'])
    ax.set_title("Fraud vs Legitimate")
    st.pyplot(fig)

    fig2, ax2 = plt.subplots()
    data.groupby('Merchant_Category')['is_fraud'].mean().plot(kind='bar', ax=ax2)
    ax2.set_title("Fraud Rate by Merchant Category")
    st.pyplot(fig2)

# ── Page 3: Model Results ─────────────────────────
elif page == "Model Results":
    st.title("Model Performance")
    st.markdown("**Algorithm:** Random Forest Classifier")
    st.markdown("**Features used:** Customer Age, Transaction Amount, Payment Method, Merchant Category")

    # These are the exact results from your notebook output
    st.subheader("Classification Report")
    report = {
        'Class': ['Legitimate (0)', 'Fraud (1)'],
        'Precision': [1.00, 0.56],
        'Recall': [1.00, 0.22],
        'F1-Score': [1.00, 0.32],
        'Support': [29818, 182]
    }
    st.dataframe(pd.DataFrame(report))
    st.metric("Overall Accuracy", "99%")

# ── Page 4: Predict ───────────────────────────────
elif page == "Predict":
    st.title("🔮 Predict Fraud on New Transaction")

    age = st.slider("Customer Age", 18, 70, 35)
    amt = st.number_input("Transaction Amount ($)", 1.0, 10000.0, 50.0)
    payment = st.selectbox("Payment Method", le_payment.classes_)
    merchant_cat = st.selectbox("Merchant Category", le_merchant.classes_)

    if st.button("Predict", type="primary"):
        payment_enc = le_payment.transform([payment])[0]
        merchant_enc = le_merchant.transform([merchant_cat])[0]

        input_data = np.array([[age, amt, payment_enc, merchant_enc]])
        prediction = rfc.predict(input_data)[0]
        probability = rfc.predict_proba(input_data)[0]

        if prediction == 1:
            st.error(f"🚨 FRAUDULENT Transaction detected! ({probability[1]*100:.1f}% confidence)")
        else:
            st.success(f"✅ Legitimate Transaction ({probability[0]*100:.1f}% confidence)")

