# Import required Python packages
import streamlit as st
import snowflake.snowpark.functions as F
import pandas as pd
from snowflake.ml.registry import registry
from snowflake.snowpark.context import get_active_session

# Get the current Snowflake session and data
session = get_active_session()
data = session.table("APPLICATION_RECORD_CLEANED")

# Initialize Snowflake ML model registry
native_registry = registry.Registry(session=session, database_name='FEATURES', schema_name='PUBLIC')
model_ver = native_registry.get_model('LOAN_APPROVAL_MODEL').version('V4')

# Define categorical and numerical columns
CATEGORICAL_COLUMNS = ["CODE_GENDER", "FLAG_OWN_CAR", "FLAG_OWN_REALTY", "NAME_INCOME_TYPE", 
                       "NAME_EDUCATION_TYPE", "NAME_FAMILY_STATUS", "NAME_HOUSING_TYPE", 
                       "OCCUPATION_TYPE"]
NUMERICAL_COLUMNS = ["CNT_CHILDREN", "AMT_INCOME_TOTAL", "DAYS_EMPLOYED","FLAG_MOBIL",
    "FLAG_WORK_PHONE",
    "FLAG_PHONE",
    "FLAG_EMAIL", 
    "CNT_FAM_MEMBERS", "AGE"]

# Default values for input fields based on data type
DEFAULT_VALUES = {
    "CNT_CHILDREN": 0,
    "AMT_INCOME_TOTAL": 50000,
    "DAYS_EMPLOYED": 1000,
    "FLAG_MOBIL": 1,
    "FLAG_WORK_PHONE": 1,
    "FLAG_PHONE": 1,
    "FLAG_EMAIL": 1,
    "CNT_FAM_MEMBERS": 1,
    "AGE": 30,
    "CODE_GENDER": "F",
    "FLAG_OWN_CAR": "N",
    "FLAG_OWN_REALTY": "Y",
    "NAME_INCOME_TYPE": "Working",
    "NAME_EDUCATION_TYPE": "Secondary / secondary special",
    "NAME_FAMILY_STATUS": "Married",
    "NAME_HOUSING_TYPE": "House / apartment",
    "OCCUPATION_TYPE": "Laborers"
}

# Streamlit UI setup
st.title("Loan Approval Prediction")
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Display introductory text
st.write("Welcome to the Loan Approval Prediction App!")
st.write("Please fill in the following information about the applicant:")

# Display form for user input
with st.form("my_form"):
    form = {}
    st.subheader("Applicant Information")
    num_columns = len(CATEGORICAL_COLUMNS)
    num_rows = -(-num_columns // 4)  # Ceiling division to calculate number of rows needed
    cols = st.columns(4)
    for i, column in enumerate(CATEGORICAL_COLUMNS):
        with cols[i % 4]:
            form[column] = st.selectbox(f"{column}", data.select(F.col(column)).distinct())
    num_columns = len(NUMERICAL_COLUMNS)
    num_rows = -(-num_columns // 4)  # Ceiling division to calculate number of rows needed
    cols = st.columns(4)
    for i, column in enumerate(NUMERICAL_COLUMNS):
        with cols[i % 4]:
            form[column] = st.number_input(f"{column}", value=DEFAULT_VALUES[column])
    submit_button = st.form_submit_button('Submit application')

# Process user input and make prediction
if submit_button:
    st.session_state.submitted = True
    input_data = pd.DataFrame([form])
    remote_prediction = model_ver.run(input_data, function_name="predict")
    if remote_prediction['PREDICTED_CAT'][0] == 0:
        st.error("Loan Denied")
    else:
        st.success("Loan Approved")
