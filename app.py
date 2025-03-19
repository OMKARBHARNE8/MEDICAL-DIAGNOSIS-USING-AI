import streamlit as st
import pickle
from streamlit_option_menu import option_menu
import pandas as pd

st.set_page_config(page_title="Disease Prediction", page_icon="⚕️", layout="wide")

# Hide Default Streamlit UI
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Optimized Layout and Styling
page_bg_img = """
<style>
/* Page Layout */
[data-testid="stAppViewContainer"] {
    background: #121212;  /* Dark Mode */
    color: white;
    padding-top: 10px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(30, 30, 50, 0.95);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 15px;
}

/* Cards */
.result-card {
    background: rgba(76, 175, 80, 0.15);
    padding: 15px;
    border-radius: 10px;
    border: 1px solid rgba(76, 175, 80, 0.3);
    box-shadow: 0px 3px 10px rgba(76, 175, 80, 0.2);
    margin-top: 15px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #4CAF50 0%, #2E7D32 100%);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: bold;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

/* Input Fields */
.stTextInput>div>div>input, .stNumberInput>div>div>input {
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 5px;
    padding: 8px;
    font-size: 14px;
}

/* Headings */
h1 {
    background: linear-gradient(90deg, #4CAF50, #81C784);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.2em;
    margin-bottom: 15px;
    text-align: center;
}

/* Compact Layout */
.block-container {
    padding-top: 5px;
    padding-bottom: 5px;
    max-width: 90%;
    margin: auto;
}

/* Align Inputs in Two Columns */
.input-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    padding: 10px;
}

/* Small Hint Text */
.hint-text {
    color: #a0a0a0;
    font-size: 0.75em;
    text-align: center;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)



# Arrange Input Fields in Two Columns
st.markdown('<div class="input-container">', unsafe_allow_html=True)


# Load the saved models
models = {
    'diabetes': pickle.load(open("F:\TRIAL\Medical diagnosis using AI\Jupyter Notebook\diabetes_model.sav", 'rb')),
    'heart_disease': pickle.load(open("F:\TRIAL\Medical diagnosis using AI\Jupyter Notebook\heart_disease_model.sav", 'rb')),
    'parkinsons': pickle.load(open("F:\TRIAL\Medical diagnosis using AI\Jupyter Notebook\parkinsons_model.sav", 'rb')),
    'lung_cancer': pickle.load(open("F:\TRIAL\Medical diagnosis using AI\Jupyter Notebook\lungs_disease_model.sav", 'rb')),
    'thyroid': pickle.load(open("F:\TRIAL\Medical diagnosis using AI\Jupyter Notebook\Thyroid_model.sav", 'rb'))
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
                if input_type == "float":
                    value = st.number_input(label, key=key, help=tooltip, format="%.6f", step=0.000001)
                elif input_type == "number":
                    step = 0.001 if key == "DiabetesPedigreeFunction" else 1
                    value = st.number_input(label, key=key, help=tooltip, step=step)
                else:
                    value = st.text_input(label, key=key, help=tooltip)
                values.append(float(value) if input_type == "float" else value)
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
        return result  # Ensure function completes execution

    except Exception as e:
        st.error(f"Error in prediction: {e}")  # Properly handling errors
       
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
            ('MDVP:Fo(Hz)', 'Enter MDVP:Fo(Hz) value', 'fo', 'float'),
            ('MDVP:Fhi(Hz)', 'Enter MDVP:Fhi(Hz) value', 'fhi', 'float'),
            ('MDVP:Flo(Hz)', 'Enter MDVP:Flo(Hz) value', 'flo', 'float'),
            ('MDVP:Jitter(%)', 'Enter MDVP:Jitter(%) value', 'Jitter_percent', 'float'),
            ('MDVP:Jitter(Abs)', 'Enter MDVP:Jitter(Abs) value', 'Jitter_Abs', 'float'),
            ('MDVP:RAP', 'Enter MDVP:RAP value', 'RAP', 'float'),
            ('MDVP:PPQ', 'Enter MDVP:PPQ value', 'PPQ', 'float'),
            ('Jitter:DDP', 'Enter Jitter:DDP value', 'DDP', 'float'),
            ('MDVP:Shimmer', 'Enter MDVP:Shimmer value', 'Shimmer', 'float'),
            ('MDVP:Shimmer(dB)', 'Enter MDVP:Shimmer(dB) value', 'Shimmer_dB', 'float'),
            ('Shimmer:APQ3', 'Enter Shimmer:APQ3 value', 'APQ3', 'float'),
            ('Shimmer:APQ5', 'Enter Shimmer:APQ5 value', 'APQ5', 'float'),
            ('MDVP:APQ', 'Enter MDVP:APQ value', 'APQ', 'float'),
            ('Shimmer:DDA', 'Enter Shimmer:DDA value', 'DDA', 'float'),
            ('NHR', 'Enter NHR value', 'NHR', 'float'),
            ('HNR', 'Enter HNR value', 'HNR', 'float'),
            ('RPDE', 'Enter RPDE value', 'RPDE', 'float'),
            ('DFA', 'Enter DFA value', 'DFA', 'float'),
            ('Spread1', 'Enter spread1 value', 'spread1', 'float'),
            ('Spread2', 'Enter spread2 value', 'spread2', 'float'),
            ('D2', 'Enter D2 value', 'D2', 'float'),
            ('PPE', 'Enter PPE value', 'PPE', 'float')
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
            ('TSH Level', 'Enter TSH level', 'tsh', 'float'),
            ('T3 Measured (1 = Yes; 0 = No)', 'Enter if T3 was measured', 't3_measured', 'number'),
            ('T3 Level', 'Enter T3 level', 't3', 'float'),
            ('TT4 Level', 'Enter TT4 level', 'tt4', 'float')
        ]
        values = create_input_group("Patient Information", inputs)
        
        if st.button("Predict Hypo-Thyroid"):
            predict_disease(models['thyroid'], values, "Hypo-Thyroid")
        st.markdown("</div>", unsafe_allow_html=True)
