import streamlit as st
import joblib
import pandas as pd
import sklearn

print(sklearn.__version__)

# Load the FULL pipeline (preprocessing + model)
model_pipeline = joblib.load("./model/model.pkl")

st.title("🏠How much is that home gonna be?")
st.write(
    "Let's fill in the details below to find out just how much this house should be."
)

# Input fields


overallQual = st.selectbox("Passenger Class", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

Neighborhood = st.selectbox(
    "Where's this home",
    [
        "Blmngtn",
        "BrDale",
        "BrkSide",
        "ClearCr",
        "CollgCr",
        "Crawfor",
        "Edwards",
        "Gilbert",
        "IDOTRR",
        "MeadowV",
        "Mitchel",
        "NAmes",
        "NPkVill",
        "NWAmes",
        "NoRidge",
        "NridgHt",
        "OldTown",
        "SWISU",
        "Sawyer",
        "SawyerW",
        "Somerst",
        "StoneBr",
        "Timber",
        "Veenker",
    ],
)

GrLivArea = st.number_input("Ground Living Area", min_value=0, max_value=2000, value=0)

TotalBsmtSF = st.number_input(
    "Total square feet of basement area", min_value=0, max_value=2000, value=0
)
GarageCars = st.number_input(
    "Size of garage in car capacity", min_value=0, max_value=5, value=0
)
BedroomAbvGr = st.number_input(
    "How many bedrooms are above grade. excluding the basement bedrooms.",
    min_value=0,
    max_value=10,
)
YearBuilt = st.number_input(
    "What year was it buit?", min_value=1872, max_value=2026, value=2026
)
FullBath = st.slider(
    "Full Bathrooms (above grade)",
    0,
    4,
    2,
    help="Number of full bathrooms above ground level (sink + toilet + shower/tub)",
)


if st.button("Predict House Price"):
    # Create DataFrame with correct column names (must match training!)
    input_data = pd.DataFrame(
        {
            "OverallQual": [overallQual],
            "GrLivArea": [GrLivArea],
            "TotalBsmtSF": [TotalBsmtSF],
            "GarageCars": [GarageCars],
            "BedroomAbvGr": [BedroomAbvGr],
            "FullBath": [FullBath],
            "YearBuilt": [YearBuilt],
        }
    )

    # Predict using the full pipeline (handles encoding + scaling automatically!)
    prediction = model_pipeline.predict(input_data)[0]

    # Survival result
    if prediction >= 500000:
        st.success("🛟 **Yowza! This house is pretty expensive. Good luck.")
    if 300000 > prediction < 500000:
        st.warning("It's a small fortune, but hey. It's affordable")
    else:
        st.error("😔 **This might fit your budget.**")

    st.write(f"Here's the price by the way, love. ${prediction}")

