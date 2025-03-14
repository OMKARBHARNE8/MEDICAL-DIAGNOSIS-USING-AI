import streamlit as st
import pickle
from streamlit_option_menu import option_menu
import pandas as pd

# Change Name & Logo
st.set_page_config(page_title="Disease Prediction", page_icon="⚕️")

# Hide Streamlit Default UI Elements
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Updated background and styling
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background: #1a1a1a; /* Light black */
    color: #ffffff;
}


[data-testid="stSidebar"] {
    background: rgba(26, 26, 46, 0.95);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.result-card {
    background: rgba(0, 255, 0, 0.1);
    padding: 15px;
    border-radius: 8px;
    border: 1px solid rgba(0, 255, 0, 0.2);
    margin-top: 20px;
}

.stButton>button {
    background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 25px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
}

.stTextInput>div>div>input {
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

h1 {
    background: linear-gradient(90deg, #4CAF50, #81C784);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5em;
    margin-bottom: 30px;
}

.hint-text {
    color: #a0a0a0;
    font-size: 0.8em;
    margin-top: 5px;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


st.markdown(page_bg_img, unsafe_allow_html=True)

# Load the saved models
models = {
    'diabetes': pickle.load(open('Models/diabetes_model.sav', 'rb')),
    'heart_disease': pickle.load(open('Models/heart_disease_model.sav', 'rb')),
    'parkinsons': pickle.load(open('Models/parkinsons_model.sav', 'rb')),
    'lung_cancer': pickle.load(open('Models/lungs_disease_model.sav', 'rb')),
    'thyroid': pickle.load(open('Models/Thyroid_model.sav', 'rb'))
}

selected = st.sidebar.radio(
    'Select Disease to Predict',
    ['Diabetes Prediction',
     'Heart Disease Prediction',
     'Parkinsons Prediction',
     'Lung Cancer Prediction',
     'Hypo-Thyroid Prediction']
)

# Helper function for input groups
def create_input_group(title, inputs):
    with st.expander(title, expanded=True):
        cols = st.columns(2)
        values = []
        for i, (label, tooltip, key, input_type) in enumerate(inputs):
            with cols[i % 2]:
                if input_type == "number":
                    # Set decimal step for Diabetes Pedigree Function
                    step = 0.001 if key == "DiabetesPedigreeFunction" else 1
                    value = st.number_input(label, key=key, help=tooltip, step=step)
                else:
                    value = st.text_input(label, key=key, help=tooltip)
                values.append(value)
    return values

# Improved disease prediction function
def predict_disease(model, input_data, disease_name):
    try:
        prediction = model.predict([input_data])
        result = prediction[0] == 1
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(
                f"""
                <div class="result-card">
                    <h3>{'🚨 ' if result else '✅ '}Prediction Result</h3>
                    <p>The person {'has' if result else 'does not have'} {disease_name}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Show confidence score if available
        if hasattr(model, 'predict_proba'):
            with col2:
                confidence = model.predict_proba([input_data])[0][1]
                st.metric("Confidence", f"{confidence:.2%}")
        
        return result
    except Exception as e:
        st.error(f"Error in prediction: {str(e)}")
        return None

# Main content area
st.title(f"AI-Powered {selected}")

# Disease-specific input handling
if selected == 'Diabetes Prediction':
    with st.container():
        st.markdown("<div class='disease-card'>", unsafe_allow_html=True)
        inputs = [
            ("Number of Pregnancies", "Number of times pregnant", "Pregnancies", "number"),
            ("Glucose Level", "Enter glucose level", "Glucose", "number"),
            ("Blood Pressure", "Enter blood pressure value", "BloodPressure", "number"),
            ("Skin Thickness", "Enter skin thickness value", "SkinThickness", "number"),
            ("Insulin Level", "Enter insulin level", "Insulin", "number"),
            ("BMI", "Enter Body Mass Index value", "BMI", "number"),
            ("Diabetes Pedigree Function", "Enter diabetes pedigree function value", "DiabetesPedigreeFunction", "number"),
            ("Age", "Enter age of the person", "Age", "number")
        ]
        values = create_input_group("Patient Information", inputs)
        
        if st.button('Predict Diabetes'):
            predict_disease(models['diabetes'], values, "Diabetes")
        st.markdown("</div>", unsafe_allow_html=True)

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    with st.container():
        st.markdown("<div class='disease-card'>", unsafe_allow_html=True)
        inputs = [
            ('Age', 'Enter age of the person', 'age', 'number'),
            ('Sex (1 = male; 0 = female)', 'Enter sex of the person', 'sex', 'number'),
            ('Chest Pain types (0, 1, 2, 3)', 'Enter chest pain type', 'cp', 'number'),
            ('Resting Blood Pressure', 'Enter resting blood pressure', 'trestbps', 'number'),
            ('Serum Cholesterol in mg/dl', 'Enter serum cholesterol', 'chol', 'number'),
            ('Fasting Blood Sugar > 120 mg/dl (1 = true; 0 = false)', 'Enter fasting blood sugar', 'fbs', 'number'),
            ('Resting Electrocardiographic results (0, 1, 2)', 'Enter resting ECG results', 'restecg', 'number'),
            ('Maximum Heart Rate achieved', 'Enter maximum heart rate', 'thalach', 'number'),
            ('Exercise Induced Angina (1 = yes; 0 = no)', 'Enter exercise induced angina', 'exang', 'number'),
            ('ST depression induced by exercise', 'Enter ST depression value', 'oldpeak', 'number'),
            ('Slope of the peak exercise ST segment (0, 1, 2)', 'Enter slope value', 'slope', 'number'),
            ('Major vessels colored by fluoroscopy (0-3)', 'Enter number of major vessels', 'ca', 'number'),
            ('Thal (0 = normal; 1 = fixed defect; 2 = reversible defect)', 'Enter thal value', 'thal', 'number')
        ]
        values = create_input_group("Patient Information", inputs)
        
        if st.button('Predict Heart Disease'):
            predict_disease(models['heart_disease'], values, "Heart Disease")
        st.markdown("</div>", unsafe_allow_html=True)

# Parkinson's Prediction Page
if selected == "Parkinsons Prediction":
    with st.container():
        st.markdown("<div class='disease-card'>", unsafe_allow_html=True)
        inputs = [
            ('MDVP:Fo(Hz)', 'Enter MDVP:Fo(Hz) value', 'fo', 'number'),
            ('MDVP:Fhi(Hz)', 'Enter MDVP:Fhi(Hz) value', 'fhi', 'number'),
            ('MDVP:Flo(Hz)', 'Enter MDVP:Flo(Hz) value', 'flo', 'number'),
            ('MDVP:Jitter(%)', 'Enter MDVP:Jitter(%) value', 'Jitter_percent', 'number'),
            ('MDVP:Jitter(Abs)', 'Enter MDVP:Jitter(Abs) value', 'Jitter_Abs', 'number'),
            ('MDVP:RAP', 'Enter MDVP:RAP value', 'RAP', 'number'),
            ('MDVP:PPQ', 'Enter MDVP:PPQ value', 'PPQ', 'number'),
            ('Jitter:DDP', 'Enter Jitter:DDP value', 'DDP', 'number'),
            ('MDVP:Shimmer', 'Enter MDVP:Shimmer value', 'Shimmer', 'number'),
            ('MDVP:Shimmer(dB)', 'Enter MDVP:Shimmer(dB) value', 'Shimmer_dB', 'number'),
            ('Shimmer:APQ3', 'Enter Shimmer:APQ3 value', 'APQ3', 'number'),
            ('Shimmer:APQ5', 'Enter Shimmer:APQ5 value', 'APQ5', 'number'),
            ('MDVP:APQ', 'Enter MDVP:APQ value', 'APQ', 'number'),
            ('Shimmer:DDA', 'Enter Shimmer:DDA value', 'DDA', 'number'),
            ('NHR', 'Enter NHR value', 'NHR', 'number'),
            ('HNR', 'Enter HNR value', 'HNR', 'number'),
            ('RPDE', 'Enter RPDE value', 'RPDE', 'number'),
            ('DFA', 'Enter DFA value', 'DFA', 'number'),
            ('Spread1', 'Enter spread1 value', 'spread1', 'number'),
            ('Spread2', 'Enter spread2 value', 'spread2', 'number'),
            ('D2', 'Enter D2 value', 'D2', 'number'),
            ('PPE', 'Enter PPE value', 'PPE', 'number')
        ]
        values = create_input_group("Patient Information", inputs)
        
        if st.button("Predict Parkinson's"):
            predict_disease(models['parkinsons'], values, "Parkinson's Disease")
        st.markdown("</div>", unsafe_allow_html=True)

# Lung Cancer Prediction Page
if selected == "Lung Cancer Prediction":
    with st.container():
        st.markdown("<div class='disease-card'>", unsafe_allow_html=True)
        inputs = [
            ('Gender (1 = Male; 0 = Female)', 'Enter gender of the person', 'GENDER', 'number'),
            ('Age', 'Enter age of the person', 'AGE', 'number'),
            ('Smoking (1 = NO; 2 = YES)', 'Enter if the person smokes', 'SMOKING', 'number'),
            ('Yellow Fingers (1 = NO; 2 = YES)', 'Enter if the person has yellow fingers', 'YELLOW_FINGERS', 'number'),
            ('Anxiety (1 = NO; 2 = YES)', 'Enter the level of anxiety (1 = Yes, 2 = No)', 'ANXIETY', 'number'),
            ('Peer Pressure (1 = NO; 2 = YES)', 'Enter if the person is under peer pressure (1 = Yes, 2 = No)', 'PEER_PRESSURE', 'number'),
            ('Chronic Disease (1 = NO; 2 = YES)', 'Enter if the person has a chronic disease (1 = Yes, 2 = No)', 'CHRONIC_DISEASE', 'number'),
            ('Fatigue (1 = NO; 2 = YES)', 'Enter if the person experiences fatigue (1 = Yes, 2 = No)', 'FATIGUE', 'number'),
            ('Allergy (1 = NO; 2 = YES)', 'Enter if the person has allergies (1 = Yes, 2 = No)', 'ALLERGY', 'number'),
            ('Wheezing (1 = NO; 2 = YES)', 'Enter if the person experiences wheezing (1 = Yes, 2 = No)', 'WHEEZING', 'number'),
            ('Alcohol Consuming (1 = NO; 2 = YES)', 'Enter if the person consumes alcohol (1 = Yes, 2 = No)', 'ALCOHOL_CONSUMING', 'number'),
            ('Coughing (1 = NO; 2 = YES)', 'Enter if the person experiences coughing (1 = Yes, 2 = No)', 'COUGHING', 'number'),
            ('Shortness Of Breath (1 = NO; 2 = YES)', 'Enter if the person experiences shortness of breath (1 = Yes, 2 = No)', 'SHORTNESS_OF_BREATH', 'number'),
            ('Swallowing Difficulty (1 = NO; 2 = YES)', 'Enter if the person has difficulty swallowing (1 = Yes, 2 = No)', 'SWALLOWING_DIFFICULTY', 'number'),
            ('Chest Pain (1 = NO; 2 = YES)', 'Enter if the person experiences chest pain (1 = Yes, 2 = No)', 'CHEST_PAIN', 'number')
        ]
        values = create_input_group("Patient Information", inputs)
        
        if st.button("Predict Lung Cancer"):
            predict_disease(models['lung_cancer'], values, "Lung Cancer")
        st.markdown("</div>", unsafe_allow_html=True)

# Hypo-Thyroid Prediction Page
if selected == "Hypo-Thyroid Prediction":
    with st.container():
        st.markdown("<div class='disease-card'>", unsafe_allow_html=True)
        inputs = [
            ('Age', 'Enter age of the person', 'age', 'number'),
            ('Sex (1 = Male; 0 = Female)', 'Enter sex of the person', 'sex', 'number'),
            ('On Thyroxine (1 = Yes; 0 = No)', 'Enter if the person is on thyroxine', 'on_thyroxine', 'number'),
            ('TSH Level', 'Enter TSH level', 'tsh', 'number'),
            ('T3 Measured (1 = Yes; 0 = No)', 'Enter if T3 was measured', 't3_measured', 'number'),
            ('T3 Level', 'Enter T3 level', 't3', 'number'),
            ('TT4 Level', 'Enter TT4 level', 'tt4', 'number')
        ]
        values = create_input_group("Patient Information", inputs)
        
        if st.button("Predict Hypo-Thyroid"):
            predict_disease(models['thyroid'], values, "Hypo-Thyroid")
        st.markdown("</div>", unsafe_allow_html=True)
